import streamlit as st
import requests
import os 

API_URL = os.get('API_URL')
# Titre de l'application avec un style personnalisé
st.markdown("<h1 style='text-align: center; color: blue;'>Formulaire de Contact</h1>", unsafe_allow_html=True)

# Création du formulaire
with st.form(key='email_form'):
    st.markdown("### Informations Personnelles")
    first_name = st.text_input('Prénom')
    last_name = st.text_input('Nom de famille')
    email = st.text_input('Email')
    phone = st.text_input('Numéro de téléphone')

    st.markdown("### Détails du Message")
    subject = st.selectbox('Sujet', ['Demande d\'information', 'Support technique', 'Retour d\'expérience', 'Autre'])
    message = st.text_area('Message')

    # Bouton de soumission
    submit_button = st.form_submit_button(label='Envoyer', help='Cliquez pour envoyer votre message')

# Quand le formulaire est soumis
if submit_button:
    # Vérifier que tous les champs obligatoires sont remplis
    if first_name and last_name and email and message:
        # Créer le payload pour la requête POST
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }

        # Envoyer la requête POST à l'API
        response = requests.post(API_URL, json=payload)

        # Vérifier la réponse de l'API
        if response.status_code == 200:
            st.success('Vos réponses ont bien été enregistrées')
        else:
            st.error('Erreur lors de l\'envoi de l\'email.')
    else:
        st.error('Veuillez remplir tous les champs obligatoires du formulaire (Prénom, Nom de famille, Email, Message).')

# Ajout d'une note en bas de page
st.markdown("<footer style='text-align: center; color: gray;'>Merci de nous avoir contacté. Nous vous répondrons dès que possible.</footer>", unsafe_allow_html=True)
