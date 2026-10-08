import streamlit as st
import ast
import operator
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Neumorphic Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# SESSION STATE
# ============================================================

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "display" not in st.session_state:
    st.session_state.display = "0"

# ============================================================
# SAFE CALCULATOR ENGINE
# ============================================================

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(expression):
    """
    Safely evaluate basic mathematical expressions.
    """

    if not expression:
        return 0

    # Convert percentage:
    # 50% -> (50/100)
    expression = re.sub(
        r"(\d+(?:\.\d+)?)%",
        r"(\1/100)",
        expression,
    )

    try:
        tree = ast.parse(expression, mode="eval")

        def calculate(node):

            if isinstance(node, ast.Expression):
                return calculate(node.body)

            if isinstance(node, ast.Constant):

                if isinstance(node.value, (int, float)):
                    return node.value

                raise ValueError("Invalid number")

            if isinstance(node, ast.BinOp):

                left = calculate(node.left)
                right = calculate(node.right)

                operation = operators.get(type(node.op))

                if operation is None:
                    raise ValueError("Invalid operator")

                if isinstance(node.op, ast.Div) and right == 0:
                    raise ZeroDivisionError

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):

                operation = operators.get(type(node.op))

                if operation is None:
                    raise ValueError("Invalid operator")

                return operation(calculate(node.operand))

            raise ValueError("Invalid expression")

        result = calculate(tree)

        if isinstance(result, float):

            if result.is_integer():
                return str(int(result))

            return f"{result:.10f}".rstrip("0").rstrip(".")

        return str(result)

    except ZeroDivisionError:
        return "Cannot divide by 0"

    except Exception:
        return "Error"


# ============================================================
# BUTTON HANDLER
# ============================================================

def press(value):

    # CLEAR
    if value == "CLR":
        st.session_state.expression = ""
        st.session_state.display = "0"
        return

    # DELETE
    if value == "DEL":

        st.session_state.expression = (
            st.session_state.expression[:-1]
        )

        if st.session_state.expression:
            st.session_state.display = (
                st.session_state.expression
            )
        else:
            st.session_state.display = "0"

        return

    # EQUAL
    if value == "=":

        if not st.session_state.expression:
            return

        result = safe_eval(
            st.session_state.expression
        )

        st.session_state.display = result

        if result not in ["Error", "Cannot divide by 0"]:
            st.session_state.expression = result

        return

    # DISPLAY SYMBOLS
    symbols = {
        "÷": "/",
        "×": "*",
        "−": "-",
    }

    actual = symbols.get(value, value)

    # Prevent multiple decimal points in same number
    if value == ".":

        current = st.session_state.expression

        number = re.split(
            r"[+\-*/%]",
            current
        )[-1]

        if "." in number:
            return

    # Prevent duplicate operators
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
# NEUMORPHIC CSS
# ============================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap'
);

/* ----------------------------------------------------------
   PAGE
---------------------------------------------------------- */

.stApp {
    background: #EBC8F7;
    font-family: 'Poppins', sans-serif;
}

/* Remove default Streamlit spacing */

.block-container {
    padding-top: 35px !important;
    padding-bottom: 30px !important;
}

/* Hide Streamlit decoration */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* ----------------------------------------------------------
   CALCULATOR
---------------------------------------------------------- */

.calculator {
    width: 330px;
    min-height: 540px;

    margin: 0 auto;

    padding: 25px;

    border-radius: 30px;

    background: #F8F7F4;

    box-shadow:
        12px 12px 28px rgba(150, 115, 155, 0.30),
        -10px -10px 25px rgba(255, 255, 255, 0.70);
}

/* ----------------------------------------------------------
   TITLE
---------------------------------------------------------- */

.title {
    text-align: center;

    color: #77717b;

    font-size: 17px;

    font-weight: 500;

    letter-spacing: 1.5px;

    margin-bottom: 18px;
}

/* ----------------------------------------------------------
   DISPLAY
---------------------------------------------------------- */

.display {

    width: 100%;

    height: 90px;

    padding: 15px 20px;

    display: flex;

    align-items: center;

    justify-content: flex-end;

    overflow: hidden;

    border-radius: 20px;

    background: #EAF2F4;

    color: #777b80;

    font-size: 34px;

    font-weight: 300;

    letter-spacing: 1px;

    white-space: nowrap;

    box-shadow:

        inset 5px 5px 12px rgba(180, 195, 200, 0.28),

        inset -5px -5px 12px rgba(255, 255, 255, 0.90),

        5px 5px 12px rgba(180, 170, 185, 0.15);

    margin-bottom: 22px;
}

/* ----------------------------------------------------------
   STREAMLIT BUTTONS
---------------------------------------------------------- */

div.stButton > button {

    width: 100%;

    height: 55px;

    border: none;

    border-radius: 50%;

    background: #EAF2F4;

    color: #74787c;

    font-family: 'Poppins', sans-serif;

    font-size: 16px;

    font-weight: 500;

    box-shadow:

        6px 6px 12px rgba(170, 155, 175, 0.28),

        -6px -6px 12px rgba(255, 255, 255, 0.85);

    transition:
        transform 0.12s ease,
        box-shadow 0.12s ease,
        background 0.12s ease;

    padding: 0;
}

