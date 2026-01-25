import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Dashboard Pro CAC40", layout="wide")
st.title("📈 Ma Salle de Marché - BTS SIO")

# Liste complète du CAC 40
cac40 = [
    "AC.PA", "AI.PA", "AIR.PA", "MT.PA", "CS.PA", "BNP.PA", "EN.PA", "BVI.PA", 
    "CAP.PA", "CA.PA", "ACA.PA", "BN.PA", "DSY.PA", "FGR.PA", "ENGI.PA", "EL.PA", 
    "ERF.PA", "ENX.PA", "RMS.PA", "KER.PA", "OR.PA", "LR.PA", "MC.PA", "ML.PA", 
    "ORA.PA", "RI.PA", "PUB.PA", "SAF.PA", "SGO.PA", "SAN.PA", "SU.PA", "GLE.PA", 
    "STLAP.PA", "STMPA.PA", "TEP.PA", "HO.PA", "TTE.PA", "VIE.PA", "DG.PA", "WLN.PA"
]

# Sidebar pour les contrôles
with st.sidebar:
    st.header("Paramètres")
    refresh = st.button("Actualiser les données")

# Grille d'affichage
cols = st.columns(4)
for i, ticker in enumerate(cac40):
    try:
        data = yf.Ticker(ticker).history(period="1mo")
        prix = round(data['Close'].iloc[-1], 2)
        moyenne = round(data['Close'].mean(), 2)
        
        with cols[i % 4]:
            st.write(f"### {ticker}")
            label_conseil = "🟢 ACHAT" if prix < moyenne else "⚪ ATTENTE"
            st.metric("Prix actuel", f"{prix} €", delta=label_conseil)
            st.line_chart(data['Close'], height=120)
    except:
        continue
