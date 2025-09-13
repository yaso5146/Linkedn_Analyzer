import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

    st.subheader("👤 Profil Detayları")

    # Profil seçmek için dropdown
    profile_names = filtered_df['name'].tolist()
    selected_profile = st.selectbox("Profil seçin", profile_names)

    # Seçilen profilin bilgilerini göster
    if selected_profile:
        profile = filtered_df[filtered_df['name'] == selected_profile].iloc[0]
        
        st.markdown(f"**İsim:** {profile['name']}")
        st.markdown(f"**Başlık:** {profile['title']}")
        st.markdown(f"**Beceriler:** {', '.join(profile['skills_list'])}")

    st.subheader("☁️ Beceriler Word Cloud")

    # Filtrelenmiş dataframe kullanabiliriz, veya tüm profilleri kullan
    all_skills_filtered = [skill.strip() for sublist in filtered_df['skills_list'] for skill in sublist]
    skills_text = " ".join(all_skills_filtered)

    if skills_text:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(skills_text)
        
        fig_wc, ax_wc = plt.subplots(figsize=(10,5))
        ax_wc.imshow(wordcloud, interpolation='bilinear')
        ax_wc.axis('off')
        
        st.pyplot(fig_wc)
    else:
        st.info("Word Cloud için yeterli beceri bulunamadı.")


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
