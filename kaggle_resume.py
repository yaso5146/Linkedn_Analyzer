import pandas as pd

df = pd.read_csv("resume_data.csv", encoding="utf-8")
print(df["extra_curricular_activity_types"])
