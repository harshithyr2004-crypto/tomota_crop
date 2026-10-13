# ============================================================
# CROP RECOMMENDATION MACHINE LEARNING PROJECT
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 2. LOAD DATASET
# ============================================================

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_csv("cp.csv")

print("\nDataset loaded successfully!")

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# 3. BASIC DATA ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("BASIC DATA ANALYSIS")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())


# ============================================================
# 4. CHECK MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing_values = df.isnull().sum()

print(missing_values)

if missing_values.sum() == 0:
    print("\nNo missing values found.")
else:
    print("\nMissing values exist in the dataset.")


# ============================================================
# 5. CHECK DUPLICATES
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE RECORDS")
print("=" * 60)

duplicates = df.duplicated().sum()

print("Number of duplicate rows:", duplicates)

if duplicates > 0:
    df = df.drop_duplicates()
    print("Duplicate rows removed.")

print("Dataset shape after duplicate removal:", df.shape)


# ============================================================
# 6. TARGET VARIABLE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("CROP DISTRIBUTION")
print("=" * 60)

crop_counts = df["label"].value_counts()

print(crop_counts)

print("\nNumber of different crops:")
print(df["label"].nunique())


# ============================================================
# 7. CROP DISTRIBUTION GRAPH
# ============================================================

plt.figure(figsize=(14, 6))

sns.countplot(
    data=df,
    x="label"
)

plt.xticks(rotation=90)

plt.title("Crop Distribution")

plt.xlabel("Crop")

plt.ylabel("Number of Samples")

plt.tight_layout()

plt.show()


# ============================================================
# 8. HISTOGRAMS
# ============================================================

print("\nDisplaying feature distributions...")

df.drop(columns=["label"]).hist(
    figsize=(14, 10),
    bins=20
)

plt.suptitle("Feature Distributions")

plt.tight_layout()

plt.show()


# ============================================================
# 9. CORRELATION MATRIX
# ============================================================

print("\nDisplaying correlation matrix...")

plt.figure(figsize=(10, 7))

correlation = df.drop(columns=["label"]).corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Feature Correlation Matrix")

plt.tight_layout()

plt.show()


# ============================================================
# 10. BOXPLOTS
# ============================================================

plt.figure(figsize=(14, 8))

sns.boxplot(
    data=df.drop(columns=["label"])
)

plt.title("Feature Boxplots")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 11. SEPARATE FEATURES AND TARGET
# ============================================================

print("\n" + "=" * 60)
print("FEATURE SELECTION")
print("=" * 60)

X = df.drop(columns=["label"])

y = df["label"]

print("\nInput Features:")
print(X.columns.tolist())

print("\nTarget:")
print("label")


# ============================================================
# 12. TRAIN TEST SPLIT
# ============================================================

print("\n" + "=" * 60)
print("TRAIN TEST SPLIT")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", X_train.shape[0])

print("Testing samples:", X_test.shape[0])


# ============================================================
# 13. CREATE MODELS
# ============================================================

models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=300,
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "KNN": KNeighborsClassifier(
        n_neighbors=5
    ),

    "SVM": SVC(
        kernel="rbf",
        probability=True,
        random_state=42
    ),

    "Logistic Regression": LogisticRegression(
        max_iter=5000,
        random_state=42
    ),

    "Naive Bayes": GaussianNB()
}


# ============================================================
# 14. TRAIN ALL MODELS
# ============================================================

print("\n" + "=" * 60)
print("MODEL TRAINING")
print("=" * 60)

results = {}

trained_models = {}

for name, model in models.items():

    print("\nTraining:", name)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    results[name] = accuracy

    trained_models[name] = model

    print(
        "Accuracy:",
        round(accuracy * 100, 2),
        "%"
    )


# ============================================================
# 15. MODEL COMPARISON
# ============================================================

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

results_df = pd.DataFrame(
    list(results.items()),
    columns=["Model", "Accuracy"]
)

results_df = results_df.sort_values(
    by="Accuracy",
    ascending=False
)

results_df["Accuracy"] = (
    results_df["Accuracy"] * 100
)

