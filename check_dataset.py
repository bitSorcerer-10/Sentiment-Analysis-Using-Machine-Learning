import pandas as pd

# Load IMDb dataset
df = pd.read_csv("IMDB Dataset.csv")

print("FIRST FIVE REVIEWS:")
print(df.head())

print("\nDATASET SHAPE:")
print(df.shape)

print("\nDATASET INFORMATION:")
df.info()

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nSENTIMENT DISTRIBUTION:")
print(df["sentiment"].value_counts())