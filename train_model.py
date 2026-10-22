
import random
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

random.seed(42)

def assign_label(loops, nesting, recursion, log_calls):
    # Heuristic labels for a prototype dataset.
    # These are not verified complexity annotations.
    if nesting >= 2:
        return "Quadratic"
    if recursion:
        return "Linear"
    if log_calls and loops == 0:
        return "Logarithmic"
    if loops >= 1:
        return "Linear"
    return "Constant"

rows = []

# Generate examples for a prototype.
for _ in range(1500):
    loops = random.randint(0, 4)
    nesting = random.randint(0, 3)
    recursion = random.randint(0, 1)
    log_calls = random.randint(0, 1)

    label = assign_label(
        loops, nesting, recursion, log_calls
    )

    rows.append({
        "loop_count": loops,
        "max_nesting": nesting,
        "has_recursion": recursion,
        "has_log_call": log_calls,
        "complexity": label
    })

df = pd.DataFrame(rows)
df.to_csv("training_data.csv", index=False)

X = df.drop(columns=["complexity"])
y = df["complexity"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Prototype model evaluation")
print("Accuracy:", round(accuracy_score(
    y_test, predictions
), 3))
print(classification_report(y_test, predictions))

joblib.dump(model, "complexity_model.pkl")

print("Training data saved: training_data.csv")
print("Model saved: complexity_model.pkl")
