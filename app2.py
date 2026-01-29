import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- 1. DESIGN "PRESTIGE" (CSS personnalisé) ---
st.set_page_config(page_title="CAC 40 Intelligence - Direction", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    /* Style des cartes entreprises */
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
    h3 { color: #00ffcc !important; font-family: 'Georgia', serif; font-size: 1.3rem; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    .stInfo { background-color: #111; border: 1px solid #00ffcc; color: #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LA GRANDE BASE DE DONNÉES (Identité des leaders) ---
# --- BASE DE DONNÉES CLASSÉE PAR PUISSANCE ÉCONOMIQUE ---
ENTREPRISES = { 
    # LE TOP 10 (Les Maîtres du Marché)
    "MC.PA": {"nom": "LVMH", "sect": "Luxe", "creation": "1987", "ceo": "Bernard Arnault", "bio": "Leader mondial du luxe, première capitalisation européenne."},
    "OR.PA": {"nom": "L'Oréal", "sect": "Cosmétique", "creation": "1909", "ceo": "Nicolas Hieronimus", "bio": "Leader mondial de la beauté, croissance historique exceptionnelle."},
    "RMS.PA": {"nom": "Hermès", "sect": "Luxe", "creation": "1837", "ceo": "Axel Dumas", "bio": "Maison d'excellence, l'une des rentabilités les plus hautes au monde."},
    "TTE.PA": {"nom": "TotalEnergies", "sect": "Énergie", "creation": "1924", "ceo": "Patrick Pouyanné", "bio": "Pilier énergétique mondial, acteur majeur de la transition."},
    "SAN.PA": {"nom": "Sanofi", "sect": "Santé", "creation": "1973", "ceo": "Paul Hudson", "bio": "Géant de la santé et des vaccins."},
    "AIR.PA": {"nom": "Airbus", "sect": "Aéronautique", "creation": "1970", "ceo": "Guillaume Faury", "bio": "Leader mondial de l'aviation civile."},
    "SU.PA": {"nom": "Schneider Electric", "sect": "Énergie", "creation": "1836", "ceo": "Peter Herweck", "bio": "Spécialiste mondial de la gestion de l'énergie numérique."},
    "AI.PA": {"nom": "Air Liquide", "sect": "Industrie", "creation": "1902", "ceo": "François Jackow", "bio": "Champion des gaz industriels et de l'hydrogène."},
    "BNP.PA": {"nom": "BNP Paribas", "sect": "Banque", "creation": "1966", "ceo": "Jean-Laurent Bonnafé", "bio": "Plus grande banque de la zone euro."},
    "EL.PA": {"nom": "EssilorLuxottica", "sect": "Optique", "creation": "2018", "ceo": "Francesco Milleri", "bio": "Leader mondial des verres et montures de lunettes."},

    # LES GRANDS GROUPES INDUSTRIELS ET FINANCIERS
    "DG.PA": {"nom": "Vinci", "sect": "BTP / Concessions", "creation": "1899", "ceo": "Xavier Huillard", "bio": "Leader mondial de la construction et des concessions."},
    "SAF.PA": {"nom": "Safran", "sect": "Aéronautique", "creation": "2005", "ceo": "Olivier Andriès", "bio": "Moteurs d'avions et équipements aéronautiques."},
    "STLAP.PA": {"nom": "Stellantis", "sect": "Automobile", "creation": "2021", "ceo": "Carlos Tavares", "bio": "Constructeur auto issu de PSA et Fiat Chrysler."},
    "DSY.PA": {"nom": "Dassault Systèmes", "sect": "Logiciels", "creation": "1981", "ceo": "Bernard Charlès", "bio": "Logiciels 3D et simulation industrielle."},
    "KER.PA": {"nom": "Kering", "sect": "Luxe", "creation": "1963", "ceo": "François-Henri Pinault", "bio": "Propriétaire de Gucci et Saint Laurent."},
    "CS.PA": {"nom": "AXA", "sect": "Assurance", "creation": "1817", "ceo": "Thomas Buberl", "bio": "Leader européen de l'assurance."},
    "SGO.PA": {"nom": "Saint-Gobain", "sect": "Matériaux", "creation": "1665", "ceo": "Benoît Bazin", "bio": "Leader mondial de l'habitat durable."},
    "STMPA.PA": {"nom": "STMicroelectronics", "sect": "Semi-conducteurs", "creation": "1987", "ceo": "Jean-Marc Chéry", "bio": "Composants électroniques pour le futur."},
    "BN.PA": {"nom": "Danone", "sect": "Agroalimentaire", "creation": "1919", "ceo": "Antoine de Saint-Affrique", "bio": "Produits laitiers et nutrition médicale."},
    "CAP.PA": {"nom": "Capgemini", "sect": "Services IT", "creation": "1967", "ceo": "Aiman Ezzat", "bio": "Conseil et transformation numérique."},

    # LES INFRASTRUCTURES ET SERVICES
    "HO.PA": {"nom": "Thales", "sect": "Défense", "creation": "1893", "ceo": "Patrice Caine", "bio": "Défense, sécurité et identité numérique."},
    "ENGI.PA": {"nom": "Engie", "sect": "Énergie", "creation": "2008", "ceo": "Catherine MacGregor", "bio": "Services énergétiques et gaz naturel."},
    "VIE.PA": {"nom": "Veolia", "sect": "Environnement", "creation": "1853", "ceo": "Estelle Brachlianoff", "bio": "Gestion de l'eau, des déchets et de l'énergie."},
    "RI.PA": {"nom": "Pernod Ricard", "sect": "Spiritueux", "creation": "1975", "ceo": "Alexandre Ricard", "bio": "Co-leader mondial des vins et spiritueux."},
    "ACA.PA": {"nom": "Crédit Agricole", "sect": "Banque", "creation": "1885", "ceo": "Philippe Brassac", "bio": "Banque de proximité leader en Europe."},
    "PUB.PA": {"nom": "Publicis", "sect": "Publicité", "creation": "1926", "ceo": "Arthur Sadoun", "bio": "Communication et marketing data."},
    "ORA.PA": {"nom": "Orange", "sect": "Télécoms", "creation": "1988", "ceo": "Christel Heydemann", "bio": "Opérateur historique télécoms."},
    "ML.PA": {"nom": "Michelin", "sect": "Pneumatiques", "creation": "1889", "ceo": "Florent Menegaux", "bio": "Leader mondial du pneu."},
    "MT.PA": {"nom": "ArcelorMittal", "sect": "Sidérurgie", "creation": "2006", "ceo": "Aditya Mittal", "bio": "Leader mondial de l'acier."},
    "GLE.PA": {"nom": "Société Générale", "sect": "Banque", "creation": "1864", "ceo": "Slawomir Krupa", "bio": "Grande banque de financement et d'investissement."},

    # LE RESTE DU CLUB
    "CA.PA": {"nom": "Carrefour", "sect": "Distribution", "creation": "1959", "ceo": "Alexandre Bompard", "bio": "Distribution alimentaire mondiale."},
    "EN.PA": {"nom": "Bouygues", "sect": "BTP / Télécom", "creation": "1952", "ceo": "Olivier Roussat", "bio": "Groupe diversifié présent dans les médias (TF1)."},
    "LR.PA": {"nom": "Legrand", "sect": "Électricité", "creation": "1865", "ceo": "Benoît Coquart", "bio": "Infrastructure électrique pour bâtiments."},
    "FGR.PA": {"nom": "Eiffage", "sect": "BTP", "creation": "1992", "ceo": "Benoît de Ruffray", "bio": "Construction et concessions autoroutières."},
    "BVI.PA": {"nom": "Bureau Veritas", "sect": "Certification", "creation": "1828", "ceo": "Hinda Gharbi", "bio": "Tests et inspection de conformité."},
    "AC.PA": {"nom": "Accor", "sect": "Hôtellerie", "creation": "1967", "ceo": "Sébastien Bazin", "bio": "Premier hôtelier européen."},
    "TEP.PA": {"nom": "Teleperformance", "sect": "Services", "creation": "1978", "ceo": "Daniel Julien", "bio": "Gestion de la relation client mondiale."},
    "ENX.PA": {"nom": "Euronext", "sect": "Finance", "creation": "2000", "ceo": "Stéphane Boujnah", "bio": "Gestionnaire des bourses européennes."},
    "ERF.PA": {"nom": "Eurofins", "sect": "Biotech", "creation": "1987", "ceo": "Gilles Martin", "bio": "Analyses bioanalytiques mondiales."},
    "WLN.PA": {"nom": "Worldline", "sect": "Paiements", "creation": "1972", "ceo": "Marc-Henri Desportes (PI)", "bio": "Services de transactions numériques."}
}

for t in TICKERS_RESTANTS:
    if t not in ENTREPRISES:
        ENTREPRISES[t] = {"nom": t, "sect": "Industrie/Service", "creation": "N/A", "ceo": "Dirigeant actuel", "bio": "Action membre de l'indice CAC 40."}

# --- 3. LOGIQUE & FONCTIONS ---
@st.cache_data
def load_data(ticker, p):
    return yf.download(ticker, period=p, progress=False)

# --- 4. INTERFACE ---
st.title("🏛️ CAC 40 Intelligence - Roselia CEO Edition")

# Sélecteurs en haut
c1, c2 = st.columns([1, 1])
with c1:
    action_target = st.selectbox("🎯 Choisir une cible stratégique :", list(ENTREPRISES.keys()))
with c2:
    periode = st.radio("⏳ Période d'observation :", ["1mo", "6mo", "1y"], horizontal=True)

# Graphique interactif
data = load_data(action_target, periode)
if not data.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], line=dict(color='#00ffcc', width=3), name='Cours'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- 5. FICHE D'IDENTITÉ (Le résumé que tu voulais) ---
info = ENTREPRISES[action_target]
with st.container():
    col_info1, col_info2 = st.columns([1, 2])
    with col_info1:
        st.info(f"**🏢 Société :** {info['nom']}\n\n**👤 CEO :** {info['ceo']}\n\n**🗓️ Création :** {info['creation']}")
    with col_info2:
        st.info(f"**📖 Résumé :** {info['bio']}")

st.markdown("---")

# --- 6. GRILLE LIVE ---
st.subheader("📡 État Global du Marché")
cols = st.columns(4)
for i, ticker in enumerate(ENTREPRISES.keys()):
    try:
        df = load_data(ticker, "1mo")
        if df.empty: continue
        prix = round(df['Close'].iloc[-1], 2)
        moyenne = round(df['Close'].mean(), 2)
        
        with cols[i % 4]:
            st.write(f"### {ENTREPRISES[ticker]['nom']}")
            signal = "🟢 ACHAT" if prix < moyenne else "⚪ ATTENTE"
            st.metric(ENTREPRISES[ticker]['sect'], f"{prix} €", delta=signal)
            st.line_chart(df['Close'], height=60)
    except:
        continue
