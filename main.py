import streamlit as st
import ast
import operator
import re

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="CircleCalc",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# STATE
# ============================================================

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "display" not in st.session_state:
    st.session_state.display = "0"

# ============================================================
# SAFE CALCULATOR
# ============================================================

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression):

    if not expression:
        return "0"

    # Convert percentage
    expression = re.sub(
        r"(\d+(?:\.\d+)?)%",
        r"(\1/100)",
        expression
    )

    try:

        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):

                if isinstance(node.value, (int, float)):
                    return node.value

                raise ValueError()

            if isinstance(node, ast.BinOp):

                left = evaluate(node.left)
                right = evaluate(node.right)

                operation = OPS.get(type(node.op))

                if operation is None:
                    raise ValueError()

                if isinstance(node.op, ast.Div) and right == 0:
                    raise ZeroDivisionError()

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):

                operation = OPS.get(type(node.op))

                if operation is None:
                    raise ValueError()

                return operation(evaluate(node.operand))

            raise ValueError()

        result = evaluate(tree)

        if isinstance(result, float):

            if result.is_integer():
                return str(int(result))

            return f"{result:.10f}".rstrip("0").rstrip(".")

        return str(result)

    except ZeroDivisionError:
        return "Error"

    except:
        return "Error"


# ============================================================
# BUTTON FUNCTION
# ============================================================

def button_press(value):

    # CLEAR
    if value == "C":

        st.session_state.expression = ""
        st.session_state.display = "0"
        return

    # DELETE
    if value == "DEL":

        st.session_state.expression = (
            st.session_state.expression[:-1]
        )

        st.session_state.display = (
            st.session_state.expression
            or "0"
        )

        return

    # EQUAL
    if value == "=":

        result = calculate(
            st.session_state.expression
        )

        st.session_state.display = result

        if result != "Error":
            st.session_state.expression = result

        return

    # SYMBOLS
    symbols = {
        "÷": "/",
        "×": "*",
        "−": "-"
    }

    actual = symbols.get(value, value)

    # Decimal protection
    if value == ".":

        current = st.session_state.expression

        last_number = re.split(
            r"[+\-*/%]",
            current
        )[-1]

        if "." in last_number:
            return

    # Operator protection
    if value in ["+", "−", "×", "÷"]:

        expression = st.session_state.expression

        if not expression:

            if value == "−":
                st.session_state.expression = "-"
                st.session_state.display = "-"
            return

        if expression[-1] in "+-*/":

            st.session_state.expression = (
                expression[:-1] + actual
            )

            st.session_state.display = (
                st.session_state.expression
            )

            return

    st.session_state.expression += actual

    st.session_state.display = (
        st.session_state.expression
    )


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap'
);

/* =========================
   BACKGROUND
========================= */

.stApp {

    background: #EBC8F7;

    font-family: 'Poppins', sans-serif;

}

/* =========================
   STREAMLIT CLEANUP
========================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {

    padding-top: 30px !important;

    padding-bottom: 30px !important;

}

/* =========================
   CALCULATOR
========================= */

.calc {

    width: 340px;

    margin: auto;

    padding: 25px;

    border-radius: 42px;

    background: #F8F7F3;

    box-shadow:

        15px 15px 35px
        rgba(145,110,150,.28),

        -15px -15px 35px
        rgba(255,255,255,.75);

}

/* =========================
   LOGO
========================= */

.logo {

    width: 55px;

    height: 55px;

    margin: 0 auto 10px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #EAF2F4;

    color: #B783A0;

    font-size: 25px;

    box-shadow:

        6px 6px 12px
        rgba(170,150,175,.28),

        -6px -6px 12px
        rgba(255,255,255,.9);

}

/* =========================
   TITLE
========================= */

.title {

    text-align: center;

    color: #77717A;

    font-size: 17px;

    font-weight: 600;

    letter-spacing: 2px;

    margin-bottom: 18px;

}

/* =========================
   ROUND DISPLAY
========================= */

.display {

    width: 100%;

    height: 92px;

    border-radius: 46px;

    background: #EAF2F4;

    display: flex;

    align-items: center;

    justify-content: flex-end;

    padding: 0 25px;

    box-sizing: border-box;

    overflow: hidden;

    color: #747B80;

    font-size: 32px;

    font-weight: 300;

    box-shadow:

        inset 6px 6px 12px
        rgba(180,195,200,.28),

        inset -6px -6px 12px
        rgba(255,255,255,.9),

        6px 6px 15px
        rgba(160,145,170,.12);

    margin-bottom: 24px;

}

/* =========================
   BUTTON
========================= */

