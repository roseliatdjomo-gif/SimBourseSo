import streamlit as st                                         
import yfinance as yf                                          
import plotly.graph_objects as go                              
from datetime import datetime, timedelta                       

# --- FONCTIONS (LOGIQUE) ---
@st.cache_data # Cette ligne est magique : elle garde les infos en mémoire !
def obtenir_infos_action(ticker):
    try:
        data = yf.Ticker(ticker)
        # On demande seulement le secteur pour aller plus vite
        secteur = data.fast_info.get('sector', 'Secteur non disponible')
        creation = "Informations détaillées dans l'onglet 'En savoir plus'"
        return secteur, creation
    except:
        return "Secteur indisponible", "Erreur de connexion"

def afficher_graphique_interactif(ticker, periode):
    data = yf.download(ticker, period=periode)
    data['MA20'] = data['Close'].rolling(window=20).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Prix'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='Moyenne', line=dict(dash='dash')))
    fig.update_layout(template="plotly_dark", height=400)
    return fig

# --- CONFIGURATION ET DONNÉES ---
st.set_page_config(page_title="Dashboard Pro CAC40", layout="wide")

cac40 = [
    "AC.PA", "AI.PA", "AIR.PA", "MT.PA", "CS.PA", "BNP.PA", "EN.PA", "BVI.PA", 
    "CAP.PA", "CA.PA", "ACA.PA", "BN.PA", "DSY.PA", "FGR.PA", "ENGI.PA", "EL.PA", 
    "ERF.PA", "ENX.PA", "RMS.PA", "KER.PA", "OR.PA", "LR.PA", "MC.PA", "ML.PA", 
    "ORA.PA", "RI.PA", "PUB.PA", "SAF.PA", "SGO.PA", "SAN.PA", "SU.PA", "GLE.PA", 
    "STLAP.PA", "STMPA.PA", "TEP.PA", "HO.PA", "TTE.PA", "VIE.PA", "DG.PA", "WLN.PA"
]

# TA BASE DE DONNÉES D'ÉVÉNEMENTS
evenements = {
    "MC.PA": {
        "1y": "Hausse record du luxe au 1er semestre, puis ralentissement chinois en fin d'année.",
        "6mo": "Correction du secteur suite aux prévisions de croissance revues à la baisse."
    },
    "TTE.PA": {
        "1y": "Fluctuation liée au prix du baril de pétrole et aux tensions géopolitiques.",
        "6mo": "Stabilité grâce aux investissements massifs dans les énergies renouvelables."
    },
    "OR.PA": {
        "1y": "Forte reprise post-covid des ventes en Asie et succès du e-commerce.",
        "6mo": "Résilience malgré l'inflation grâce au positionnement haut de gamme."
    }
}

st.title("📈 Ma Salle de Marché - BTS SIO")

# --- ANALYSE DÉTAILLÉE ---
action_detail = st.selectbox("Sélectionnez une action :", cac40)
periode = st.radio("Période :", ["1d", "1mo", "3mo", "6mo", "1y"], horizontal=True)

st.plotly_chart(afficher_graphique_interactif(action_detail, periode), use_container_width=True)

# AFFICHAGE DE L'EXPLICATION DE TA BASE DE DONNÉES
st.subheader(f"📜 Analyse des variations ({periode})")
if action_detail in evenements and periode in evenements[action_detail]:
    st.info(evenements[action_detail][periode])
else:
    st.write("Analyse automatique : La variation suit la tendance générale du marché CAC 40.")

st.markdown("---")

# --- GRILLE DES 40 ACTIONS ---
cols = st.columns(4)
for i, ticker in enumerate(cac40):
    try:
        data = yf.Ticker(ticker).history(period="1mo")
        prix = round(data['Close'].iloc[-1], 2)
        moyenne = round(data['Close'].mean(), 2)
        
        with cols[i % 4]:
            st.write(f"### {ticker}")
            conseil = "🟢 ACHAT" if prix < moyenne else "⚪ ATTENTE"
            st.metric("Prix", f"{prix} €", delta=conseil)
            st.line_chart(data['Close'], height=120)
            
            sect, desc = obtenir_infos_action(ticker)
            st.write(f"**Secteur :** {sect}")
            with st.expander("📖 En savoir plus"):
                st.caption(desc)
    except:
        continue
