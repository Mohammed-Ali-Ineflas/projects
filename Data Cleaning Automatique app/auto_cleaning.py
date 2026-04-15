import streamlit as st
import pandas as pd

# 1. Configuration dyal l'interface
st.set_page_config(page_title="Data Cleaner Pro", page_icon="🧹", layout="wide")

st.title("Data Cleaner Express 🧹")
st.write("Outil rapide bach tn9i les fichiers CSV dyalek en un clic.")

# 2. Upload dyal l'fichier
uploaded_file = st.file_uploader("Lo7 l'fichier CSV dyalek hna", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Fichier tcharja b naja7!")
        
        # Aperçu (Avant)
        st.subheader("Aperçu dyal les données (Avant)")
        st.write(f"**Lignes :** {df.shape[0]} | **Colonnes :** {df.shape[1]}")
        st.dataframe(df.head())
        
        # 3. Les Options dyal Nettoyage
        st.subheader("⚙️ Options de Nettoyage")
        
        # Option 1: Doublons
        drop_duplicates = st.checkbox("Supprimer les lignes en double (Doublons)")
        
        # Option 2: Les valeurs manquantes (Radio button bach khtar 7aja we7da)
        na_action = st.radio(
            "Kifach bghiti t-gérer les valeurs manquantes (NaN) ?",
            ["Ne rien faire", 
             "Supprimer les lignes (Perte de données)", 
             "Remplacer par la moyenne (Uniquement colonnes numériques)"]
        )
            
        # 4. L'Action dyal Nettoyage
        if st.button("Lancer le nettoyage 🚀"):
            df_clean = df.copy()
            
            # Traitement dyal Doublons
            if drop_duplicates:
                df_clean = df_clean.drop_duplicates()
                
            # Traitement dyal l'khawi (NaN)
            if na_action == "Supprimer les lignes (Perte de données)":
                df_clean = df_clean.dropna()
            elif na_action == "Remplacer par la moyenne (Uniquement colonnes numériques)":
                # Kanjebdo ghir les colonnes li fihom ar9am
                numeric_cols = df_clean.select_dtypes(include=['number']).columns
                # Kan3emro lkhawi fihom b la moyenne dyal kola colonne
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
                
            st.subheader("✨ Aperçu dyal les données (Après)")
            st.write(f"**Lignes restantes :** {df_clean.shape[0]}")
            st.dataframe(df_clean.head())
            
            # 5. Export dyal l'fichier n9i
            csv = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Télécharger le fichier nettoyé",
                data=csv,
                file_name="data_nettoyee.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"W9e3 mochkil f l9raya dyal l'fichier. L'erreur: {e}")