print("\n")
print(results_df.to_string(index=False))


# ============================================================
# 16. MODEL COMPARISON GRAPH
# ============================================================

plt.figure(figsize=(12, 6))

sns.barplot(
    data=results_df,
    x="Accuracy",
    y="Model"
)

plt.title("Machine Learning Model Comparison")

plt.xlabel("Accuracy (%)")

plt.ylabel("Model")

plt.xlim(90, 100)

plt.tight_layout()

plt.show()


# ============================================================
# 17. SELECT BEST MODEL
# ============================================================

best_model_name = results_df.iloc[0]["Model"]

best_model = trained_models[best_model_name]

print("\n" + "=" * 60)
print("BEST MODEL")
print("=" * 60)

print("Best Model:", best_model_name)

print(
    "Accuracy:",
    round(
        results_df.iloc[0]["Accuracy"],
        2
    ),
    "%"
)


# ============================================================
# 18. FINAL PREDICTIONS
# ============================================================

y_pred = best_model.predict(X_test)


# ============================================================
# 19. CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ============================================================
# 20. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

plt.figure(figsize=(14, 11))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=best_model.classes_,
    yticklabels=best_model.classes_
)

plt.title(
    "Confusion Matrix - " + best_model_name
)

plt.xlabel("Predicted Crop")

plt.ylabel("Actual Crop")

plt.xticks(rotation=90)

plt.yticks(rotation=0)

plt.tight_layout()

plt.show()


# ============================================================
# 21. FEATURE IMPORTANCE
# ============================================================

if hasattr(best_model, "feature_importances_"):

    feature_importance = pd.Series(
        best_model.feature_importances_,
        index=X.columns
    )

    feature_importance = feature_importance.sort_values(
        ascending=False
    )

    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE")
    print("=" * 60)

    print(feature_importance)


    # Feature importance graph

    plt.figure(figsize=(10, 6))

    feature_importance.sort_values().plot(
        kind="barh"
    )

    plt.title(
        "Feature Importance - " + best_model_name
    )

    plt.xlabel("Importance")

    plt.ylabel("Feature")

    plt.tight_layout()

    plt.show()


# ============================================================
# 22. SAVE THE TRAINED MODEL
# ============================================================

model_filename = "crop_recommendation_model.pkl"

joblib.dump(
    best_model,
    model_filename
)

print("\n" + "=" * 60)
print("MODEL SAVED")
print("=" * 60)

print(
    "Model saved as:",
    model_filename
)


# ============================================================
# 23. LOAD THE SAVED MODEL
# ============================================================

loaded_model = joblib.load(
    model_filename
)

print("\nSaved model loaded successfully!")


# ============================================================
# 24. NEW CROP PREDICTION
# ============================================================

print("\n" + "=" * 60)
print("NEW CROP PREDICTION")
print("=" * 60)


# Example input

new_data = pd.DataFrame({

    "N": [90],

    "P": [42],

    "K": [43],

    "temperature": [20.87],

    "humidity": [82.00],

    "ph": [6.50],

    "rainfall": [202.93]

})


print("\nInput values:")

print(new_data)


# Predict crop

prediction = loaded_model.predict(
    new_data
)

print("\nRecommended Crop:")

print(
    prediction[0]
)


# ============================================================
# 25. PREDICTION PROBABILITY
# ============================================================

if hasattr(
    loaded_model,
    "predict_proba"
):

    probabilities = loaded_model.predict_proba(
        new_data
    )[0]

    probability_df = pd.DataFrame({

        "Crop": loaded_model.classes_,

        "Probability": probabilities

    })

    probability_df = probability_df.sort_values(
        by="Probability",
        ascending=False
    )

    print("\n" + "=" * 60)
    print("TOP 5 CROP PREDICTIONS")
    print("=" * 60)

    print(
        probability_df.head(5).to_string(
            index=False
        )
    )


# ============================================================
# 26. FINISHED
# ============================================================

print("\n" + "=" * 60)
print("PROGRAM COMPLETED")
print("=" * 60)

print("\nYour crop recommendation model is ready!")