/* Hover */

div.stButton > button:hover {

    color: #666b70;

    background: #EAF2F4;

    transform: translateY(-1px);

    box-shadow:

        4px 4px 8px rgba(170, 155, 175, 0.25),

        -4px -4px 8px rgba(255, 255, 255, 0.85);
}

/* Press */

div.stButton > button:active {

    transform: translateY(2px);

    box-shadow:

        inset 4px 4px 8px rgba(175, 165, 180, 0.30),

        inset -4px -4px 8px rgba(255, 255, 255, 0.75);
}

/* ----------------------------------------------------------
   GRID SPACING
---------------------------------------------------------- */

div[data-testid="stHorizontalBlock"] {

    gap: 11px !important;

    margin-bottom: 11px;
}

/* ----------------------------------------------------------
   EQUAL BUTTON
---------------------------------------------------------- */

.equal-button div.stButton > button {

    border-radius: 30px;

    background: #E4A6C8;

    color: #FFFFFF;

    box-shadow:

        6px 6px 12px rgba(170, 135, 155, 0.32),

        -6px -6px 12px rgba(255, 255, 255, 0.80);
}

.equal-button div.stButton > button:hover {

    background: #E4A6C8;

    color: #FFFFFF;
}

/* ----------------------------------------------------------
   SPECIAL BUTTONS
---------------------------------------------------------- */

.special div.stButton > button {

    color: #B17A9A;

    font-size: 14px;
}

/* ----------------------------------------------------------
   FOOTER
---------------------------------------------------------- */

.footer {

    text-align: center;

    margin-top: 20px;

    color: #918798;

    font-size: 11px;

    letter-spacing: 1px;
}

/* ----------------------------------------------------------
   MOBILE
---------------------------------------------------------- */

@media (max-width: 500px) {

    .block-container {
        padding: 20px 10px !important;
    }

    .calculator {

        width: min(330px, 94vw);

        padding: 22px;

        border-radius: 28px;
    }

    .display {
        height: 85px;
        font-size: 30px;
    }

    div.stButton > button {
        height: 52px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# CALCULATOR CARD
# ============================================================

st.markdown(
    '<div class="calculator">',
    unsafe_allow_html=True,
)

# TITLE

st.markdown(
    '<div class="title">CALCULATOR</div>',
    unsafe_allow_html=True,
)

# DISPLAY

display_value = st.session_state.display

st.markdown(
    f"""
    <div class="display">
        {display_value}
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# ROW 1
# ============================================================

c1, c2, c3, c4 = st.columns(4, gap="small")

with c1:
    st.markdown('<div class="special">', unsafe_allow_html=True)

    if st.button("clr", key="clear"):
        press("CLR")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="special">', unsafe_allow_html=True)

    if st.button("DEL", key="delete"):
        press("DEL")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    if st.button("%", key="percent"):
        press("%")
        st.rerun()

with c4:
    if st.button("/", key="divide"):
        press("÷")
        st.rerun()


# ============================================================
# ROW 2
# ============================================================

c1, c2, c3, c4 = st.columns(4, gap="small")

for col, value in zip(
    [c1, c2, c3, c4],
    ["7", "8", "9", "×"]
):

    with col:
        if st.button(value, key=f"key_{value}"):
            press(value)
            st.rerun()


# ============================================================
# ROW 3
# ============================================================

c1, c2, c3, c4 = st.columns(4, gap="small")

for col, value in zip(
    [c1, c2, c3, c4],
    ["4", "5", "6", "−"]
):

    with col:
        if st.button(value, key=f"key_{value}"):
            press(value)
            st.rerun()


# ============================================================
# ROW 4
# ============================================================

c1, c2, c3, c4 = st.columns(4, gap="small")

for col, value in zip(
    [c1, c2, c3, c4],
    ["1", "2", "3", "+"]
):

    with col:
        if st.button(value, key=f"key_{value}"):
            press(value)
            st.rerun()


# ============================================================
# ROW 5
# ============================================================

c1, c2, c3, c4 = st.columns(4, gap="small")

with c1:
    if st.button(".", key="decimal"):
        press(".")
        st.rerun()

with c2:
    if st.button("0", key="zero"):
        press("0")
        st.rerun()

# Equal takes two columns

with c3:
    st.markdown(
        '<div class="equal-button">',
        unsafe_allow_html=True,
    )

    if st.button("=", key="equals"):
        press("=")
        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

with c4:
    # visually joins the equal area
    st.markdown(
        """
        <div style="
            height:55px;
            border-radius:30px;
            background:#E4A6C8;
            box-shadow:
                6px 6px 12px rgba(170,135,155,.32),
                -6px -6px 12px rgba(255,255,255,.80);
        "></div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        SOFT • SIMPLE • NEUMORPHIC
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
