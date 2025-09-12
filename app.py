import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

st.title("🔎 LinkedIn Profil Analizi")

# CSV yükleme
uploaded_file = st.file_uploader("Profil verilerini yükle (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Skills sütununu listeye çevir
    df['skills_list'] = df['skills'].apply(lambda x: x.split(','))

    st.subheader("📋 Yüklenen Profiller")
    st.write(df[['name', 'title', 'skills']])

    # 🔎 Filtreleme & Arama
    st.subheader("🔎 Profil Arama")

    search_title = st.text_input("İş unvanına göre ara (ör: Data Scientist)")
    search_skill = st.text_input("Becerilere göre ara (ör: Python)")

    filtered_df = df.copy()

    if search_title:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False, na=False)]

    if search_skill:
        filtered_df = filtered_df[filtered_df['skills'].str.contains(search_skill, case=False, na=False)]

    st.write(filtered_df[['name', 'title', 'skills']])


    # Tüm becerileri topla
    all_skills = [skill.strip() for sublist in df['skills_list'] for skill in sublist]
    skill_counts = Counter(all_skills)

    # En popüler beceriler
    st.subheader("🔥 En Popüler Beceriler")
    for skill, count in skill_counts.most_common(10):
        st.write(f"{skill}: {count}")

    # Grafik çiz
    st.subheader("📊 Beceriler Grafiği")
    skills, counts = zip(*skill_counts.most_common(10))
    fig, ax = plt.subplots()
    ax.bar(skills, counts)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("Lütfen bir CSV dosyası yükleyin.")
