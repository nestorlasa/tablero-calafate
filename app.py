import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página para que ocupe todo el ancho
st.set_page_config(page_title="Tablero PEM - El Calafate", layout="wide")

st.title("📊 Actualizador de Tablero Comercial")
st.write("Sucursal 1697 - El Calafate")

# Zona para subir el PDF
archivo_pdf = st.file_uploader("Arrastrá aquí el informe PDF mensual del PEM", type="pdf")

if archivo_pdf is not None:
    st.success(f"¡Archivo '{archivo_pdf.name}' procesado! (En la próxima versión la IA leerá los datos reales)")
    st.markdown("---")
    
    # Aquí está el diseño de tu tablero simétrico y adaptativo
    html_tablero = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root { --bg-main: #f0f4f8; --bg-panel: #ffffff; --text-main: #1e293b; --text-muted: #64748b; --red: #ef4444; --green: #10b981; --yellow: #f59e0b; --blue: #2563eb; --border: #e2e8f0; }
            * { box-sizing: border-box; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
            body { background-color: var(--bg-main); color: var(--text-main); margin: 0; padding: 15px; font-size: 14px; }
            .header { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .header h1 { margin: 0; font-size: 20px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #ffffff;}
            .header .badge { background: rgba(255, 255, 255, 0.2); color: #ffffff; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: 500;}
            .section-title { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; display: flex; align-items: center; gap: 5px; font-weight: 700; }
            .section-title::before { content: '>'; color: var(--blue); }
            .alerts-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }
            .alert-card { background-color: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 15px; position: relative; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
            .alert-card.critical { border-top: 4px solid var(--red); }
            .alert-card.success { border-top: 4px solid var(--green); }
            .alert-title { font-size: 12px; font-weight: bold; margin-bottom: 5px; display: flex; justify-content: space-between;}
            .alert-val { font-size: 28px; font-weight: bold; margin-bottom: 5px; }
            .alert-desc { font-size: 11px; color: var(--text-muted); line-height: 1.4;}
            .text-red { color: #dc2626; } .text-green { color: #059669; } .text-blue { color: var(--blue); }
            .middle-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
            .panel { background-color: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 20px 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
            .bar-row { display: flex; align-items: center; margin-bottom: 16px; }
            .bar-label { width: 140px; font-size: 13px; font-weight: 600; color: var(--text-main); }
            .bar-track { flex-grow: 1; background-color: #f1f5f9; height: 12px; border-radius: 6px; margin: 0 15px; overflow: hidden; border: 1px solid #e2e8f0; }
            .bar-fill { height: 100%; border-radius: 5px; }
            .bar-fill.red { background-color: var(--red); } .bar-fill.green { background-color: var(--green); }
            .bar-percent { width: 55px; text-align: right; font-weight: bold; font-size: 14px; }
            .cond-item-wrapper { border-bottom: 1px solid var(--border); padding: 10px 0; }
            .cond-item-wrapper:last-child { border-bottom: none; padding-bottom: 0;}
            .cond-header { display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; margin-bottom: 8px; color: var(--text-main); }
            .cond-grid { display: grid; grid-template-columns: repeat(4, 1fr); background-color: #f8fafc; padding: 8px 12px; border-radius: 6px; border-left: 3px solid #cbd5e1; }
            .cond-grid div { display: flex; flex-direction: column; font-size: 13px; font-weight: 600; }
            .cond-grid span { font-size: 10px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 2px; font-weight: 700; }
            .cond-icon { display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 50%; font-size: 10px; margin-right: 8px; font-weight: bold; }
            .icon-red { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5;}
            table { width: 100%; border-collapse: collapse; font-size: 13px; }
            th { background-color: #f8fafc; color: var(--text-muted); text-align: left; padding: 12px 10px; font-weight: 700; text-transform: uppercase; border-bottom: 2px solid var(--border); }
            td { padding: 12px 10px; border-bottom: 1px solid var(--border); color: var(--text-main); }
            tr:hover { background-color: #f1f5f9; }
            .status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
            .bg-red { background-color: var(--red); } .bg-green { background-color: var(--green); }
            @media (max-width: 900px) { .alerts-grid { grid-template-columns: 1fr; } .middle-grid { grid-template-columns: 1fr; } .cond-grid { grid-template-columns: 1fr 1fr; gap: 10px;} .bar-row { flex-wrap: wrap; } .bar-label { width: 100%; margin-bottom: 5px; } .bar-track { margin: 0 10px 0 0; } }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>SUCURSAL 1697 - EL CALAFATE | REPORTE DE GESTIÓN PEM 2026</h1>
            <div class="badge">Provincia: Santa Cruz | Corte: 03-Jun-26</div>
        </div>
        <div class="section-title">PANEL DE ALERTAS - DESVÍOS E INCUMPLIMIENTOS TRAMO 3</div>
        <div class="alerts-grid">
            <div class="alert-card critical">
                <div class="alert-title text-red"><span>V4 BC USD - CRÍTICO</span></div>
                <div class="alert-val text-red">25.01%</div>
                <div class="alert-desc">Ejecutado: 22k USD vs 88k USD proyectado. Foco en operaciones de comercio exterior.</div>
            </div>
            <div class="alert-card success">
                <div class="alert-title text-green"><span>V6 SERVICIOS - ALCANZADA</span></div>
                <div class="alert-val text-green">101.48%</div>
                <div class="alert-desc">Riesgo revertido. Ejecutado $333M vs $328M proyectado.</div>
            </div>
            <div class="alert-card success">
                <div class="alert-title text-green"><span>V3 BC $ - DESTACADO</span></div>
                <div class="alert-val text-green">200.43%</div>
                <div class="alert-desc">Excelente desempeño. Ejecutado $2.639M vs $1.317M proyectado.</div>
            </div>
            <div class="alert-card critical">
                <div class="alert-title text-red"><span>T3 CONDICIONES - BLOQUEO</span></div>
                <div class="alert-val text-red">-50.0%</div>
                <div class="alert-desc">Leve mejora en Ctas. Ctes, pero se mantiene la pérdida neta. Bloquea estímulos.</div>
            </div>
        </div>
        <div class="middle-grid">
            <div class="panel">
                <div class="section-title">SEMÁFORO VARIABLES PEM</div>
                <div class="bar-row"><div class="bar-label"><span class="status-dot bg-green"></span>V1 - Dep. Pesos SPR</div><div class="bar-track"><div class="bar-fill green" style="width: 100%;"></div></div><div class="bar-percent text-green">113.4%</div></div>
                <div class="bar-row"><div class="bar-label"><span class="status-dot bg-green"></span>V2 - Dep. USD</div><div class="bar-track"><div class="bar-fill green" style="width: 100%;"></div></div><div class="bar-percent text-green">352.0%</div></div>
                <div class="bar-row"><div class="bar-label"><span class="status-dot bg-green"></span>V3 - Banca Com. $</div><div class="bar-track"><div class="bar-fill green" style="width: 100%;"></div></div><div class="bar-percent text-green">200.4%</div></div>
                <div class="bar-row"><div class="bar-label"><span class="status-dot bg-red"></span>V4 - BC USD</div><div class="bar-track"><div class="bar-fill red" style="width: 25.01%;"></div></div><div class="bar-percent text-red">25.0%</div></div>
                <div class="bar-row"><div class="bar-label"><span class="status-dot bg-green"></span>V6 - Ing. Servicios</div><div class="bar-track"><div class="bar-fill green" style="width: 100%;"></div></div><div class="bar-percent text-green">101.5%</div></div>
            </div>
            <div class="panel">
                <div class="section-title">CONDICIONANTES TRAMO 3 - CANTIDADES REALES</div>
                <div class="cond-item-wrapper">
                    <div class="cond-header"><div><span class="cond-icon icon-red">X</span> Clientes Financian (Banca Com.)</div><div class="text-red">-33.3%</div></div>
                    <div class="cond-grid"><div><span>Base Dic '25</span> 103</div><div><span>Actual</span> 102 <small class="text-red">(-1)</small></div><div><span>Meta</span> 106 <small class="text-blue">(+3)</small></div><div><span>Faltan</span> <span class="text-red">4 clientes</span></div></div>
                </div>
                <div class="cond-item-wrapper">
                    <div class="cond-header"><div><span class="cond-icon icon-red">X</span> Cuentas Corrientes Comerciales</div><div class="text-red">-50.0%</div></div>
                    <div class="cond-grid"><div><span>Base Dic '25</span> 274</div><div><span>Actual</span> 266 <small class="text-red">(-8)</small></div><div><span>Meta</span> 290 <small class="text-blue">(+16)</small></div><div><span>Faltan</span> <span class="text-red">24 ctas.</span></div></div>
                </div>
                <div class="cond-item-wrapper">
                    <div class="cond-header"><div><span class="cond-icon icon-red">X</span> Tarjetas de Crédito Indiv.</div><div class="text-red">-36.0%</div></div>
                    <div class="cond-grid"><div><span>Base Dic '25</span> 4.276</div><div><span>Actual</span> 4.191 <small class="text-red">(-85)</small></div><div><span>Meta</span> 4.512 <small class="text-blue">(+236)</small></div><div><span>Faltan</span> <span class="text-red">321 tarj.</span></div></div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    components.html(html_tablero, height=750, scrolling=True)
else:
    st.info("Esperando archivo... Por favor, subí un PDF para ver el tablero.")
