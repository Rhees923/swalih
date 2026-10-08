import streamlit as st
import ast
import operator
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NOVA CALC",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "display" not in st.session_state:
    st.session_state.display = "0"

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# SAFE CALCULATOR ENGINE
# ============================================================

OPERATORS = {
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

    # Percentage
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

                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError()

                if isinstance(node.op, ast.Div) and right == 0:
                    raise ZeroDivisionError()

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):

                operation = OPERATORS.get(type(node.op))

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
# INPUT HANDLER
# ============================================================

def press(value):

    if value == "AC":

        st.session_state.expression = ""
        st.session_state.display = "0"
        return

    if value == "DEL":

        st.session_state.expression = (
            st.session_state.expression[:-1]
        )

        st.session_state.display = (
            st.session_state.expression or "0"
        )

        return

    if value == "=":

        expression = st.session_state.expression

        if not expression:
            return

        result = calculate(expression)

        if result != "Error":

            st.session_state.history.insert(
                0,
                f"{expression} = {result}"
            )

            st.session_state.history = (
                st.session_state.history[:5]
            )

            st.session_state.display = result
            st.session_state.expression = result

        else:

            st.session_state.display = "Error"

        return

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
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

/* ==========================================================
   BODY
========================================================== */

.stApp {

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(124,58,237,.20),
            transparent 30%
        ),

        radial-gradient(
            circle at 90% 90%,
            rgba(59,130,246,.15),
            transparent 30%
        ),

        #080B14;

    font-family: 'Inter', sans-serif;

}

/* ==========================================================
   HIDE STREAMLIT UI
========================================================== */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {

    max-width: 430px !important;

    padding-top: 35px !important;

    padding-bottom: 30px !important;
}

/* ==========================================================
   CALCULATOR
========================================================== */

.calculator {

    padding: 24px;

    border-radius: 28px;

    background:
        rgba(18, 24, 39, .88);

    border:
        1px solid rgba(255,255,255,.08);

    box-shadow:

        0 30px 80px
        rgba(0,0,0,.55),

        inset 0 1px 1px
        rgba(255,255,255,.04);

    backdrop-filter: blur(20px);

    animation: calculatorIn .6s ease;
}

