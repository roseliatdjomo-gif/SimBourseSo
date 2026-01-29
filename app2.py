import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- 1. CONFIGURATION & DESIGN (Ton arme de persuasion) ---
st.set_page_config(page_title="CAC40 Intelligence Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; }
    div[data-testid="column"] {
        background: linear-gradient(145deg, #111111, #1a1a1a);
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    div[data-testid="column"]:hover {
        transform: translateY(-5px);
        border-color: #00ffcc;
        box-shadow: 0 10px 20px rgba(0, 255, 204, 0.2);
    }
    h3 { color: #00ffcc !important; font-weight: bold; font-size: 1.2rem; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800; }
    .stMetric { background-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES (Secteurs Fixes & Événements) ---
SECTEURS = {
    "AC.PA": "Hôtellerie (Accor)", "AI.PA": "Industrie (Air Liquide)", "AIR.PA": "Aéronautique (Airbus)",
    "MT.PA": "Sidérurgie (ArcelorMittal)", "CS.PA": "Assurance (AXA)", "BNP.PA": "Banque (BNP Paribas)",
    "EN.PA": "BTP (Bouygues)", "BVI.PA": "Certification (Bureau Veritas)", "CAP.PA": "Services IT (Capgemini)",
    "CA.PA": "Distribution (Carrefour)", "ACA.PA": "Banque (Crédit Agricole)", "BN.PA": "Agroalimentaire (Danone)",
    "DSY.PA": "Logiciels (Dassault Systèmes)", "FGR.PA": "Eiffage", "ENGI.PA": "Énergie (Engie)",
    "EL.PA": "Optique (EssilorLuxottica)", "ERF.PA": "Biotech (Eurofins)", "ENX.PA": "Bourse (Euronext)",
    "RMS.PA": "Luxe (Hermès)", "KER.PA": "Luxe (Kering)", "OR.PA": "Cosmétique (L'Oréal)",
    "LR.PA": "Électricité (Legrand)", "MC.PA": "Luxe (LVMH)", "ML.PA": "Pneumatiques (Michelin)",
    "ORA.PA": "Télécoms (Orange)", "RI.PA": "Spiritueux (Pernod Ricard)", "PUB.PA": "Publicité (Publicis)",
    "SAF.PA": "Aéronautique (Safran)", "SGO.PA": "Matériaux (Saint-Gobain)", "SAN.PA": "Santé (Sanofi)",
    "SU.PA": "Énergie (Schneider Electric)", "GLE.PA": "Banque (Société Générale)", "STLAP.PA": "Auto (Stellantis)",
    "STMPA.PA": "Semi-conducteurs (STMicro)", "TEP.PA": "Télémarketing (Teleperformance)", "HO.PA": "Défense (Thales)",
    "TTE.PA": "Énergie (TotalEnergies)", "VIE.PA": "Environnement (Veolia)", "DG.PA": "BTP (Vinci)", "WLN.PA": "Paiements (Worldline)"
}

evenements = {
    "MC.PA": {"1y": "Hausse record au S1, ralentissement chinois au S2.", "6mo": "Correction suite aux taux d'intérêt."},
    "TTE.PA": {"1y": "Impacté par la volatilité du prix du baril.", "6mo": "Forte distribution de dividendes."},
    "OR.PA": {"1y": "Croissance portée par l'innovation dermatologique.", "6mo": "Résistance à l'inflation."}
}

@st.cache_data
def get_stock_data(ticker, p):
    return yf.download(ticker, period=p, progress=False)

# --- 3. INTERFACE DE COMMANDE ---
st.title("🏛️ CAC 40 Intelligence - Direction Générale")

col_a, col_b = st.columns([1, 2])
with col_a:
    action_detail = st.selectbox("🎯 Sélectionnez une cible :", list(SECTEURS.keys()))
with col_b:
    periode = st.radio("⏳ Période d'analyse :", ["1mo", "6mo", "1y"], horizontal=True)

# Graphique Central
data_plot = get_stock_data(action_detail, periode)
if not data_plot.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_plot.index, y=data_plot['Close'], line=dict(color='#00ffcc', width=3), name='Cours'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig, use_container_width=True)

# Rapport d'expertise
with st.expander("🔍 Rapport d'Analyse des Variations"):
    rapport = evenements.get(action_detail, {}).get(periode, "Analyse technique : La valeur suit les tendances macro-économiques du secteur.")
    st.info(rapport)

st.markdown("---")

# --- 4. LA GRILLE LIVE ---
st.subheader("📡 État du Marché en Temps Réel")
cols = st.columns(4)
for i, ticker in enumerate(SECTEURS.keys()):
    try:
        df = get_stock_data(ticker, "1mo")
        if df.empty: continue
        
        prix = round(df['Close'].iloc[-1], 2)
        moyenne = round(df['Close'].mean(), 2)
        
        with cols[i % 4]:
            st.write(f"### {ticker}")
            conseil = "🟢 ACHAT" if prix < moyenne else "⚪ ATTENTE"
            st.metric(SECTEURS[ticker], f"{prix} €", delta=conseil)
            st.line_chart(df['Close'], height=80)
    except:
        continue
