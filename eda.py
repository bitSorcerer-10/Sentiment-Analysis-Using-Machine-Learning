
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load cleaned dataset
df = pd.read_csv("cleaned_IMDB_Dataset.csv")

# Calculate review length
df["review_length"] = df["cleaned_review"].apply(
    lambda x: len(str(x).split())
)

# 1. Sentiment distribution
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="sentiment")
plt.title("Positive vs Negative Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.savefig("sentiment_distribution.png")
plt.show()

# 2. Review length distribution
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="review_length", bins=50)
plt.title("Review Length Distribution")
plt.xlabel("Number of Words")
plt.ylabel("Frequency")
plt.savefig("review_length.png")
plt.show()

# 3. Word clouds
positive_text = " ".join(
    df[df["sentiment"] == "positive"]["cleaned_review"].astype(str)
)

negative_text = " ".join(
    df[df["sentiment"] == "negative"]["cleaned_review"].astype(str)
)

positive_wc = WordCloud(
    width=800, height=400, background_color="white"
).generate(positive_text)

negative_wc = WordCloud(
    width=800, height=400, background_color="white"
).generate(negative_text)

plt.figure(figsize=(10, 5))
plt.imshow(positive_wc, interpolation="bilinear")
plt.axis("off")
plt.title("Positive Reviews Word Cloud")
plt.savefig("positive_wordcloud.png")
plt.show()

plt.figure(figsize=(10, 5))
plt.imshow(negative_wc, interpolation="bilinear")
plt.axis("off")
plt.title("Negative Reviews Word Cloud")
plt.savefig("negative_wordcloud.png")
plt.show()

print("EDA completed successfully!")
print("\nAverage review length:")
print(df.groupby("sentiment")["review_length"].mean())
