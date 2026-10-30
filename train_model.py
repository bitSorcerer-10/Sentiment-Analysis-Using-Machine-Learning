
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("cleaned_IMDB_Dataset.csv")

X = df["cleaned_review"]
y = df["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

svm_model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=10000)),
    ("classifier", LinearSVC())
])

print("Training SVM model...")

svm_model.fit(X_train, y_train)

y_pred = svm_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nSVM RESULTS")
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

joblib.dump(svm_model, "svm_model.joblib")

print("Model saved successfully!")
