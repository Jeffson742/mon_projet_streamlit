import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt
from fpdf import FPDF

# Titre de l'application
st.title("JSL Distribution : Votre partenaire de confiance pour un dédouanement rapide et efficace.")
st.write("Bienvenue dans notre application interactive 🎉")

# Formulaire d'entrée
st.header("Saisissez vos informations :")
numero = st.text_input("Numéro de déclaration")
conteneurs = st.number_input("Nombre de conteneurs", min_value=1, step=1)
importateur = st.text_input("Nom de l'importateur")

# Sélection des dates de la période
st.subheader("Sélectionnez la période")
start_date = st.date_input("Date de début de la période", value=datetime(2024, 10, 28).date())
end_date = st.date_input("Date de fin de la période", value=datetime(2024, 12, 15).date())

# Validation des dates
if start_date > end_date:
    st.error("La date de début doit être antérieure ou égale à la date de fin.")

# Soumission des données
if st.button("Soumettre"):
    if numero and importateur and start_date and end_date:
        # Préparer les données pour le CSV
        periode = f"{start_date.strftime('%d %B %Y')} - {end_date.strftime('%d %B %Y')}"
        data = {
            'Numéro': [numero],
            'Conteneurs': [conteneurs],
            'Importateur': [importateur],
            'Date': [datetime.now().strftime('%Y-%m-%d')],
            'Période': [periode]
        }
        df = pd.DataFrame(data)

        try:
            # Ajouter les données au fichier CSV existant
            df.to_csv('declarations.csv', mode='a', header=False, index=False)
        except FileNotFoundError:
            # Créer le fichier avec les en-têtes si inexistant
            df.to_csv('declarations.csv', index=False)

        st.success(f"Déclaration {numero} enregistrée avec succès pour {importateur} sous la période '{periode}'.")
    else:
        st.error("Veuillez remplir tous les champs.")

# Section : Déclarations enregistrées
st.header("Déclarations enregistrées")
try:
    # Lire les données depuis le fichier CSV
    df = pd.read_csv('declarations.csv', names=['Numéro', 'Conteneurs', 'Importateur', 'Date', 'Période'])
    st.dataframe(df)  # Afficher le tableau des données
except FileNotFoundError:
    st.write("Aucune déclaration enregistrée pour le moment.")

# Section : Totaux des déclarations et des conteneurs
st.header("Statistiques globales")
try:
    if not df.empty:
        total_declarations = len(df)  # Total des déclarations
        total_conteneurs = df['Conteneurs'].sum()  # Total des conteneurs

        # Afficher les statistiques
        st.write(f"### Total des déclarations : {total_declarations}")
        st.write(f"### Total des conteneurs : {total_conteneurs}")
except FileNotFoundError:
    st.warning("Aucune donnée enregistrée pour le moment.")

# Section : Générer des fichiers CSV par importateur
st.header("Générer des fichiers CSV par importateur")
try:
    if not df.empty:
        importateurs = df['Importateur'].unique()
        selected_importateur = st.selectbox("Choisissez un importateur :", importateurs)

        # Filtrer les données pour l'importateur sélectionné
        filtered_by_importer = df[df['Importateur'] == selected_importateur]

        # Télécharger le fichier CSV de l'importateur
        csv_importer = filtered_by_importer.to_csv(index=False)
        st.download_button(
            label=f"Télécharger les données pour {selected_importateur} (CSV)",
            data=csv_importer,
            file_name=f'declarations_{selected_importateur}.csv',
            mime='text/csv'
        )
except KeyError:
    st.write("Aucune donnée disponible pour les importateurs.")

# Section : Générer des fichiers PDF par importateur et période
st.header("Générer des fichiers PDF par importateur et période")
try:
    if not df.empty:
        selected_importateur_pdf = st.selectbox("Choisissez un importateur pour le PDF :", importateurs)

        # Filtrer les données par importateur
        filtered_by_importer_pdf = df[df['Importateur'] == selected_importateur_pdf]

        # Générer un PDF pour l'importateur et la période sélectionnés
        if st.button(f"Générer un PDF pour {selected_importateur_pdf}"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt=f"Déclarations pour {selected_importateur_pdf}", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Période : {start_date.strftime('%d %B %Y')} - {end_date.strftime('%d %B %Y')}", ln=True, align="C")

            for index, row in filtered_by_importer_pdf.iterrows():
                pdf.cell(200, 10, txt=f"Numéro : {row['Numéro']}, Conteneurs : {row['Conteneurs']}, Date : {row['Date']}", ln=True)

            # Sauvegarder le PDF
            pdf_output = f"declarations_{selected_importateur_pdf}_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}.pdf"
            pdf.output(pdf_output)

            with open(pdf_output, "rb") as file:
                st.download_button(
                    label=f"Télécharger le PDF pour {selected_importateur_pdf}",
                    data=file,
                    file_name=pdf_output,
                    mime="application/pdf"
                )
except KeyError:
    st.write("Aucune donnée disponible pour générer des PDF.")

# Section : Visualisation des données
st.header("Visualisation des données")
try:
    chart = alt.Chart(df).mark_bar().encode(
        x='Importateur',
        y='Conteneurs',
        tooltip=['Numéro', 'Conteneurs', 'Importateur', 'Période']
    )
    st.altair_chart(chart, use_container_width=True)
except FileNotFoundError:
    st.warning("Pas encore de données pour créer des visualisations.")
