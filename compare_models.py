
import pandas as pd

results = {
    "Model": [
        "Naive Bayes",
        "Logistic Regression",
        "SVM"
    ],
    "Accuracy (%)": [
        86.07,
        89.55,
        89.25
    ]
}

df = pd.DataFrame(results)

df = df.sort_values(
    by="Accuracy (%)",
    ascending=False
)

print("\nMODEL COMPARISON")
print(df.to_string(index=False))

df.to_csv("model_comparison.csv", index=False)

print("\nComparison saved successfully!")
