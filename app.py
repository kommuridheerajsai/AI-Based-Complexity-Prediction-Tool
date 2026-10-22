
import ast
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Complexity Predictor",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI-Based Complexity Prediction Tool")
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

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if (
                        isinstance(child.func, ast.Name)
                        and child.func.id == node.name
                    ):
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


# Load the trained model
try:
    model = load_model()
except FileNotFoundError:
    st.error(
        "Model not found. Please run train_model.py first."
    )
    st.stop()
except Exception as error:
    st.error(f"Unable to load model: {error}")
    st.stop()


# Code input
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
            # Extract features
            features = extract_features(code)
            X = pd.DataFrame([features])

            # Predict complexity category
            prediction = model.predict(X)[0]

            # Convert category to Big-O notation
            complexity_map = {
                "Constant": "O(1)",
                "Logarithmic": "O(log n)",
                "Linear": "O(n)",
                "Quadratic": "O(n²)"
            }

            big_o = complexity_map.get(
                prediction, "Unknown"
            )

            explanations = {
                "Constant": (
                    "The estimated work remains constant "
                    "as input size increases."
                ),
                "Logarithmic": (
                    "The estimated work grows logarithmically "
                    "with input size."
                ),
                "Linear": (
                    "The estimated work grows proportionally "
                    "to input size."
                ),
                "Quadratic": (
                    "The estimated work may grow proportionally "
                    "to the square of input size."
                )
            }

            # Display results
            st.subheader("📊 Complexity Prediction")

            st.metric(
                label="Predicted Time Complexity",
                value=big_o
            )

            st.success(
                f"Predicted Category: {prediction}"
            )

            st.write(
                explanations.get(
                    prediction,
                    "No explanation available."
                )
            )

            # Show extracted features in a collapsible section
            with st.expander("View Extracted Code Features"):
                st.dataframe(
                    X,
                    use_container_width=True
                )

            st.warning(
                "This is an experimental ML estimate. "
                "The model uses synthetic training data and "
                "simple code features. Its prediction may not "
                "match the actual Big-O complexity."
            )

        except SyntaxError:
            st.error(
                "Invalid Python syntax. Please correct your code."
            )

        except Exception as error:
            st.error(f"Prediction failed: {error}")
