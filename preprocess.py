
import pandas as pd
import re
import nltk

from nltk.corpus import stopwords

# Load dataset
df = pd.read_csv("IMDB Dataset.csv")

# Load English stopwords
stop_words = set(stopwords.words("english"))

# Preserve important negation words
negation_words = {"not", "no", "nor", "never"}
stop_words = stop_words - negation_words
# Function to clean reviews
def clean_text(text):

    # Convert text to lowercase
    text = text.lower()

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)


# Apply cleaning to all reviews
df["cleaned_review"] = df["review"].apply(clean_text)

# Display original and cleaned reviews
print("ORIGINAL REVIEW:")
print(df["review"][0])

print("\nCLEANED REVIEW:")
print(df["cleaned_review"][0])

# Save processed dataset
df.to_csv("cleaned_IMDB_Dataset.csv", index=False)

print("\nPreprocessing completed successfully!")
print("Cleaned dataset saved.")
