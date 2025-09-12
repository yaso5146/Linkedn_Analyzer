import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# CSV dosyasını oku
df = pd.read_csv("profiles.csv")

# Skills sütununu listeye çevir
df['skills_list'] = df['skills'].apply(lambda x: x.split(','))

# Örnek: tüm isimleri ve becerilerini yazdır
for index, row in df.iterrows():
    print("İsim:", row['name'])
    print("Başlık:", row['title'])
    print("Beceriler:", row['skills_list'])
    print("---")

all_skills = [skill for sublist in df['skills_list'] for skill in sublist]
skill_counts = Counter(all_skills)

print("En çok geçen beceriler:")
for skill, count in skill_counts.most_common():
    print(skill, count)

skills, counts = zip(*skill_counts.most_common())
plt.bar(skills, counts)
plt.xticks(rotation=45)
plt.title("En Popüler Beceriler")
plt.show()