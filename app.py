
import ast
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Complexity Predictor",
    page_icon="🤖",
    layout="centered"
)

st.title("AI-Based Complexity Prediction Tool")
st.write(
    "Enter Python code to estimate its time-complexity category."
)

@st.cache_resource
def load_model():
    return joblib.load("complexity_model.pkl")

def extract_features(code):
    tree = ast.parse(code)

    loop_count = 0
    max_nesting = 0
    has_recursion = 0
    has_log_call = 0

    def visit(node, depth=0):
        nonlocal loop_count, max_nesting
        nonlocal has_recursion, has_log_call

        if isinstance(node, (ast.For, ast.While)):
            loop_count += 1
            depth += 1
            max_nesting = max(max_nesting, depth)

        if isinstance(node, ast.Call):
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr

            if name in ("log2", "bisect_left", "bisect_right"):
                has_log_call = 1

        if isinstance(node, ast.FunctionDef):
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if (isinstance(child.func, ast.Name)
                            and child.func.id == node.name):
                        has_recursion = 1

        for child in ast.iter_child_nodes(node):
            visit(child, depth)

    visit(tree)

    return {
        "loop_count": loop_count,
        "max_nesting": max_nesting,
        "has_recursion": has_recursion,
        "has_log_call": has_log_call
    }

try:
    model = load_model()
except FileNotFoundError:
    st.error("Model not found. Run train_model.py first.")
    st.stop()

code = st.text_area(
    "Enter your Python code",
    height=220,
    placeholder=(
        "for i in range(n):\n"
        "    print(i)"
    )
)

if st.button("Predict Complexity", type="primary"):
    if not code.strip():
        st.warning("Please enter some Python code.")
    else:
        try:
            features = extract_features(code)
            X = pd.DataFrame([features])

            prediction = model.predict(X)[0]

            st.subheader("Prediction Result")
            st.success(f"Predicted category: {prediction}")

            st.write("Extracted code features:")
            st.dataframe(X, use_container_width=True)

            st.info(
                "This is an experimental ML estimate. "
                "The model uses a synthetic training dataset "
                "and simple structural features, so its "
                "prediction may be incorrect."
            )

        except SyntaxError:
            st.error("The code contains a Python syntax error.")
