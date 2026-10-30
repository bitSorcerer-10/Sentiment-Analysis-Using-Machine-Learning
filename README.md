# Sentiment Analysis Project

**IMDb Movie Review Sentiment Classification Using Machine Learning**

## 1. About the Project

This project uses Machine Learning to classify movie reviews as **Positive** or **Negative** based on their text.

It uses the IMDb dataset containing 50,000 movie reviews.

## 2. Technologies Used

- Python
- Pandas, NumPy
- Scikit-learn
- NLTK
- Matplotlib, Seaborn
- WordCloud
- Streamlit

## 3. Machine Learning Models

Three models were trained and compared:

| Model | Accuracy |
|---|---:|
| Naive Bayes | 86.07% |
| Logistic Regression | 89.55% |
| SVM | 89.25% |

**Best Model:** Logistic Regression (89.55%)

## 4. Project Features

- Text preprocessing
- Data visualization
- Model training and comparison
- Model evaluation using a confusion matrix
- Interactive Streamlit web application
- Positive and negative sentiment prediction

## 5. How to Run

**Step 1:** Clone or download this project.

**Step 2:** Open the project folder in VS Code.

**Step 3:** Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

**Step 4:** Install dependencies:

```bash
pip install -r requirements.txt
```

**Step 5:** Run the application:

```bash
streamlit run app.py
```

The application will open in your browser. Enter a movie review to get its sentiment prediction.

## 6. Dataset

IMDb 50K Movie Reviews Dataset:
- 25,000 positive reviews
- 25,000 negative reviews

## 7. Conclusion

This project demonstrates the use of Machine Learning and Natural Language Processing for sentiment classification of movie reviews.