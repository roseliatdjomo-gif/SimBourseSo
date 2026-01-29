import streamlit as st                                         
import yfinance as yf                                          
import plotly.graph_objects as go                              # Ligne 3
from datetime import datetime, timedelta                       # Ligne 4
                                                               # Ligne 5
# --- FONCTIONS (LOGIQUE) ---                                  # Ligne 6
def obtenir_infos_action(ticker):                              # Ligne 7
    try:                                                       # Ligne 8
        data = yf.Ticker(ticker)                               # Ligne 9
        info = data.info                                       # Ligne 10
        secteur = info.get('sector', 'Secteur non disponible') # Ligne 11
        creation = info.get('longBusinessSummary', 'N/A')      # Ligne 12
        return secteur, creation                               # Ligne 13
    except:                                                    # Ligne 14
        return "Erreur", "Données indisponibles"               # Ligne 15
                                                               # Ligne 16
def afficher_graphique_interactif(ticker, periode):            # Ligne 17
    data = yf.download(ticker, period=periode)                 # Ligne 18
    data['MA20'] = data['Close'].rolling(window=20).mean()     # Ligne 19
    fig = go.Figure()                                          # Ligne 20
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Prix')) # Ligne 21
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], name='Moyenne', line=dict(dash='dash'))) # Ligne 22
    fig.update_layout(template="plotly_dark", height=400)      # Ligne 23
    return fig                                                 # Ligne 24
                                                               # Ligne 25
# --- CONFIGURATION ET LISTE ---                               # Ligne 26
st.set_page_config(page_title="Dashboard Pro CAC40", layout="wide") # Ligne 27
                                                               # Ligne 28
cac40 = [                                                      # Ligne 29
    "AC.PA", "AI.PA", "AIR.PA", "MT.PA", "CS.PA", "BNP.PA", "EN.PA", "BVI.PA", # Ligne 30
    "CAP.PA", "CA.PA", "ACA.PA", "BN.PA", "DSY.PA", "FGR.PA", "ENGI.PA", "EL.PA", # Ligne 31
    "ERF.PA", "ENX.PA", "RMS.PA", "KER.PA", "OR.PA", "LR.PA", "MC.PA", "ML.PA", # Ligne 32
    "ORA.PA", "RI.PA", "PUB.PA", "SAF.PA", "SGO.PA", "SAN.PA", "SU.PA", "GLE.PA", # Ligne 33
    "STLAP.PA", "STMPA.PA", "TEP.PA", "HO.PA", "TTE.PA", "VIE.PA", "DG.PA", "WLN.PA" # Ligne 34
]                                                              # Ligne 35
                                                               # Ligne 36
st.title("📈 Ma Salle de Marché - BTS SIO")                    # Ligne 37
                                                               # Ligne 38
# --- ANALYSE DÉTAILLÉE (HAUT DE PAGE) ---                     # Ligne 39
action_detail = st.selectbox("Sélectionnez une action :", cac40) # Ligne 40
periode = st.radio("Période :", ["1d", "1mo", "3mo", "6mo", "1y"], horizontal=True) # Ligne 41
                                                               # Ligne 42
st.plotly_chart(afficher_graphique_interactif(action_detail, periode), use_container_width=True) # Ligne 43
                                                               # Ligne 44
if periode == "1y":                                            # Ligne 45
    st.write("📊 **Événements sur 1 an :** Janvier (Résultats), Mars (Taux), Octobre (Luxe).") # Ligne 46
elif periode == "6mo":                                         # Ligne 47
    st.write("📊 **Événements sur 6 mois :** Inflation et consommation estivale.") # Ligne 48
                                                               # Ligne 49
st.markdown("---")                                             # Ligne 50
                                                               # Ligne 51
# --- GRILLE DES 40 ACTIONS (BAS DE PAGE) ---                  # Ligne 52
cols = st.columns(4)                                           # Ligne 53
for i, ticker in enumerate(cac40):                             # Ligne 54
    try:                                                       # Ligne 55
        data = yf.Ticker(ticker).history(period="1mo")         # Ligne 56
        prix = round(data['Close'].iloc[-1], 2)                # Ligne 57
        moyenne = round(data['Close'].mean(), 2)               # Ligne 58
                                                               # Ligne 59
        with cols[i % 4]:                                      # Ligne 60
            st.write(f"### {ticker}")                          # Ligne 61
            conseil = "🟢 ACHAT" if prix < moyenne else "⚪ ATTENTE" # Ligne 62
            st.metric("Prix", f"{prix} €", delta=conseil)      # Ligne 63
            st.line_chart(data['Close'], height=120)           # Ligne 64
                                                               # Ligne 65
            # On affiche les infos pour CHAQUE action automatiquement
            sect, desc = obtenir_infos_action(ticker)          # Ligne 66
            st.write(f"**Secteur :** {sect}")                  # Ligne 67
            with st.expander("📖 En savoir plus"):              # Ligne 68
                st.caption(desc)                               # Ligne 69
    except:                                                    
        continue                                               
