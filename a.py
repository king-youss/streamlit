import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Créer la connexion à la base de données SQLite
conn = sqlite3.connect('questionnaire.db')
cursor = conn.cursor()

# Fonction pour créer la table questionnaire_responses
def create_table():
    global cursor
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questionnaire_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INT,
            gender TEXT,
            pet_preference TEXT
        )
    ''')
    conn.commit()

# Fonction pour insérer des données dans la base de données
def insert_data(name, age, gender, pet_preference):
    cursor.execute('''
        INSERT INTO questionnaire_responses (name, age, gender, pet_preference)
        VALUES (?, ?, ?, ?)
    ''', (name, age, gender, pet_preference))
    conn.commit()

# Fonction pour supprimer une réponse de la base de données par ID
def delete_response_by_id(response_id):
    cursor.execute('SELECT * FROM questionnaire_responses WHERE id=?', (response_id,))
    data = cursor.fetchone()

    if data:
        cursor.execute('DELETE FROM questionnaire_responses WHERE id=?', (response_id,))
        conn.commit()
        st.warning(f"🗑️ Réponse avec l'ID {response_id} a été supprimée!")
    else:
        st.warning(f"❌ Aucune réponse trouvée avec l'ID {response_id}!")

# Fonction pour supprimer toutes les réponses de la base de données
def delete_all_responses():
    cursor.execute('DELETE FROM questionnaire_responses')
    conn.commit()

# Fonction pour afficher les réponses stockées
def display_responses():
    st.title("Réponses enregistrées dans la base de données")
    responses = pd.read_sql_query('SELECT * FROM questionnaire_responses', conn)

    if responses.empty:
        st.info("Aucune réponse enregistrée pour le moment.")
    else:
        st.table(responses)

# Fonction pour afficher un histogramme de la répartition des âges
def display_age_histogram():
    st.header("Répartition des âges")
    responses = pd.read_sql_query('SELECT * FROM questionnaire_responses', conn)

    if not responses.empty:
        plt.figure(figsize=(10, 6))
        sns.histplot(responses['age'], bins=20, kde=True)
        plt.title("Histogramme de la Répartition des Âges")
        plt.xlabel("Âge")
        plt.ylabel("Nombre de Réponses")
        st.pyplot()

# Fonction pour afficher un graphique circulaire des préférences d'animaux
def display_pet_preference_pie_chart():
    st.header("Préférences d'Animaux")
    responses = pd.read_sql_query('SELECT * FROM questionnaire_responses', conn)

    if not responses.empty:
        pet_counts = responses['pet_preference'].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(pet_counts, labels=pet_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        plt.title("Répartition des Préférences d'Animaux")
        st.pyplot()

# Fonction pour filtrer les réponses par genre
def filter_responses_by_gender():
    st.header("Filtrer les Réponses par Genre")
    gender_to_filter = st.selectbox("Sélectionner le genre à filtrer:", ["Homme", "Femme", "Autre"])
    
    filtered_responses = pd.read_sql_query(f'SELECT * FROM questionnaire_responses WHERE gender="{gender_to_filter}"', conn)
    
    if filtered_responses.empty:
        st.info(f"Aucune réponse trouvée pour le genre {gender_to_filter}.")
    else:
        st.table(filtered_responses)

# Fonction pour afficher les statistiques générales
def display_general_statistics():
    st.header("Statistiques Générales")
    responses = pd.read_sql_query('SELECT * FROM questionnaire_responses', conn)

    if not responses.empty:
        average_age = responses['age'].mean()
        st.write(f"Moyenne d'âge : {average_age:.2f} ans")

        gender_distribution = responses['gender'].value_counts()
        st.bar_chart(gender_distribution)

# Styles pour l'apparence
st.set_page_config(
    page_title="Questionnaire App",
    page_icon="📝",
    layout="wide"
)

# Interface utilisateur Streamlit
st.title("📝 Questionnaire")
st.markdown("---")  # Ligne horizontale

# Sidebar pour les options
st.sidebar.title("Options")

# Informations sur l'application
st.sidebar.info(
    "Bienvenue dans l'application Questionnaire. "
    "Utilisez la barre latérale pour explorer différentes options."
)

# Liens utiles
st.sidebar.markdown("### Liens Utiles")
st.sidebar.markdown("[Documentation Streamlit](https://docs.streamlit.io/)")
st.sidebar.markdown("[GitHub Repository](https://github.com/votre-nom/questionnaire-app)")

# Section Collecte des réponses
st.header("Collecte des réponses")
st.markdown("---")  # Ligne horizontale

# Utilisation de boîtes pour organiser la mise en page
col1, col2, col3, col4 = st.columns(4)

with col1:
    name = st.text_input("Nom:")

with col2:
    age = st.number_input("Âge:", min_value=1, max_value=100, value=1)

with col3:
    gender = st.radio("Genre:", ["Homme", "Femme", "Autre"])

with col4:
    pet_preference = st.selectbox("Préférence d'animal de compagnie:", ["Chien", "Chat", "Poisson", "Autre"])

# Bouton pour soumettre les réponses
if st.button("Soumettre"):
    create_table()
    insert_data(name, age, gender, pet_preference)
    st.success("✅ Réponses soumises avec succès!")

# Section Supprimer une réponse par ID
st.header("Supprimer une réponse par ID")
st.markdown("---")  # Ligne horizontale

response_id = st.number_input("ID de la réponse à supprimer:", min_value=1, value=1)

if st.button("Supprimer la réponse par ID"):
    delete_response_by_id(response_id)

# Section Supprimer toutes les réponses
st.header("Gestion des réponses")
st.markdown("---")  # Ligne horizontale

if st.button("Supprimer toutes les réponses"):
    delete_all_responses()
    st.warning("🗑️ Toutes les réponses ont été supprimées!")

# Section Afficher les réponses stockées
st.header("Afficher les réponses stockées")
st.markdown("---")  # Ligne horizontale
display_responses()

# Section Statistiques
st.header("Statistiques")
st.markdown("---")  # Ligne horizontale

# Boutons pour afficher les statistiques
if st.button("Répartition des Âges"):
    display_age_histogram()

if st.button("Préférences d'Animaux"):
    display_pet_preference_pie_chart()

if st.button("Statistiques Générales"):
    display_general_statistics()

# Section Filtrer par Genre
st.header("Filtrer les Réponses par Genre")
st.markdown("---")  # Ligne horizontale

filter_responses_by_gender()

# Fermer la connexion à la base de données à la fin
conn.close()