div.stButton > button {

    width: 58px !important;

    height: 58px !important;

    min-width: 58px !important;

    max-width: 58px !important;

    padding: 0 !important;

    margin: auto !important;

    border-radius: 50% !important;

    border: none !important;

    background: #EAF2F4 !important;

    color: #70777B !important;

    font-family: 'Poppins', sans-serif !important;

    font-size: 16px !important;

    font-weight: 500 !important;

    box-shadow:

        7px 7px 13px
        rgba(165,150,175,.30),

        -7px -7px 13px
        rgba(255,255,255,.88) !important;

    transition: all .15s ease !important;

}

/* =========================
   HOVER
========================= */

@media (hover:hover) {

    div.stButton > button:hover {

        transform: translateY(-3px) !important;

        color: #5E6468 !important;

        background: #EAF2F4 !important;

        box-shadow:

            5px 5px 10px
            rgba(165,150,175,.28),

            -5px -5px 10px
            rgba(255,255,255,.9) !important;

    }

}

/* =========================
   PRESS
========================= */

div.stButton > button:active {

    transform: scale(.93) !important;

    box-shadow:

        inset 5px 5px 10px
        rgba(170,155,180,.30),

        inset -5px -5px 10px
        rgba(255,255,255,.8) !important;

}

/* =========================
   EQUAL
========================= */

.equal div.stButton > button {

    background: #E4A6C8 !important;

    color: white !important;

    box-shadow:

        7px 7px 14px
        rgba(165,125,150,.35),

        -7px -7px 14px
        rgba(255,255,255,.8) !important;

}

/* =========================
   SPECIAL
========================= */

.special div.stButton > button {

    color: #B57999 !important;

    font-size: 13px !important;

}

/* =========================
   SPACING
========================= */

div[data-testid="stHorizontalBlock"] {

    gap: 8px !important;

    margin-bottom: 10px !important;

}

/* =========================
   FOOTER
========================= */

.footer {

    text-align: center;

    margin-top: 20px;

    color: #958B99;

    font-size: 10px;

    letter-spacing: 2px;

}

/* =========================
   MOBILE
========================= */

@media (max-width: 500px) {

    .calc {

        width: min(340px, 92vw);

        padding: 20px;

    }

    div.stButton > button {

        width: 54px !important;

        height: 54px !important;

        min-width: 54px !important;

        max-width: 54px !important;

    }

    .display {

        height: 85px;

        font-size: 28px;

    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# OPEN CALCULATOR
# ============================================================

st.markdown(
    '<div class="calc">',
    unsafe_allow_html=True
)

# Logo
st.markdown(
    '<div class="logo">＋</div>',
    unsafe_allow_html=True
)

# Title
st.markdown(
    '<div class="title">CIRCLE CALC</div>',
    unsafe_allow_html=True
)

# Display
st.markdown(
    f"""
    <div class="display">
        {st.session_state.display}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ROW 1
# ============================================================

columns = st.columns(4)

buttons = ["C", "DEL", "%", "÷"]

for column, value in zip(columns, buttons):

    with column:

        st.markdown(
            '<div class="special">',
            unsafe_allow_html=True
        )

        if st.button(
            value,
            key=f"r1_{value}"
        ):

            button_press(value)
            st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# ROW 2
# ============================================================

columns = st.columns(4)

for column, value in zip(
    columns,
    ["7", "8", "9", "×"]
):

    with column:

        if st.button(
            value,
            key=f"r2_{value}"
        ):

            button_press(value)
            st.rerun()


# ============================================================
# ROW 3
# ============================================================

columns = st.columns(4)

for column, value in zip(
    columns,
    ["4", "5", "6", "−"]
):

    with column:

        if st.button(
            value,
            key=f"r3_{value}"
        ):

            button_press(value)
            st.rerun()


# ============================================================
# ROW 4
# ============================================================

columns = st.columns(4)

for column, value in zip(
    columns,
    ["1", "2", "3", "+"]
):

    with column:

        if st.button(
            value,
            key=f"r4_{value}"
        ):

            button_press(value)
            st.rerun()


# ============================================================
# ROW 5
# ============================================================

columns = st.columns(4)

# Decimal
with columns[0]:

    if st.button(".", key="decimal"):

        button_press(".")
        st.rerun()


# Zero
with columns[1]:

    if st.button("0", key="zero"):

        button_press("0")
        st.rerun()


# Equals
with columns[2]:

    st.markdown(
        '<div class="equal">',
        unsafe_allow_html=True
    )

    if st.button("=", key="equals"):

        button_press("=")
        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# Extra circular button
with columns[3]:

    if st.button("⌫", key="backspace"):

        button_press("DEL")
        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        MADE WITH PYTHON • CIRCLE CALC
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)
