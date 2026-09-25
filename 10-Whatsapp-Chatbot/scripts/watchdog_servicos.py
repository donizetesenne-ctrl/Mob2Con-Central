"""Watchdog local do chatbot Mob2Con.

Executa o worker PowerShell de saude periodicamente. Nao le nem altera o
pareamento, o banco ou o .env. A Tarefa Agendada mantem este processo vivo;
o proprio processo recupera bot e gateway.
"""

from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
import msvcrt
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import BinaryIO

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / "dados"
WORKER = ROOT / "SUPERVISOR-SERVICOS.ps1"
LOG = ROOT / "watchdog.log"
HEARTBEAT = DADOS / "watchdog-heartbeat.json"
LOCK = DADOS / "watchdog.lock"
POWERSHELL = Path(os.environ.get("SystemRoot", r"C:\Windows")) / (
    r"System32\WindowsPowerShell\v1.0\powershell.exe"
)
INTERVAL_SECONDS = 30
WORKER_TIMEOUT_SECONDS = 180
CREATE_NO_WINDOW = 0x08000000

running = True


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("mob2con.watchdog")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        LOG,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-7s %(message)s")
    )
    logger.addHandler(handler)
    return logger


def acquire_lock() -> BinaryIO | None:
    DADOS.mkdir(parents=True, exist_ok=True)
    handle = LOCK.open("a+b")
    handle.seek(0, os.SEEK_END)
    if handle.tell() == 0:
        handle.write(b"0")
        handle.flush()
    handle.seek(0)
    try:
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        handle.close()
        return None
    return handle


def write_heartbeat(exit_code: int | None, duration: float, error: str = "") -> None:
    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "pid": os.getpid(),
        "worker_exit_code": exit_code,
        "worker_duration_seconds": round(duration, 3),
        "error": error,
    }
    temporary = HEARTBEAT.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=True, separators=(",", ":")),
        encoding="utf-8",
    )
    os.replace(temporary, HEARTBEAT)


def run_worker(logger: logging.Logger) -> None:
    started = time.monotonic()
    exit_code: int | None = None
    error = ""
    try:
        completed = subprocess.run(
            [
                str(POWERSHELL),
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(WORKER),
            ],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=WORKER_TIMEOUT_SECONDS,
            check=False,
            creationflags=CREATE_NO_WINDOW,
        )
        exit_code = completed.returncode
        if exit_code != 0:
            logger.warning("Worker de saude terminou com codigo %s", exit_code)
    except subprocess.TimeoutExpired:
        error = f"worker excedeu {WORKER_TIMEOUT_SECONDS}s"
        logger.error(error)
    except Exception as exc:  # pragma: no cover - defesa operacional
        error = f"falha ao executar worker: {exc}"
        logger.exception(error)
    finally:
        write_heartbeat(exit_code, time.monotonic() - started, error)


def request_stop(signum: int, _frame: object) -> None:
    global running
    running = False


def main() -> int:
    logger = configure_logging()
    lock_handle = acquire_lock()
    if lock_handle is None:
        logger.info("Outra instancia do watchdog ja esta ativa; encerrando duplicata.")
        return 0

    for signum in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(signum, request_stop)
        except (ValueError, OSError):
            pass

    logger.info("Watchdog iniciado | pid=%s | intervalo=%ss", os.getpid(), INTERVAL_SECONDS)
    try:
        while running:
            run_worker(logger)
            for _ in range(INTERVAL_SECONDS):
                if not running:
                    break
                time.sleep(1)
    except Exception:  # pragma: no cover - deixa Scheduler reiniciar
        logger.exception("Watchdog encerrou por falha nao tratada.")
        return 1
    finally:
        try:
            msvcrt.locking(lock_handle.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
        lock_handle.close()
        logger.info("Watchdog encerrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
