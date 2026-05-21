import json, os, shutil

BASE_DIR = r"C:\Users\Donizete Senne\Desktop\Mob2Con-Central\02-Powerbi-Projetos\Nordestão Exclusivo dn.Report\definition\pages"
GRID = 8
MARGIN = 12

def fix_val(val, is_pos=True):
    if val is None: return 0
    # Se for posição x/y e estiver perto da margem (12), mantém 12. Senão, arredonda para múltiplo de 8.
    if is_pos and abs(val - MARGIN) <= 4:
        return MARGIN
    return int(round(val / GRID) * GRID)

def fix_page(page_name):
    page_path = os.path.join(BASE_DIR, page_name, "visuals")
    if not os.path.exists(page_path): return
    
    print(f"Corrigindo página: {page_name}")
    for folder in os.listdir(page_path):
        vj = os.path.join(page_path, folder, "visual.json")
        if not os.path.exists(vj): continue
        
        with open(vj, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        pos = data.get("position", {})
        if not pos: continue
        
        # Backup
        bak = vj + ".bak"
        if not os.path.exists(bak): shutil.copy2(vj, bak)
        
        old_pos = pos.copy()
        pos["x"] = fix_val(pos.get("x", 0), True)
        pos["y"] = fix_val(pos.get("y", 0), True)
        pos["width"] = fix_val(pos.get("width", 0), False)
        pos["height"] = fix_val(pos.get("height", 0), False)
        
        if old_pos != pos:
            print(f"  - {folder}: ({old_pos['x']},{old_pos['y']}) {old_pos['width']}x{old_pos['height']} -> ({pos['x']},{pos['y']}) {pos['width']}x{pos['height']}")
            with open(vj, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

pages = ["pg_estoque", "pg_executivo", "pg_ruptura", "pg_vendas", "pg_operacao", "pg_produtividade"]
for p in pages:
    fix_page(p)
