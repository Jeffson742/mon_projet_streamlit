import streamlit as st
import pandas as pd  # Pour manipuler les données
import altair as alt
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
        # Préparer les données pour le CSV
        data = {
            'Numéro': [numero],
            'Conteneurs': [conteneurs],
            'Importateur': [importateur]
        }
        df = pd.DataFrame(data)  # Créer un DataFrame à partir des données

        try:
            # Ajouter les données au fichier CSV existant (sans écraser)
            df.to_csv('declarations.csv', mode='a', header=False, index=False)
        except FileNotFoundError:
            # Si le fichier n'existe pas, le créer avec un en-tête
            df.to_csv('declarations.csv', index=False)

        st.success(f"Déclaration {numero} enregistrée avec {conteneurs} conteneurs pour {importateur}.")
    else:
        st.error("Veuillez remplir tous les champs.")

st.header("Déclarations enregistrées")
try:
    # Lire les données depuis le fichier CSV
    df = pd.read_csv('declarations.csv', names=['Numéro', 'Conteneurs', 'Importateur'])
    st.dataframe(df)  # Afficher le tableau des données
except FileNotFoundError:
    st.write("Aucune déclaration enregistrée pour le moment.")

st.header("Télécharger les déclarations")
try:
    with open("declarations.csv", "r") as f:
        st.download_button(
            label="Télécharger le fichier CSV",
            data=f,
            file_name="declarations.csv",
            mime="text/csv"
        )
except FileNotFoundError:
    st.write("Aucun fichier CSV à télécharger pour le moment.")


st.header("Visualisation des données")
try:
    df = pd.read_csv('declarations.csv', names=['Numéro', 'Conteneurs', 'Importateur'])

    # Créer un graphique en barres
    chart = alt.Chart(df).mark_bar().encode(
        x='Importateur',
        y='Conteneurs',
        tooltip=['Numéro', 'Conteneurs', 'Importateur']
    )
    st.altair_chart(chart, use_container_width=True)
except FileNotFoundError:
    st.warning("Pas encore de données pour créer des visualisations.")
