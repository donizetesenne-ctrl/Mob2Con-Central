# Medidas HTML Corrigidas — Brand Mob2Con
> Aplicar quando o Power BI Desktop reabrir

## Cores aplicadas (design-tokens.json)
- Verde sucesso: `#107C41`
- Vermelho alerta: `#C00000`
- Laranja Mob2Con: `#F46901`
- Grafite: `#434343`
- Preto título: `#111111`
- Fundo card: `#FFFFFF`
- Fundo neutro: `#F3F2F1`
- Fonte: `Raleway, sans-serif`

---

## 1. !Comparativo vendas m1 m2 (HTML)

```dax
VAR MaxDate = CALCULATE(MAX('Date'[dt_referencia]), ALLSELECTED('Date'))
VAR M1_Fim = EOMONTH(MaxDate, -1)
VAR M0_Fim = EOMONTH(MaxDate, -2)
VAR vM1 = CALCULATE([Venda (Qtd.) M-1], DATESINPERIOD('Date'[dt_referencia], M1_Fim, -1, MONTH))
VAR vM0 = CALCULATE([Venda (Qtd.) M-2], DATESINPERIOD('Date'[dt_referencia], M0_Fim, -1, MONTH))
VAR NomeM0 = FORMAT(M0_Fim, "MMM")
VAR NomeM1 = FORMAT(M1_Fim, "MMM")
VAR vPerc = DIVIDE(vM1 - vM0, vM0)
VAR IconColor = IF(vPerc > 0, "#107C41", IF(vPerc < 0, "#C00000", "#434343"))
VAR Icon = IF(vPerc > 0, "▲", IF(vPerc < 0, "▼", "►"))
RETURN
"<div style='font-family:Raleway,sans-serif;font-size:13px;padding:8px;background:#FFFFFF;border-radius:6px;border-left:4px solid #F46901;'>" &
"<b>Vendas (Qtd.)</b><br>" &
UPPER(NomeM0) & " " & FORMAT(vM0, "#,##0") & " → " &
UPPER(NomeM1) & " " & FORMAT(vM1, "#,##0") &
" <span style='color:" & IconColor & ";font-weight:700;'>" & Icon & " " & FORMAT(vPerc, "0.0%") & "</span></div>"
```

---

## 2. !Comparativo rupt op m1 m2 (HTML)

```dax
VAR MaxDate = CALCULATE(MAX('Date'[dt_referencia]), ALLSELECTED('Date'))
VAR M1_Fim = EOMONTH(MaxDate, -1)
VAR M0_Fim = EOMONTH(MaxDate, -2)
VAR vM1 = CALCULATE([% Ruptura Operacional (Qtd.) Rede], DATESINPERIOD('Date'[dt_referencia], M1_Fim, -1, MONTH))
VAR vM0 = CALCULATE([% Ruptura Operacional (Qtd.) Rede], DATESINPERIOD('Date'[dt_referencia], M0_Fim, -1, MONTH))
VAR NomeM0 = FORMAT(M0_Fim, "MMM")
VAR NomeM1 = FORMAT(M1_Fim, "MMM")
VAR vPerc = DIVIDE(vM1 - vM0, vM0)
VAR IconColor = IF(vPerc > 0, "#C00000", IF(vPerc < 0, "#107C41", "#434343"))
VAR Icon = IF(vPerc > 0, "▲", IF(vPerc < 0, "▼", "►"))
RETURN
"<div style='font-family:Raleway,sans-serif;font-size:13px;padding:8px;background:#FFFFFF;border-radius:6px;border-left:4px solid #C00000;'>" &
"<b>Ruptura Operacional (Qtd.)</b><br>" &
UPPER(NomeM0) & " " & FORMAT(vM0, "0.0%") & " → " &
UPPER(NomeM1) & " " & FORMAT(vM1, "0.0%") &
" <span style='color:" & IconColor & ";font-weight:700;'>" & Icon & " " & FORMAT(vPerc, "0.0%") & "</span></div>"
```

---

## 3. !Comparativo rupt com m1 m2 (HTML)

