import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Tablero PEM - El Calafate", layout="wide")

# 1. EL CARGADOR DE ARCHIVOS AHORA ESTÁ ESCONDIDO EN EL PANEL LATERAL
with st.sidebar:
    st.title("⚙️ Generador de Tablero")
    st.write("Arrastrá el PDF del mes aquí para actualizar los datos.")
    archivo_pdf = st.file_uploader("", type="pdf")
    st.markdown("---")
    st.write("ℹ️ *Este panel es solo para vos. Tus compañeros verán el reporte limpio que descargues.*")

st.title("📊 Actualizador de Tablero Comercial - Sucursal 1697")

if archivo_pdf is not None:
    st.success(f"✅ Archivo procesado correctamente. ¡Tablero generado!")
    
    # 2. EL HTML COMPLETO (CON LA TABLA RESTAURADA Y ADAPTADO A CELULARES)
    html_tablero = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Gesti&oacute;n PEM 2026</title>
        <style>
            :root { --bg-main: #f0f4f8; --bg-panel: #ffffff; --text-main: #1e293b; --text-muted: #64748b; --red: #ef4444; --green: #10b981; --yellow: #f59e0b; --blue: #2563eb; --border: #e2e8f0; }
            * { box-sizing: border-box; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
            body { background-color: var(--bg-main); color: var(--text-main); margin: 0; padding: 15px; font-size: 14px; }
            .header { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 15px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex-wrap: wrap; gap: 10px;}
            .header h1 { margin: 0; font-size: 18px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #ffffff;}
            .header .badge { background: rgba(255, 255, 255, 0.2); color: #ffffff; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: 500;}
            .section-title { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; display: flex; align-items: center; gap: 5px; font-weight: 700; }
            .section-title::before { content: '>'; color: var(--blue); }
            .alerts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 15px; margin-bottom: 20px; }
            .alert-card { background-color: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
            .alert-card.critical { border-top: 4px solid var(--red); }
            .alert-card.success { border-top: 4px solid var(--green); }
            .alert-title { font-size: 12px; font-weight: bold; margin-bottom: 5px; display: flex; justify-content: space-between;}
            .alert-val { font-size: 26px; font-weight: bold; margin-bottom: 5px; }
            .alert-desc { font-size: 11px; color: var(--text-muted); line-height: 1.4;}
            .text-red { color: #dc2626; } .text-green { color: #059669; } .text-blue { color: var(--blue); }
            .middle-grid { display: grid; grid-template-columns: 1.6fr 1.2fr; gap: 20px; margin-bottom: 20px; }
            .panel { background-color: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 20px 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); overflow: hidden;}
            .bar-row { display: flex; align-items: center; margin-bottom: 16px; }
            .bar-label { width: 140px; font-size: 13px; font-weight: 600; color: var(--text-main); }
            .bar-track { flex-grow: 1; background-color: #f1f5f9; height: 12px; border-radius: 6px; margin: 0 15px; overflow: hidden; border: 1px solid #e2e8f0; }
            .bar-fill { height: 100%; border-radius: 5px; }
            .bar-fill.red { background-color: var(--red); } .bar-fill.green { background-color: var(--green); }
            .bar-percent { width: 55px; text-align: right; font-weight: bold; font-size: 14px; }
            .cond-item-wrapper { border-bottom: 1px solid var(--border); padding: 12px 0; }
            .cond-item-wrapper:last-child { border-bottom: none; padding-bottom: 0;}
            .cond-header { display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; margin-bottom: 8px; color: var(--text-main); }
            .cond-grid { display: grid; grid-template-columns: repeat(4, 1fr); background-color: #f8fafc; padding: 8px 12px; border-radius: 6px; border-left: 3px solid #cbd5e1; gap: 10px;}
            .cond-grid div { display: flex; flex-direction: column; font-size: 13px; font-weight: 600; }
            .cond-grid span { font-size: 10px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 2px; font-weight: 700; }
            .cond-icon { display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 50%; font-size: 10px; margin-right: 8px; font-weight: bold; }
            .icon-red { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5;}
            .table-responsive { width: 100%; overflow-x: auto; }
            table { width: 100%; min-width: 600px; border-collapse: collapse; font-size: 13px; }
            th { background-color: #f8fafc; color: var(--text-muted); text-align: left; padding: 12px 10px; font-weight: 700; text-transform: uppercase; border-bottom: 2px solid var(--border); }
            td { padding: 12px 10px; border-bottom: 1px solid var(--border); color: var(--text-main); }
            tr:hover { background-color: #f1f5f9; }
            .status-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }
            .bg-red { background-color: var(--red); } .bg-green { background-color: var(--green); }
            @media (max-width: 900px) { .middle-grid { grid-template-columns: 1fr; } .cond-grid { grid-template-columns: 1fr 1fr; } .bar-row { flex-wrap: wrap; } .bar-label { width: 100%; margin-bottom: 5px; } .bar-track { margin: 0 10px 0 0; } }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>SUCURSAL 1697 - EL CALAFATE | REPORTE DE GESTIÓN</h1>
            <div class="badge">Corte: 03-Jun-26</div>
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
                    <div class="cond-header"><div><span class="cond-icon icon-red">X</span> Clientes Financian</div><div class="text-red">-33.3%</div></div>
                    <div class="cond-grid"><div><span>Base Dic '25</span> 103</div><div><span>Actual</span> 102 <small class="text-red">(-1)</small></div><div><span>Meta</span> 106 <small class="text-blue">(+3)</small></div><div><span>Faltan</span> <span class="text-red">4 cl.</span></div></div>
                </div>
                <div class="cond-item-wrapper">
                    <div class="cond-header"><div><span class="cond-icon icon-red">X</span> Ctas. Ctes. Comerciales</div><div class="text-red">-50.0%</div></div>
                    <div class="cond-grid"><div><span>Base Dic '25</span> 274</div><div><span>Actual</span> 266 <small class="text-red">(-8)</small></div><div><span>Meta</span> 290 <small class="text-blue">(+16)</small></div><div><span>Faltan</span> <span class="text-red">24 ct.</span></div></div>
                </div>
                <div class="cond-item-wrapper">
                    <div class="cond-header"><div><span class="cond-icon icon-red">X</span> Tarjetas de Crédito</div><div class="text-red">-36.0%</div></div>
                    <div class="cond-grid"><div><span>Base Dic '25</span> 4.276</div><div><span>Actual</span> 4.191 <small class="text-red">(-85)</small></div><div><span>Meta</span> 4.512 <small class="text-blue">(+236)</small></div><div><span>Faltan</span> <span class="text-red">321 tj.</span></div></div>
                </div>
            </div>
        </div>
        <div class="panel">
            <div class="section-title">DETALLE EJECUTIVO PEM - CIFRAS EN MILES</div>
            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>Variable de Medición</th>
                            <th>Proyectado (Meta)</th>
                            <th>Ejecutado (Real)</th>
                            <th>Diferencia Absoluta</th>
                            <th>% Cumplimiento</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>V1 - Dep. Com. Pesos SPR</strong></td><td>$ 2.164.672</td><td>$ 2.455.137</td><td class="text-green">+ $ 290.465</td><td class="text-green"><strong>113.42%</strong></td><td><span class="status-dot bg-green"></span> Superado</td></tr>
                        <tr><td><strong>V2 - Dep. Com. ME (USD)</strong></td><td>USD 350</td><td>USD 1.233</td><td class="text-green">+ USD 883</td><td class="text-green"><strong>351.98%</strong></td><td><span class="status-dot bg-green"></span> Superado</td></tr>
                        <tr><td><strong>V3 - Banca Comercial en Pesos</strong></td><td>$ 1.317.136</td><td>$ 2.639.917</td><td class="text-green">+ $ 1.322.781</td><td class="text-green"><strong>200.43%</strong></td><td><span class="status-dot bg-green"></span> Destacado</td></tr>
                        <tr><td><strong>V4 - Banca Comercial ME (USD)</strong></td><td>USD 88</td><td>USD 22</td><td class="text-red">- USD 66</td><td class="text-red"><strong>25.01%</strong></td><td><span class="status-dot bg-red"></span> Crítico</td></tr>
                        <tr><td><strong>V6 - Ingresos por Servicios</strong></td><td>$ 328.589</td><td>$ 333.467</td><td class="text-green">+ $ 4.877</td><td class="text-green"><strong>101.48%</strong></td><td><span class="status-dot bg-green"></span> Superado</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    # 3. EL NUEVO BOTÓN PARA DESCARGAR (Fácil para compartir)
    st.download_button(
        label="📥 Descargar Reporte Listo (Para enviar por WhatsApp/Mail)",
        data=html_tablero,
        file_name="Reporte_PEM_Calafate.html",
        mime="text/html"
    )
    
    st.markdown("---")
    
    # Renderizado del tablero con altura completa
    components.html(html_tablero, height=1100, scrolling=True)

else:
    st.info("👈 Esperando informe... Subí el PDF en el panel de la izquierda para comenzar.")
