import streamlit as st

st.set_page_config(
    page_title="Python Calculator",
    page_icon="🐍",
    layout="centered"
)

# -----------------------------
# CSS
# -----------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

.calculator-title {
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 25px;
}

.result {
    background: #020617;
    color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: right;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 20px;
}

div.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    border: none;
    font-size: 20px;
    font-weight: bold;
    background: #334155;
    color: white;
}

div.stButton > button:hover {
    background: #475569;
    color: white;
}

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "result" not in st.session_state:
    st.session_state.result = ""

# -----------------------------
# Calculator Function
# -----------------------------

def calculate():

    expression = st.session_state.expression

    allowed = "0123456789+-*/(). "

    if not expression:
        return

    if not all(char in allowed for char in expression):
        st.session_state.result = "Error"
        return

    try:
        answer = eval(
            expression,
            {"__builtins__": None},
            {}
        )

        st.session_state.result = str(answer)

    except:
        st.session_state.result = "Error"


# -----------------------------
# Title
# -----------------------------

st.markdown(
    '<div class="calculator-title">🐍 Python Calculator</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Display
# -----------------------------

display = (
    st.session_state.result
    if st.session_state.result
    else st.session_state.expression
)

st.markdown(
    f'<div class="result">{display or "0"}</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Buttons
# -----------------------------

rows = [
    ["C", "(", ")", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", "⌫"]
]

for row in rows:

    columns = st.columns(4)

    for i, button in enumerate(row):

        with columns[i]:

            if st.button(button, key=button):

                if button == "C":

                    st.session_state.expression = ""
                    st.session_state.result = ""

                elif button == "=":

                    calculate()

                elif button == "⌫":

                    st.session_state.expression = (
                        st.session_state.expression[:-1]
                    )

                    st.session_state.result = ""

                else:

                    st.session_state.expression += button
                    st.session_state.result = ""

                st.rerun()

# -----------------------------
# Footer
# -----------------------------

st.markdown(
    '<div class="footer">Made with Python 🐍</div>',
    unsafe_allow_html=True
)