@keyframes calculatorIn {

    from {
        opacity: 0;
        transform: translateY(25px) scale(.97);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* ==========================================================
   HEADER
========================================================== */

.brand {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-bottom: 20px;
}

.brand-name {

    color: #ffffff;

    font-size: 18px;

    font-weight: 800;

    letter-spacing: 1px;
}

.brand-name span {

    color: #8b5cf6;
}

.status {

    display: flex;

    align-items: center;

    gap: 6px;

    color: #94a3b8;

    font-size: 11px;
}

.status-dot {

    width: 7px;

    height: 7px;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 10px #22c55e;

}

/* ==========================================================
   DISPLAY
========================================================== */

.display {

    min-height: 125px;

    padding: 22px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            #111827,
            #0b1120
        );

    border:
        1px solid rgba(255,255,255,.06);

    box-shadow:
        inset 0 5px 20px rgba(0,0,0,.25);

    display: flex;

    flex-direction: column;

    justify-content: flex-end;

    align-items: flex-end;

    overflow: hidden;

    margin-bottom: 20px;
}

.expression {

    width: 100%;

    text-align: right;

    color: #64748b;

    font-size: 14px;

    min-height: 22px;

    overflow: hidden;

    text-overflow: ellipsis;
}

.result {

    max-width: 100%;

    color: #f8fafc;

    font-size: 42px;

    font-weight: 500;

    letter-spacing: -1px;

    overflow: hidden;

    text-overflow: ellipsis;

    animation: resultIn .18s ease;
}

@keyframes resultIn {

    from {
        opacity: .3;
        transform: translateY(5px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ==========================================================
   BUTTONS
========================================================== */

div.stButton > button {

    width: 100%;

    height: 58px;

    border-radius: 17px;

    border:
        1px solid rgba(255,255,255,.06);

    background:
        #1a2233;

    color: #e2e8f0;

    font-family: 'Inter', sans-serif;

    font-size: 17px;

    font-weight: 600;

    box-shadow:
        0 5px 12px rgba(0,0,0,.22);

    transition:
        transform .12s ease,
        background .12s ease,
        box-shadow .12s ease;

}

/* Hover */

@media (hover:hover) {

    div.stButton > button:hover {

        color: #ffffff;

        background: #243047;

        transform: translateY(-2px);

        box-shadow:
            0 9px 20px rgba(0,0,0,.28);

    }

}

/* Press */

div.stButton > button:active {

    transform: scale(.94);

    box-shadow:
        0 2px 5px rgba(0,0,0,.25);

}

/* ==========================================================
   OPERATOR BUTTONS
========================================================== */

.operator div.stButton > button {

    background:
        #25203b;

    color:
        #a78bfa;

    border-color:
        rgba(139,92,246,.15);
}

.operator div.stButton > button:hover {

    background:
        #30294b;

}

/* ==========================================================
   CLEAR
========================================================== */

.clear div.stButton > button {

    background:
        #321d2b;

    color:
        #fb7185;

}

/* ==========================================================
   EQUAL
========================================================== */

.equals div.stButton > button {

    background:
        linear-gradient(
            135deg,
            #8b5cf6,
            #6366f1
        );

    color: white;

    border-color:
        rgba(167,139,250,.25);

    box-shadow:
        0 8px 20px
        rgba(99,102,241,.28);
}

.equals div.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #9b6cff,
            #7476ff
        );

}

/* ==========================================================
   BUTTON GAP
========================================================== */

div[data-testid="stHorizontalBlock"] {

    gap: 9px !important;

    margin-bottom: 9px !important;
}

/* ==========================================================
   HISTORY
========================================================== */

.history-title {

    color: #94a3b8;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1.5px;

    margin-top: 18px;

    margin-bottom: 8px;
}

.history-item {

    color: #64748b;

    font-size: 12px;

    padding: 6px 0;

    border-bottom:
        1px solid rgba(255,255,255,.04);

    text-align: right;
}

/* ==========================================================
   KEYBOARD
========================================================== */

.keyboard {

    text-align: center;

    color: #475569;

    font-size: 10px;

    margin-top: 16px;

    letter-spacing: .5px;
}

/* ==========================================================
   MOBILE
========================================================== */

@media (max-width: 500px) {

    .block-container {

        padding:
            15px 10px !important;
    }

    .calculator {

        padding: 18px;

        border-radius: 24px;
    }

    .result {

        font-size: 34px;
    }

    div.stButton > button {

        height: 54px;

        font-size: 16px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CALCULATOR START
# ============================================================

st.markdown(
    '<div class="calculator">',
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="brand">

    <div class="brand-name">
        NOVA<span>CALC</span>
    </div>

    <div class="status">
        <div class="status-dot"></div>
        READY
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# DISPLAY
# ============================================================

expression_display = (
    st.session_state.expression
    if st.session_state.expression
    else "Ready"
)

st.markdown(
    f"""
    <div class="display">

        <div class="expression">
            {expression_display}
        </div>

        <div class="result">
            {st.session_state.display}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ROW 1
# ============================================================

cols = st.columns(4)

buttons = ["AC", "DEL", "%", "÷"]

for col, value in zip(cols, buttons):

    with col:

        if value in ["AC", "DEL"]:

            st.markdown(
                '<div class="clear">',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                '<div class="operator">',
                unsafe_allow_html=True
            )

        if st.button(
            value,
            key=f"btn_{value}"
        ):

            press(value)
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ROW 2
# ============================================================

cols = st.columns(4)

for col, value in zip(
    cols,
    ["7", "8", "9", "×"]
):

    with col:

        if value == "×":
            st.markdown(
                '<div class="operator">',
                unsafe_allow_html=True
            )

        if st.button(
            value,
            key=f"btn2_{value}"
        ):

            press(value)
            st.rerun()

        if value == "×":
            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ROW 3
# ============================================================

cols = st.columns(4)

for col, value in zip(
    cols,
    ["4", "5", "6", "−"]
):

    with col:

        if value == "−":
            st.markdown(
                '<div class="operator">',
                unsafe_allow_html=True
            )

        if st.button(
            value,
            key=f"btn3_{value}"
        ):

            press(value)
            st.rerun()

        if value == "−":
            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ROW 4
# ============================================================

cols = st.columns(4)

for col, value in zip(
    cols,
    ["1", "2", "3", "+"]
):

    with col:

        if value == "+":
            st.markdown(
                '<div class="operator">',
                unsafe_allow_html=True
            )

        if st.button(
            value,
            key=f"btn4_{value}"
        ):

            press(value)
            st.rerun()

        if value == "+":
            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ROW 5
# ============================================================

cols = st.columns(4)

for col, value in zip(
    cols,
    [".", "0", "⌫", "="]
):

    with col:

        if value == "=":

            st.markdown(
                '<div class="equals">',
                unsafe_allow_html=True
            )

        if st.button(
            value,
            key=f"btn5_{value}"
        ):

            press(
                "DEL"
                if value == "⌫"
                else value
            )

            st.rerun()

        if value == "=":

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# ============================================================
# HISTORY
# ============================================================

if st.session_state.history:

    st.markdown(
        '<div class="history-title">RECENT</div>',
        unsafe_allow_html=True
    )

    for item in st.session_state.history[:3]:

        st.markdown(
            f'<div class="history-item">{item}</div>',
            unsafe_allow_html=True
        )


# ============================================================
# KEYBOARD INFO
# ============================================================

st.markdown(
    """
    <div class="keyboard">
        KEYBOARD: 0–9 &nbsp; + − * / &nbsp; ENTER &nbsp; BACKSPACE &nbsp; ESC
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CLOSE CALCULATOR
# ============================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# KEYBOARD JAVASCRIPT
# ============================================================

st.components.v1.html(
    """
    <script>

    document.addEventListener("keydown", function(event) {

        const key = event.key;

        let buttonText = null;

        if (/^[0-9]$/.test(key)) {
            buttonText = key;
        }

        else if (key === "+") {
            buttonText = "+";
        }

        else if (key === "-") {
            buttonText = "−";
        }

        else if (key === "*") {
            buttonText = "×";
        }

        else if (key === "/") {
            buttonText = "÷";
        }

        else if (key === ".") {
            buttonText = ".";
        }

        else if (key === "%") {
            buttonText = "%";
        }

        else if (key === "Enter" || key === "=") {
            buttonText = "=";
        }

        else if (key === "Backspace") {
            buttonText = "⌫";
        }

        else if (key === "Escape") {
            buttonText = "AC";
        }

        if (buttonText !== null) {

            event.preventDefault();

            const buttons =
                window.parent.document.querySelectorAll(
                    'button'
                );

            for (const button of buttons) {

                if (
                    button.innerText.trim()
                    === buttonText
                ) {

                    button.click();
                    break;

                }

            }

        }

    });

    </script>
    """,
    height=0
)
