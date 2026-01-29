import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="CAC 40 - Roselia Capital", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    div[data-testid="column"] {
        background: #111;
        border: 1px solid #222;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    div[data-testid="column"]:hover { border-color: #00ffcc; }
    h3 { color: #00ffcc !important; font-size: 1.1rem; margin-bottom: 0px; }
    .stMetricValue { font-size: 1.3rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LA BASE COMPLÈTE (40 Entreprises) ---
ENTREPRISES = {
    "MC.PA": {"nom": "LVMH", "sect": "Luxe", "ceo": "Bernard Arnault", "crea": "1987"},
    "OR.PA": {"nom": "L'Oréal", "sect": "Cosmétique", "ceo": "Nicolas Hieronimus", "crea": "1909"},
    "RMS.PA": {"nom": "Hermès", "sect": "Luxe", "ceo": "Axel Dumas", "crea": "1837"},
    "TTE.PA": {"nom": "TotalEnergies", "sect": "Énergie", "ceo": "Patrick Pouyanné", "crea": "1924"},
    "SAN.PA": {"nom": "Sanofi", "sect": "Santé", "ceo": "Paul Hudson", "crea": "1973"},
    "AIR.PA": {"nom": "Airbus", "sect": "Aéro", "ceo": "Guillaume Faury", "crea": "1970"},
    "SU.PA": {"nom": "Schneider Electric", "sect": "Énergie", "ceo": "Peter Herweck", "crea": "1836"},
    "AI.PA": {"nom": "Air Liquide", "sect": "Industrie", "ceo": "François Jackow", "crea": "1902"},
    "BNP.PA": {"nom": "BNP Paribas", "sect": "Banque", "ceo": "J.L. Bonnafé", "crea": "1966"},
    "EL.PA": {"nom": "EssilorLuxottica", "sect": "Optique", "ceo": "Francesco Milleri", "crea": "2018"},
    "DG.PA": {"nom": "Vinci", "sect": "BTP", "ceo": "Xavier Huillard", "crea": "1899"},
    "SAF.PA": {"nom": "Safran", "sect": "Aéro", "ceo": "Olivier Andriès", "crea": "2005"},
    "STLAP.PA": {"nom": "Stellantis", "sect": "Auto", "ceo": "Carlos Tavares", "crea": "2021"},
    "DSY.PA": {"nom": "Dassault Systèmes", "sect": "Logiciels", "ceo": "Bernard Charlès", "crea": "1981"},
    "KER.PA": {"nom": "Kering", "sect": "Luxe", "ceo": "F.H. Pinault", "crea": "1963"},
    "CS.PA": {"nom": "AXA", "sect": "Assurance", "ceo": "Thomas Buberl", "crea": "1817"},
    "SGO.PA": {"nom": "Saint-Gobain", "sect": "Matériaux", "ceo": "Benoît Bazin", "crea": "1665"},
    "STMPA.PA": {"nom": "STMicroelectronics", "sect": "Semi-cond.", "ceo": "Jean-Marc Chéry", "crea": "1987"},
    "BN.PA": {"nom": "Danone", "sect": "Agro", "ceo": "A. de Saint-Affrique", "crea": "1919"},
    "CAP.PA": {"nom": "Capgemini", "sect": "IT", "ceo": "Aiman Ezzat", "crea": "1967"},
    "HO.PA": {"nom": "Thales", "sect": "Défense", "ceo": "Patrice Caine", "crea": "1893"},
    "ENGI.PA": {"nom": "Engie", "sect": "Énergie", "ceo": "Catherine MacGregor", "crea": "2008"},
    "VIE.PA": {"nom": "Veolia", "sect": "Environnement", "ceo": "E. Brachlianoff", "crea": "1853"},
    "RI.PA": {"nom": "Pernod Ricard", "sect": "Spiritueux", "ceo": "Alexandre Ricard", "crea": "1975"},
    "ACA.PA": {"nom": "Crédit Agricole", "sect": "Banque", "ceo": "Philippe Brassac", "crea": "1885"},
    "PUB.PA": {"nom": "Publicis", "sect": "Pub", "ceo": "Arthur Sadoun", "crea": "1926"},
    "ORA.PA": {"nom": "Orange", "sect": "Télécom", "ceo": "Christel Heydemann", "crea": "1988"},
    "ML.PA": {"nom": "Michelin", "sect": "Pneus", "ceo": "Florent Menegaux", "crea": "1889"},
    "MT.PA": {"nom": "ArcelorMittal", "sect": "Acier", "ceo": "Aditya Mittal", "crea": "2006"},
    "GLE.PA": {"nom": "Société Générale", "sect": "Banque", "ceo": "Slawomir Krupa", "crea": "1864"},
    "CA.PA": {"nom": "Carrefour", "sect": "Distrib.", "ceo": "Alexandre Bompard", "crea": "1959"},
    "EN.PA": {"nom": "Bouygues", "sect": "BTP", "ceo": "Olivier Roussat", "crea": "1952"},
    "LR.PA": {"nom": "Legrand", "sect": "Élec", "ceo": "Benoît Coquart", "crea": "1865"},
    "FGR.PA": {"nom": "Eiffage", "sect": "BTP", "ceo": "Benoît de Ruffray", "crea": "1992"},
    "BVI.PA": {"nom": "Bureau Veritas", "sect": "Certif.", "ceo": "Hinda Gharbi", "crea": "1828"},
    "AC.PA": {"nom": "Accor", "sect": "Hôtel", "ceo": "Sébastien Bazin", "crea": "1967"},
    "TEP.PA": {"nom": "Teleperformance", "sect": "Services", "ceo": "Daniel Julien", "crea": "1978"},
    "ENX.PA": {"nom": "Euronext", "sect": "Finance", "ceo": "Stéphane Boujnah", "crea": "2000"},
    "ERF.PA": {"nom": "Eurofins", "sect": "Biotech", "ceo": "Gilles Martin", "crea": "1987"},
    "WLN.PA": {"nom": "Worldline", "sect": "Paiement", "ceo": "M.H. Desportes", "crea": "1972"}
}

# --- 3. LOGIQUE D'ANALYSE ---
@st.cache_data(ttl=3600)
def analyze(ticker):
    df = yf.download(ticker, period="1mo", progress=False)
    if df.empty or len(df) < 5: return None
    p_actuel = float(df['Close'].iloc[-1])
    p_5j = float(df['Close'].iloc[-5])
    moyenne = float(df['Close'].mean())
    var = ((p_actuel - p_5j) / p_5j) * 100
    verdict = "🟢 ACHAT" if p_actuel < moyenne else "⚪ ATTENTE"
    return {"prix": round(p_actuel, 2), "var": round(var, 2), "statut": verdict, "df": df['Close']}

# --- 4. INTERFACE ---
st.title("🏛️ CAC 40 Intelligence - Direction Générale")
st.write(f"Bienvenue, Roselia. Voici l'état des 40 piliers de l'économie.")

cols = st.columns(4) # 4 colonnes pour une vue d'ensemble compacte

for i, (ticker, info) in enumerate(ENTREPRISES.items()):
    data = analyze(ticker)
    if data:
        with cols[i % 4]:
            st.write(f"### {info['nom']}")
            st.caption(f"{ticker} | {info['sect']}")
            
            # Métriques simplifiées pour la grille
            st.metric("Prix", f"{data['prix']} €", delta=f"{data['var']}% (5j)")
            st.write(f"**Verdict :** {data['statut']}")
            
            # Mini graphique
            st.line_chart(data['df'], height=80)
            
            # Fiche détaillée
            with st.expander("👤 Identité"):
                st.write(f"**CEO :** {info['ceo']}")
                st.write(f"**Création :** {info['crea']}")
