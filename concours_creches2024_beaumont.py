import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
from collections import defaultdict

# Configurer la page
st.set_page_config(page_title="Vote : Concours de la plus belle crèche Noël 2024", page_icon="🌟", layout="centered")

# Initialiser le stockage des votes
if 'votes' not in st.session_state:
    st.session_state.votes = {
        "Catégorie Famille": defaultdict(int),
        "Catégorie Paroisse": defaultdict(int)
    }

if 'votes_cast_categories' not in st.session_state:
    st.session_state.votes_cast_categories = set()  # Stocker les catégories où l'utilisateur a déjà voté

# Fonction pour générer un QR Code
def generer_qr_code(data):
    qr = qrcode.QRCode(
        version=2,  # Version ajustée pour réduire la taille
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,  # Taille ajustée pour le QR Code
        border=2  # Bordure standard
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Fonction pour réinitialiser les votes
def reinitialiser_votes():
    st.session_state.votes = {
        "Catégorie Famille": defaultdict(int),
        "Catégorie Paroisse": defaultdict(int)
    }
    st.session_state.votes_cast_categories = set()

# Titre de l'application
st.title("Concours de la plus belle crèche Noël 2024 🎄")
st.markdown("**Votez pour votre crèche préférée parmi les catégories ci-dessous !**")

# Ajouter un QR Code pour partager l'application
st.subheader("Partagez cette application")
qr_data = "https://votescreches2024-nxjtyxkx2hhdkmod87bgyz.streamlit.app/"  # Remplacez par le lien Streamlit après déploiement
img = generer_qr_code(qr_data)
buffer = BytesIO()
img.save(buffer, format="PNG")
st.image(buffer.getvalue(), caption="Scannez-moi pour voter !", use_container_width=True)

# Catégories et options
categories = {
    "Catégorie Famille": [
        "Choisissez une option",  # Option explicite
        "1. Famille Rocha Da Cruz",
        "2. Famille AMENYO",
        "3. Famille AGNERE",
        "4. Famille GONGORA",
        "5. Famille STENGER",
        "6. Famille UBEDA"
    ],
    "Catégorie Paroisse": [
        "Choisissez une option",  # Option explicite
        "1. Église St Denis à Nointel",
        "2. Chapelle Notre Dame de la Réconciliation à Mours",
        "3. Église St Germain l’Auxerrois à Presles",
        "4. Église St Laurent à Beaumont"
    ]
}

# Sélection de catégorie
category_choice = st.selectbox("Choisissez une catégorie :", list(categories.keys()))

# Afficher les options de vote pour la catégorie sélectionnée
st.subheader(f"Votes pour la catégorie {category_choice}")
vote_choice = st.radio(
    "Choisissez votre crèche préférée :",
    [f"{i}. {option}" if option != "Choisissez une option" else option for i, option in enumerate(categories[category_choice], start=1)]
)

# Partie administrateur uniquement avec code correct
st.sidebar.title("Mode Administrateur")
admin_password = st.sidebar.text_input("Entrez le code administrateur :", type="password")

if admin_password == "Beaumont@2024":
    st.sidebar.success("Accès administrateur accordé")
    st.sidebar.subheader("Options d'administration")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Rafraîchir la page (Admin)"):
            st.experimental_rerun()
    with col2:
        if st.button("🗑️ Réinitialiser les votes"):
            reinitialiser_votes()
            st.success("Les votes ont été réinitialisés.")
            st.experimental_rerun()

    # Administrateur peut voter plusieurs fois
    if vote_choice != "Choisissez une option":
        if st.button("Valider mon vote (Admin) ✅"):
            st.session_state.votes[category_choice][vote_choice] += 1
            st.success(f"Vote enregistré pour la {vote_choice} dans la {category_choice} (par Admin) !")
            st.experimental_rerun()

# Vérification avant d'enregistrer un vote (utilisateur classique)
elif vote_choice != "Choisissez une option":
    if category_choice in st.session_state.votes_cast_categories:
        st.warning(f"Vous avez déjà voté pour une crèche dans la catégorie '{category_choice}'.")
    else:
        if st.button("Valider mon vote ✅"):
            st.session_state.votes[category_choice][vote_choice] += 1
            st.session_state.votes_cast_categories.add(category_choice)
            st.success(f"Merci pour votre vote pour la {vote_choice} dans la {category_choice} !")
            st.experimental_rerun()

# Résultats dynamiques réservés à l'administrateur
if admin_password == "Beaumont@2024":
    st.subheader("Résultats en temps réel")
    category_votes = st.session_state.votes[category_choice]
    if category_votes:
        sorted_votes = sorted(category_votes.items(), key=lambda x: x[1], reverse=True)
        st.write("### Classement final :")
        for rank, (nominee, votes) in enumerate(sorted_votes, start=1):
            st.write(f"**{rank}**. {nominee} - {votes} vote(s)")
    else:
        st.info("Aucun vote pour l'instant. Soyez le premier à voter !")
