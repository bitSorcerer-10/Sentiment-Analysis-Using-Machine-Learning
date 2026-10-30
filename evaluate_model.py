
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Load dataset
df = pd.read_csv("cleaned_IMDB_Dataset.csv")

X = df["cleaned_review"]
y = df["sentiment"]

# Use the same test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Load trained Logistic Regression model
model = joblib.load("logistic_regression_model.joblib")

# Make predictions
y_pred = model.predict(X_test)

# Create confusion matrix
cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["negative", "positive"]
)

print("Confusion Matrix:")
print(cm)

# Visualize confusion matrix
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Negative", "Positive"]
)

disp.plot(cmap="Blues", values_format="d")
plt.title("Logistic Regression - Confusion Matrix")
plt.savefig("confusion_matrix.png")
plt.show()

print("Confusion matrix saved successfully!")
