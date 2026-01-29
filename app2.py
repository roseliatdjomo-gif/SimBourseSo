import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. DESIGN & STYLE (L'arme de la CEO) ---
st.set_page_config(page_title="CAC 40 Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    div[data-testid="column"] {
        background: #111111;
        border: 1px solid #222;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    div[data-testid="column"]:hover { border-color: #00ffcc; }
    h3 { color: #00ffcc !important; margin-bottom: 5px; font-size: 1.4rem; }
    .variation-pos { color: #00ff88; font-weight: bold; }
    .variation-neg { color: #ff4b4b; font-weight: bold; }
    .stMetric { background-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES (Ordonnée par puissance) ---
ENTREPRISES = {
    "MC.PA": {"nom": "LVMH", "sect": "Luxe", "ceo": "Bernard Arnault", "crea": "1987", "bio": "Leader mondial du luxe."},
    "OR.PA": {"nom": "L'Oréal", "sect": "Beauté", "ceo": "Nicolas Hieronimus", "crea": "1909", "bio": "N°1 mondial de la cosmétique."},
    "RMS.PA": {"nom": "Hermès", "sect": "Luxe", "ceo": "Axel Dumas", "crea": "1837", "bio": "Excellence de la maroquinerie."},
    "TTE.PA": {"nom": "TotalEnergies", "sect": "Énergie", "ceo": "Patrick Pouyanné", "crea": "1924", "bio": "Géant de l'énergie multi-sources."},
    "SAN.PA": {"nom": "Sanofi", "sect": "Santé", "ceo": "Paul Hudson", "crea": "1973", "bio": "Leader de la pharmacie et vaccins."},
    "AIR.PA": {"nom": "Airbus", "sect": "Aéro", "ceo": "Guillaume Faury", "crea": "1970", "bio": "Champion de l'aviation civile."},
    "SU.PA": {"nom": "Schneider", "sect": "Électricité", "ceo": "Peter Herweck", "crea": "1836", "bio": "Gestion de l'énergie."},
    "AI.PA": {"nom": "Air Liquide", "sect": "Industrie", "ceo": "François Jackow", "crea": "1902", "bio": "Gaz industriels et oxygène."},
    "BNP.PA": {"nom": "BNP Paribas", "sect": "Banque", "ceo": "J.L. Bonnafé", "crea": "1966", "bio": "1ère banque de la zone euro."},
    "EL.PA": {"nom": "EssilorLux", "sect": "Optique", "ceo": "F. Milleri", "crea": "2018", "bio": "Leader mondial des lunettes."}
}

# --- 3. LOGIQUE DE CALCUL (5 Jours & Décision) ---
@st.cache_data(ttl=3600)
def get_stock_analysis(ticker):
    # On récupère 1 mois pour avoir la moyenne et les 5 derniers jours
    df = yf.download(ticker, period="1mo", progress=False)
    if df.empty: return None
    
    prix_actuel = df['Close'].iloc[-1]
    prix_il_y_a_5j = df['Close'].iloc[-5] if len(df) >= 5 else df['Close'].iloc[0]
    moyenne_mois = df['Close'].mean()
    
    # Calcul de la variation sur 5 jours
    variation_5j = ((prix_actuel - prix_il_y_a_5j) / prix_il_y_a_5j) * 100
    
    # Décision de la CEO
    decision = "🟢 ACHAT" if prix_actuel < moyenne_mois else "⚪ ATTENTE"
    
    return {
        "prix": round(prix_actuel, 2),
        "var": round(variation_5j, 2),
        "statut": decision,
        "history": df['Close']
    }

# --- 4. INTERFACE ---
st.title("🏛️ Roselia Capital : Décisions Stratégiques")
st.markdown("---")

cols = st.columns(2)

for i, (ticker, info) in enumerate(ENTREPRISES.items()):
    data = get_stock_analysis(ticker)
    if data:
        with cols[i % 2]:
            # En-tête : Nom + Code
            st.write(f"### {info['nom']} ({ticker})")
            
            # Ligne des indicateurs : Prix | Var 5j | Verdict
            c1, c2, c3 = st.columns(3)
            c1.metric("Prix", f"{data['prix']} €")
            
            # Couleur de la variation
            color_class = "variation-pos" if data['var'] >= 0 else "variation-neg"
            c2.markdown(f"Var. 5j<br><span class='{color_class}'>{data['var']}%</span>", unsafe_allow_html=True)
            
            c3.metric("VERDICT", data['statut'])
            
            # Graphique de tendance
            st.line_chart(data['history'], height=120)
            
            # Fiche entreprise "En savoir plus"
            with st.expander("📖 Fiche Entreprise & CEO"):
                st.write(f"**Dirigeant :** {info['ceo']}")
                st.write(f"**Secteur :** {info['sect']} | **Créé en :** {info['crea']}")
                st.write(f"**Activité :** {info['bio']}")
                st.caption(f"Le verdict '{data['statut']}' est basé sur la position du prix actuel par rapport à sa moyenne mensuelle.")