```dax
VAR MaxDate = CALCULATE(MAX('Date'[dt_referencia]), ALLSELECTED('Date'))
VAR M1_Fim = EOMONTH(MaxDate, -1)
VAR M0_Fim = EOMONTH(MaxDate, -2)
VAR vM1 = CALCULATE([% Ruptura Comercial (Qtd.) Rede], DATESINPERIOD('Date'[dt_referencia], M1_Fim, -1, MONTH))
VAR vM0 = CALCULATE([% Ruptura Comercial (Qtd.) Rede], DATESINPERIOD('Date'[dt_referencia], M0_Fim, -1, MONTH))
VAR NomeM0 = FORMAT(M0_Fim, "MMM")
VAR NomeM1 = FORMAT(M1_Fim, "MMM")
VAR vPerc = DIVIDE(vM1 - vM0, vM0)
VAR IconColor = IF(vPerc > 0, "#C00000", IF(vPerc < 0, "#107C41", "#434343"))
VAR Icon = IF(vPerc > 0, "▲", IF(vPerc < 0, "▼", "►"))
RETURN
"<div style='font-family:Raleway,sans-serif;font-size:13px;padding:8px;background:#FFFFFF;border-radius:6px;border-left:4px solid #F46901;'>" &
"<b>Ruptura Comercial (Qtd.)</b><br>" &
UPPER(NomeM0) & " " & FORMAT(vM0, "0.0%") & " → " &
UPPER(NomeM1) & " " & FORMAT(vM1, "0.0%") &
" <span style='color:" & IconColor & ";font-weight:700;'>" & Icon & " " & FORMAT(vPerc, "0.0%") & "</span></div>"
```

---

## 4. !Comparativo efetiv m1 m2 (HTML) — COM BARRA DE PROGRESSO

```dax
VAR MaxDate = CALCULATE(MAX('Date'[dt_referencia]), ALLSELECTED('Date'))
VAR M1_Fim = EOMONTH(MaxDate, -1)
VAR M0_Fim = EOMONTH(MaxDate, -2)
VAR vM1 = CALCULATE([%VISITAS], DATESINPERIOD('Date'[dt_referencia], M1_Fim, -1, MONTH))
VAR vM0 = CALCULATE([%VISITAS], DATESINPERIOD('Date'[dt_referencia], M0_Fim, -1, MONTH))
VAR NomeM0 = FORMAT(M0_Fim, "MMM")
VAR NomeM1 = FORMAT(M1_Fim, "MMM")
VAR vPerc = DIVIDE(vM1 - vM0, vM0)
VAR IconColor = IF(vPerc > 0, "#107C41", IF(vPerc < 0, "#C00000", "#434343"))
VAR Icon = IF(vPerc > 0, "▲", IF(vPerc < 0, "▼", "►"))
VAR BarWidth = ROUND(vM1 * 100, 0)
VAR BarColor = IF(vM1 >= 0.8, "#107C41", IF(vM1 >= 0.6, "#F46901", "#C00000"))
RETURN
"<div style='font-family:Raleway,sans-serif;font-size:13px;padding:8px;background:#FFFFFF;border-radius:6px;border-left:4px solid " & BarColor & ";'>" &
"<b>Efetividade Visitas</b><br>" &
UPPER(NomeM0) & " " & FORMAT(vM0, "0.0%") & " → " &
UPPER(NomeM1) & " " & FORMAT(vM1, "0.0%") &
" <span style='color:" & IconColor & ";font-weight:700;'>" & Icon & " " & FORMAT(vPerc, "0.0%") & "</span>" &
"<div style='background:#F3F2F1;border-radius:4px;height:8px;margin-top:6px;'><div style='background:" & BarColor & ";width:" & BarWidth & "%;height:8px;border-radius:4px;'></div></div></div>"
```

---

## 5. !Resumo Geral Mês (HTML) — REESCRITO COMPLETO

