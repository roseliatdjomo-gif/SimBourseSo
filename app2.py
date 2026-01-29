import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. DESIGN "LUXE & DÉCISION" ---
st.set_page_config(page_title="Roselia Capital - CAC 40", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    div[data-testid="column"] {
        background: #111;
        border: 1px solid #222;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.3s ease;
    }
    div[data-testid="column"]:hover { border-color: #00ffcc; transform: translateY(-2px); }
    h3 { color: #00ffcc !important; font-size: 1.3rem; margin-bottom: 0px; }
    .stMetricValue { font-size: 1.6rem !important; }
    .variation-label { font-size: 0.9rem; color: #888; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES HIÉRARCHIQUE ---
ENTREPRISES = {
    "MC.PA": {"nom": "LVMH", "sect": "Luxe", "ceo": "Bernard Arnault", "crea": "1987", "bio": "N°1 mondial du luxe."},
    "OR.PA": {"nom": "L'Oréal", "sect": "Beauté", "ceo": "Nicolas Hieronimus", "crea": "1909", "bio": "Leader mondial des cosmétiques."},
    "RMS.PA": {"nom": "Hermès", "sect": "Luxe", "ceo": "Axel Dumas", "crea": "1837", "bio": "Excellence de la maroquinerie."},
    "TTE.PA": {"nom": "TotalEnergies", "sect": "Énergie", "ceo": "Patrick Pouyanné", "crea": "1924", "bio": "Géant mondial multi-énergies."},
    "SAN.PA": {"nom": "Sanofi", "sect": "Santé", "ceo": "Paul Hudson", "crea": "1973", "bio": "Leader de la santé humaine."},
    "AIR.PA": {"nom": "Airbus", "sect": "Aéro", "ceo": "Guillaume Faury", "crea": "1970", "bio": "Champion de l'aviation civile."},
    "SU.PA": {"nom": "Schneider", "sect": "Énergie", "ceo": "Peter Herweck", "crea": "1836", "bio": "Gestion numérique de l'énergie."},
    "AI.PA": {"nom": "Air Liquide", "sect": "Industrie", "ceo": "François Jackow", "crea": "1902", "bio": "Gaz industriels et santé."},
    "BNP.PA": {"nom": "BNP Paribas", "sect": "Banque", "ceo": "J.L. Bonnafé", "crea": "1966", "bio": "1ère banque de la zone euro."},
    "EL.PA": {"nom": "EssilorLux", "sect": "Optique", "ceo": "F. Milleri", "crea": "2018", "bio": "Leader mondial des lunettes."}
}

# --- 3. ANALYSE TECHNIQUE ---
@st.cache_data(ttl=3600)
def get_analysis(ticker):
    df = yf.download(ticker, period="1mo", progress=False)
    if df.empty or len(df) < 5: return None
    
    # Correction du bug de comparaison (on extrait la valeur simple)
    prix_actuel = float(df['Close'].iloc[-1])
    prix_5j = float(df['Close'].iloc[-5])
    moyenne = float(df['Close'].mean())
    
    variation = ((prix_actuel - prix_5j) / prix_5j) * 100
    verdict = "🟢 ACHAT" if prix_actuel < moyenne else "⚪ ATTENTE"
    
    return {"prix": round(prix_actuel, 2), "var": round(variation, 2), "statut": verdict, "df": df['Close']}

# --- 4. INTERFACE ---
st.title("🏛️ Roselia Capital : Décisions Marché")

cols = st.columns(2)

for i, (ticker, info) in enumerate(ENTREPRISES.items()):
    data = get_analysis(ticker)
    if data:
        with cols[i % 2]:
            st.write(f"### {info['nom']} ({ticker})")
            
            # Grille d'indicateurs
            m1, m2, m3 = st.columns(3)
            m1.metric("Prix", f"{data['prix']} €")
            m2.metric("Var. 5j", f"{data['var']}%")
            m3.metric("VERDICT", data['statut'])
            
            # Tendance visuelle
            st.line_chart(data['df'], height=100)
            
            # Infos CEO et Entreprise
            with st.expander("📄 Voir la fiche identité"):
                st.markdown(f"**Dirigeant :** {info['ceo']} | **Créé en :** {info['crea']}")
                st.markdown(f"**Secteur :** {info['sect']}")
                st.caption(f"Note : {info['bio']}")
