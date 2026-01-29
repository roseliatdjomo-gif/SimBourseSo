import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- 1. DESIGN "PRESTIGE" ---
st.set_page_config(page_title="CAC 40 Intelligence - Roselia CEO Edition", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    div[data-testid="column"] {
        background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
        border: 1px solid #222;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    div[data-testid="column"]:hover {
        border-color: #00ffcc;
        transform: translateY(-3px);
    }
    h3 { color: #00ffcc !important; font-family: 'Georgia', serif; font-size: 1.1rem; margin-bottom: 0px;}
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.5rem; }
    .stInfo { background-color: #111; border: 1px solid #00ffcc; color: #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LA GRANDE BASE DE DONNÉES CLASSÉE PAR PUISSANCE ---
ENTREPRISES = {
    "MC.PA": {"nom": "LVMH", "sect": "Luxe", "creation": "1987", "ceo": "Bernard Arnault", "bio": "Premier groupe de luxe mondial."},
    "OR.PA": {"nom": "L'Oréal", "sect": "Cosmétique", "creation": "1909", "ceo": "Nicolas Hieronimus", "bio": "Leader mondial de la beauté."},
    "RMS.PA": {"nom": "Hermès", "sect": "Luxe", "creation": "1837", "ceo": "Axel Dumas", "bio": "Excellence artisanale française."},
    "TTE.PA": {"nom": "TotalEnergies", "sect": "Énergie", "creation": "1924", "ceo": "Patrick Pouyanné", "bio": "Géant mondial de l'énergie."},
    "SAN.PA": {"nom": "Sanofi", "sect": "Santé", "creation": "1973", "ceo": "Paul Hudson", "bio": "Leader de la santé humaine."},
    "AIR.PA": {"nom": "Airbus", "sect": "Aéronautique", "creation": "1970", "ceo": "Guillaume Faury", "bio": "Leader de l'aviation civile."},
    "SU.PA": {"nom": "Schneider Electric", "sect": "Énergie", "creation": "1836", "ceo": "Peter Herweck", "bio": "Gestion de l'énergie numérique."},
    "AI.PA": {"nom": "Air Liquide", "sect": "Industrie", "creation": "1902", "ceo": "François Jackow", "bio": "Gaz industriels et santé."},
    "BNP.PA": {"nom": "BNP Paribas", "sect": "Banque", "creation": "1966", "ceo": "Jean-Laurent Bonnafé", "bio": "1ère banque de la zone Euro."},
    "EL.PA": {"nom": "EssilorLuxottica", "sect": "Optique", "creation": "2018", "ceo": "Francesco Milleri", "bio": "Leader mondial de l'optique."},
    "DG.PA": {"nom": "Vinci", "sect": "BTP", "creation": "1899", "ceo": "Xavier Huillard", "bio": "Concessions et construction mondiale."},
    "SAF.PA": {"nom": "Safran", "sect": "Aéronautique", "creation": "2005", "ceo": "Olivier Andriès", "bio": "Moteurs d'avions et défense."},
    "STLAP.PA": {"nom": "Stellantis", "sect": "Auto", "creation": "2021", "ceo": "Carlos Tavares", "bio": "Géant de l'automobile mondiale."},
    "DSY.PA": {"nom": "Dassault Systèmes", "sect": "Logiciels", "creation": "1981", "ceo": "Bernard Charlès", "bio": "Logiciels de simulation 3D."},
    "KER.PA": {"nom": "Kering", "sect": "Luxe", "creation": "1963", "ceo": "François-Henri Pinault", "bio": "Propriétaire de Gucci et Yves Saint Laurent."},
    "CS.PA": {"nom": "AXA", "sect": "Assurance", "creation": "1817", "ceo": "Thomas Buberl", "bio": "Leader mondial de l'assurance."},
    "SGO.PA": {"nom": "Saint-Gobain", "sect": "Matériaux", "creation": "1665", "ceo": "Benoît Bazin", "bio": "Habitat durable et construction."},
    "STMPA.PA": {"nom": "STMicroelectronics", "sect": "Semi-cond.", "creation": "1987", "ceo": "Jean-Marc Chéry", "bio": "Électronique pour l'auto et l'industrie."},
    "BN.PA": {"nom": "Danone", "sect": "Agroalimentaire", "creation": "1919", "ceo": "Antoine de Saint-Affrique", "bio": "Nutrition et produits laitiers."},
    "CAP.PA": {"nom": "Capgemini", "sect": "IT", "creation": "1967", "ceo": "Aiman Ezzat", "bio": "Conseil et services numériques."},
    "HO.PA": {"nom": "Thales", "sect": "Défense", "creation": "1893", "ceo": "Patrice Caine", "bio": "Défense et identité numérique."},
    "ENGI.PA": {"nom": "Engie", "sect": "Énergie", "creation": "2008", "ceo": "Catherine MacGregor", "bio": "Transition bas carbone et gaz."},
    "VIE.PA": {"nom": "Veolia", "sect": "Environnement", "creation": "1853", "ceo": "Estelle Brachlianoff", "bio": "Gestion de l'eau et des déchets."},
    "RI.PA": {"nom": "Pernod Ricard", "sect": "Spiritueux", "creation": "1975", "ceo": "Alexandre Ricard", "bio": "Vins et spiritueux premium."},
    "ACA.PA": {"nom": "Crédit Agricole", "sect": "Banque", "creation": "1885", "ceo": "Philippe Brassac", "bio": "Banque de détail internationale."},
    "PUB.PA": {"nom": "Publicis", "sect": "Publicité", "creation": "1926", "ceo": "Arthur Sadoun", "bio": "Marketing et communication data."},
    "ORA.PA": {"nom": "Orange", "sect": "Télécoms", "creation": "1988", "ceo": "Christel Heydemann", "bio": "Opérateur télécom leader."},
    "ML.PA": {"nom": "Michelin", "sect": "Pneus", "creation": "1889", "ceo": "Florent Menegaux", "bio": "Manufacture de pneumatiques."},
    "MT.PA": {"nom": "ArcelorMittal", "sect": "Acier", "creation": "2006", "ceo": "Aditya Mittal", "bio": "Leader mondial de la sidérurgie."},
    "GLE.PA": {"nom": "Société Générale", "sect": "Banque", "creation": "1864", "ceo": "Slawomir Krupa", "bio": "Services bancaires internationaux."},
    "CA.PA": {"nom": "Carrefour", "sect": "Distribution", "creation": "1959", "ceo": "Alexandre Bompard", "bio": "Commerce alimentaire mondial."},
    "EN.PA": {"nom": "Bouygues", "sect": "BTP/Médias", "creation": "1952", "ceo": "Olivier Roussat", "bio": "BTP, Télécoms et Médias (TF1)."},
    "LR.PA": {"nom": "Legrand", "sect": "Électricité", "creation": "1865", "ceo": "Benoît Coquart", "bio": "Infrastructures électriques."},
    "FGR.PA": {"nom": "Eiffage", "sect": "BTP", "creation": "1992", "ceo": "Benoît de Ruffray", "bio": "Construction et concessions."},
    "BVI.PA": {"nom": "Bureau Veritas", "sect": "Certification", "creation": "1828", "ceo": "Hinda Gharbi", "bio": "Certification et inspection."},
    "AC.PA": {"nom": "Accor", "sect": "Hôtellerie", "creation": "1967", "ceo": "Sébastien Bazin", "bio": "Groupe hôtelier international."},
    "TEP.PA": {"nom": "Teleperformance", "sect": "Services", "creation": "1978", "ceo": "Daniel Julien", "bio": "Relation client externalisée."},
    "ENX.PA": {"nom": "Euronext", "sect": "Finance", "creation": "2000", "ceo": "Stéphane Boujnah", "bio": "Gestionnaire boursier européen."},
    "ERF.PA": {"nom": "Eurofins", "sect": "Biotech", "creation": "1987", "ceo": "Gilles Martin", "bio": "Analyses biologiques."},
    "WLN.PA": {"nom": "Worldline", "sect": "Paiements", "creation": "1972", "ceo": "Marc-Henri Desportes", "bio": "Paiements électroniques."}
}

# --- 3. LOGIQUE & FONCTIONS ---
@st.cache_data
def load_data(ticker, p):
    return yf.download(ticker, period=p, progress=False)

# --- 4. INTERFACE ---
st.title("🏛️ CAC 40 Intelligence - Roselia CEO Edition")

c1, c2 = st.columns([1, 1])
with c1:
    action_target = st.selectbox("🎯 Choisir une cible stratégique :", list(ENTREPRISES.keys()))
with c2:
    periode = st.radio("⏳ Observation :", ["1mo", "6mo", "1y"], horizontal=True)

# Graphique
data = load_data(action_target, periode)
if not data.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], line=dict(color='#00ffcc', width=3), name='Cours'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig, use_container_width=True)

# Fiche Identité
info = ENTREPRISES[action_target]
st.info(f"**Société :** {info['nom']} | **CEO :** {info['ceo']} | **Création :** {info['creation']} \n\n **Résumé :** {info['bio']}")

st.markdown("---")

# --- 5. GRILLE LIVE ---
st.subheader("📡 État Global du Marché (Par Capitalisation)")
cols = st.columns(4)
for i, (ticker, details) in enumerate(ENTREPRISES.items()):
    try:
        df = load_data(ticker, "1mo")
        if df.empty: continue
        prix = round(df['Close'].iloc[-1], 2)
        moyenne = round(df['Close'].mean(), 2)
        
        with cols[i % 4]:
            st.write(f"### {details['nom']}")
            signal = "🟢 ACHAT" if prix < moyenne else "⚪ ATTENTE"
            st.metric(details['sect'], f"{prix} €", delta=signal)
            st.line_chart(df['Close'], height=60)
    except:
        continue
