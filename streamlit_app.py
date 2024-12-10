import streamlit as st

# Titre de l'application
st.title("Ma première application Streamlit 🚀")
st.write("Bienvenue dans mon application interactive 🎉")

# Formulaire d'entrée
st.header("Saisissez vos informations :")
numero = st.text_input("Numéro de déclaration")
conteneurs = st.number_input("Nombre de conteneurs", min_value=1, step=1)
importateur = st.text_input("Nom de l'importateur")

if st.button("Soumettre"):
    if numero and importateur:
        st.success(f"Déclaration {numero} enregistrée avec {conteneurs} conteneurs pour {importateur}.")
    else:
        st.error("Veuillez remplir tous les champs.")