```dax
VAR Rede = FIRSTNONBLANK('dim_rede'[nm_rede], "Todas")
VAR VendaQtd = [Venda (Qtd.) M-1]
VAR RuptCom = [% Ruptura Comercial (Qtd.) Rede]
VAR RuptOp = [% Ruptura Operacional (Qtd.) Rede]
VAR Efetiv = [%VISITAS]
VAR Lojas = [Lojas Cadastradas no Projeto]
VAR LojasVenda = [Lojas com venda no Projeto M-1]
VAR Horas = [Horas Realizadas (Projeto)]
VAR HorasIdeais = [Horas Ideais]
VAR PctHoras = DIVIDE(Horas, HorasIdeais)
VAR CorVenda = IF(VendaQtd > 0, "#107C41", "#434343")
VAR CorRuptCom = IF(RuptCom > 0.3, "#C00000", IF(RuptCom > 0.1, "#F46901", "#107C41"))
VAR CorRuptOp = IF(RuptOp > 0.5, "#C00000", IF(RuptOp > 0.2, "#F46901", "#107C41"))
VAR CorEfetiv = IF(Efetiv >= 0.8, "#107C41", IF(Efetiv >= 0.6, "#F46901", "#C00000"))
VAR CorHoras = IF(PctHoras >= 0.5, "#107C41", "#C00000")
RETURN
"<div style='font-family:Raleway,sans-serif;font-size:12px;line-height:20px;background:#FFFFFF;border:1px solid #F3F2F1;border-radius:8px;padding:12px;'>" &
"<div style='font-size:14px;font-weight:800;color:#111111;border-bottom:2px solid #F46901;padding-bottom:4px;margin-bottom:8px;'>RESUMO " & UPPER(Rede) & "</div>" &
"💰 <b>Vendas:</b> <span style='color:" & CorVenda & ";font-weight:700;'>" & FORMAT(VendaQtd, "#,##0") & " un.</span><br>" &
"🛒 <b>Rupt. Comercial:</b> <span style='color:" & CorRuptCom & ";font-weight:700;'>" & FORMAT(RuptCom, "0.0%") & "</span><br>" &
"⚙️ <b>Rupt. Operacional:</b> <span style='color:" & CorRuptOp & ";font-weight:700;'>" & FORMAT(RuptOp, "0.0%") & "</span><br>" &
"✅ <b>Efetividade:</b> <span style='color:" & CorEfetiv & ";font-weight:700;'>" & FORMAT(Efetiv, "0.0%") & "</span><br>" &
"🏬 <b>Lojas:</b> " & FORMAT(LojasVenda, "#,0") & "/" & FORMAT(Lojas, "#,0") & "<br>" &
"⏱️ <b>Horas:</b> <span style='color:" & CorHoras & ";'>" & FORMAT(Horas, "#,0") & "h / " & FORMAT(HorasIdeais, "#,0") & "h (" & FORMAT(PctHoras, "0%") & ")</span>" &
"<div style='background:#F3F2F1;border-radius:4px;height:6px;margin-top:6px;'><div style='background:" & CorHoras & ";width:" & ROUND(PctHoras * 100, 0) & "%;height:6px;border-radius:4px;'></div></div></div>"
```

---

## 6. !Alerta GAP Horas (HTML) — NOVA MEDIDA

```dax
VAR Horas = [Horas Realizadas (Projeto)]
VAR HorasIdeais = [Horas Ideais]
VAR GAP = HorasIdeais - Horas
VAR PctExec = DIVIDE(Horas, HorasIdeais)
VAR BarColor = IF(PctExec >= 0.5, "#107C41", IF(PctExec >= 0.2, "#F46901", "#C00000"))
RETURN
"<div style='font-family:Raleway,sans-serif;font-size:12px;padding:10px;background:#FFF5F5;border:1px solid #C00000;border-radius:8px;'>" &
"<div style='font-weight:800;color:#C00000;font-size:13px;'>🚨 ALERTA: GAP DE HORAS</div>" &
"<div style='margin-top:6px;'>Executado: <b>" & FORMAT(Horas, "#,0") & "h</b> de " & FORMAT(HorasIdeais, "#,0") & "h (" & FORMAT(PctExec, "0.0%") & ")</div>" &
"<div style='color:#C00000;font-weight:700;'>GAP: -" & FORMAT(GAP, "#,0") & "h</div>" &
"<div style='background:#F3F2F1;border-radius:4px;height:10px;margin-top:8px;'><div style='background:" & BarColor & ";width:" & ROUND(PctExec * 100, 0) & "%;height:10px;border-radius:4px;'></div></div></div>"
```

---

## Como aplicar

Quando reabrir o Power BI Desktop:
1. Conecte via MCP (vai reconectar automaticamente)
2. Cole: "Aplica as medidas HTML do arquivo MEDIDAS_HTML_CORRIGIDAS.md"
3. Ou copie cada DAX manualmente no editor de medidas

## CSS equivalente (para referência)

```css
/* Mob2Con Brand - Design Tokens aplicados no HTML inline */
:root {
  --mob-orange: #F46901;
  --mob-green: #107C41;
  --mob-red: #C00000;
  --mob-dark: #111111;
  --mob-gray: #434343;
  --mob-bg: #F3F2F1;
  --mob-white: #FFFFFF;
  --mob-font: 'Raleway', sans-serif;
}
```
