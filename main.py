import streamlit as st
import streamlit.components.v1 as components
import ast
import operator
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NEXA CALC",
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
# SAFE MATH ENGINE
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


def safe_calculate(expression):

    if not expression:
        return "0"

    # Convert percentage
    expression = re.sub(
        r"(\d+(?:\.\d+)?)%",
        r"(\1/100)",
        expression
    )

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        def evaluate(node):

            if isinstance(
                node,
                ast.Expression
            ):
                return evaluate(node.body)

            if isinstance(
                node,
                ast.Constant
            ):

                if isinstance(
                    node.value,
                    (int, float)
                ):
                    return node.value

                raise ValueError()

            if isinstance(
                node,
                ast.BinOp
            ):

                left = evaluate(node.left)
                right = evaluate(node.right)

                operation = OPERATORS.get(
                    type(node.op)
                )

                if operation is None:
                    raise ValueError()

                if (
                    isinstance(
                        node.op,
                        ast.Div
                    )
                    and right == 0
                ):
                    raise ZeroDivisionError()

                return operation(
                    left,
                    right
                )

            if isinstance(
                node,
                ast.UnaryOp
            ):

                operation = OPERATORS.get(
                    type(node.op)
                )

                if operation is None:
                    raise ValueError()

                return operation(
                    evaluate(node.operand)
                )

            raise ValueError()

        result = evaluate(tree)

        if isinstance(result, float):

            if result.is_integer():
                return str(int(result))

            return (
                f"{result:.10f}"
                .rstrip("0")
                .rstrip(".")
            )

        return str(result)

    except ZeroDivisionError:

        return "Cannot divide by 0"

    except:

        return "Error"


# ============================================================
# CALCULATOR ACTION
# ============================================================

def calculate_action(value):

    # CLEAR
    if value == "AC":

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
            if st.session_state.expression
            else "0"
        )

        return

    # EQUAL
    if value == "=":

        expression = (
            st.session_state.expression
        )

        if not expression:
            return

        result = safe_calculate(
            expression
        )

        if result not in [
            "Error",
            "Cannot divide by 0"
        ]:

            st.session_state.history.insert(
                0,
                f"{expression} = {result}"
            )

            st.session_state.history = (
                st.session_state.history[:5]
            )

            st.session_state.expression = result
            st.session_state.display = result

        else:

            st.session_state.display = result

        return

    # SYMBOLS
    symbols = {
        "×": "*",
        "÷": "/",
        "−": "-"
    }

    actual = symbols.get(
        value,
        value
    )

    # DECIMAL
    if value == ".":

        current = (
            st.session_state.expression
        )

        last_number = re.split(
            r"[+\-*/%]",
            current
        )[-1]

        if "." in last_number:
            return

    # OPERATORS
    if value in [
        "+",
        "−",
        "×",
        "÷"
    ]:

        expression = (
            st.session_state.expression
        )

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
# PREMIUM CSS
# ============================================================

st.markdown(
"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

/* ========================================================
   BACKGROUND
======================================================== */

.stApp {

    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(99,102,241,.18),
            transparent 30%
        ),

        radial-gradient(
            circle at 85% 85%,
            rgba(14,165,233,.13),
            transparent 30%
        ),

        #070B14;

    font-family:
        'Inter',
        sans-serif;

}

/* ========================================================
   REMOVE STREAMLIT UI
======================================================== */

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

    max-width: 440px !important;

    padding-top: 30px !important;

    padding-bottom: 30px !important;
}

/* ========================================================
   MAIN CARD
======================================================== */

.calculator {

    background:
        rgba(17,24,39,.92);

    border:
        1px solid rgba(255,255,255,.07);

    border-radius:
        24px;

    padding:
        24px;

    box-shadow:
        0 30px 80px rgba(0,0,0,.55);

    animation:
        cardEnter .55s ease;

}

@keyframes cardEnter {

    from {

        opacity: 0;

        transform:
            translateY(25px);

    }

    to {

        opacity: 1;

        transform:
            translateY(0);

    }

}

/* ========================================================
   HEADER
======================================================== */

.header {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    margin-bottom:
        18px;

}

.logo {

    font-size:
        20px;

    font-weight:
        800;

    color:
        white;

    letter-spacing:
        .5px;

}

.logo span {

    color:
        #6366F1;

}

.online {

    font-size:
        10px;

    color:
        #64748B;

    display:
        flex;

    align-items:
        center;

    gap:
        6px;

}

.dot {

    width:
        7px;

    height:
        7px;

    background:
        #22C55E;

    border-radius:
        50%;

    box-shadow:
        0 0 10px #22C55E;

}

/* ========================================================
   DISPLAY
======================================================== */

.display {

    height:
        120px;

    padding:
        18px 20px;

    border-radius:
        18px;

    background:
        #0B1120;

    border:
        1px solid rgba(255,255,255,.06);

    box-shadow:
        inset 0 3px 15px rgba(0,0,0,.30);

    display:
        flex;

    flex-direction:
        column;

    justify-content:
        flex-end;

    align-items:
        flex-end;

    overflow:
        hidden;

    margin-bottom:
        18px;

}

.expression {

    color:
        #64748B;

    font-size:
        13px;

    width:
        100%;

    text-align:
        right;

    overflow:
        hidden;

    text-overflow:
        ellipsis;

}

.result {

    color:
        #F8FAFC;

    font-size:
        40px;

    font-weight:
        500;

    width:
        100%;

    text-align:
        right;

    overflow:
        hidden;

    text-overflow:
        ellipsis;

    animation:
        numberIn .18s ease;

}

@keyframes numberIn {

    from {

        opacity:
            .4;

        transform:
            translateY(4px);

    }

    to {

        opacity:
            1;

        transform:
            translateY(0);

    }

}

/* ========================================================
   BUTTONS
======================================================== */

div.stButton > button {

    width:
        100% !important;

    height:
        58px !important;

    border-radius:
        15px !important;

    background:
        #182235 !important;

    color:
        #E2E8F0 !important;

    border:
        1px solid rgba(255,255,255,.05) !important;

    font-family:
        'Inter',
        sans-serif !important;

    font-size:
        17px !important;

    font-weight:
        600 !important;

    box-shadow:
        0 5px 12px rgba(0,0,0,.20) !important;

    transition:
        all .15s ease !important;

}

/* ========================================================
   HOVER
======================================================== */

@media (hover:hover) {

    div.stButton > button:hover {

        background:
            #22304A !important;

        color:
            white !important;

        transform:
            translateY(-2px) !important;

        box-shadow:
            0 9px 22px rgba(0,0,0,.30) !important;

    }

}

/* ========================================================
   PRESS
======================================================== */

div.stButton > button:active {

    transform:
        scale(.94) !important;

}

/* ========================================================
   SPECIAL
======================================================== */

.special div.stButton > button {

    background:
        #211D38 !important;

    color:
        #A78BFA !important;

}

.clear div.stButton > button {

    background:
        #321E29 !important;

    color:
        #FB7185 !important;

}

/* ========================================================
   EQUAL
======================================================== */

.equal div.stButton > button {

    background:
        linear-gradient(
            135deg,
            #6366F1,
            #4F46E5
        ) !important;

    color:
        white !important;

    box-shadow:
        0 8px 20px
        rgba(79,70,229,.30) !important;

}

.equal div.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #7477FF,
            #5B55F0
        ) !important;

}

/* ========================================================
   SPACING
======================================================== */

div[data-testid="stHorizontalBlock"] {

    gap:
        9px !important;

    margin-bottom:
        9px !important;

}

/* ========================================================
   HISTORY
======================================================== */

.history-title {

    color:
        #64748B;

    font-size:
        10px;

    font-weight:
        700;

    letter-spacing:
        1.5px;

    margin-top:
        18px;

}

.history-item {

    color:
        #94A3B8;

    font-size:
        11px;

    padding:
        6px 0;

    border-bottom:
        1px solid rgba(255,255,255,.04);

    text-align:
        right;

}

/* ========================================================
   KEYBOARD
======================================================== */

.keyboard {

    text-align:
        center;

    color:
        #475569;

    font-size:
        10px;

    margin-top:
        15px;

}

/* ========================================================
   MOBILE
======================================================== */

@media (max-width:500px) {

    .block-container {

        padding:
            15px 10px !important;

    }

    .calculator {

        padding:
            18px;

    }

    div.stButton > button {

        height:
            53px !important;

    }

    .result {

        font-size:
            34px;

    }

}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# CALCULATOR UI
# ============================================================

st.markdown(
    '<div class="calculator">',
    unsafe_allow_html=True
)

# HEADER

st.markdown(
"""
<div class="header">

    <div class="logo">
        NEXA<span>CALC</span>
    </div>

    <div class="online">
        <div class="dot"></div>
        READY
    </div>

</div>
""",
unsafe_allow_html=True
)


# DISPLAY

st.markdown(
f"""
<div class="display">

    <div class="expression">
        {st.session_state.expression or "Ready"}
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

for col, value in zip(
    cols,
    ["AC", "DEL", "%", "÷"]
):

    with col:

        if value in ["AC", "DEL"]:

            st.markdown(
                '<div class="clear">',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                '<div class="special">',
                unsafe_allow_html=True
            )

        if st.button(
            value,
            key=f"r1_{value}"
        ):

            calculate_action(value)
            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# NUMBER ROWS
# ============================================================

rows = [
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
]

for row_number, row in enumerate(rows):

    cols = st.columns(4)

    for col, value in zip(cols, row):

        with col:

            if value in [
                "×",
                "−",
                "+"
            ]:

                st.markdown(
                    '<div class="special">',
                    unsafe_allow_html=True
                )

            if st.button(
                value,
                key=f"row{row_number}_{value}"
            ):

                calculate_action(value)
                st.rerun()

            if value in [
                "×",
                "−",
                "+"
            ]:

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


# ============================================================
# LAST ROW
# ============================================================

cols = st.columns(4)

last_buttons = [
    ".",
    "0",
    "⌫",
    "="
]

for col, value in zip(
    cols,
    last_buttons
):

    with col:

        if value == "=":

            st.markdown(
                '<div class="equal">',
                unsafe_allow_html=True
            )

        if st.button(
            value,
            key=f"last_{value}"
        ):

            if value == "⌫":

                calculate_action("DEL")

            else:

                calculate_action(value)

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
        '<div class="history-title">RECENT CALCULATIONS</div>',
        unsafe_allow_html=True
    )

    for item in st.session_state.history[:3]:

        st.markdown(
            f'<div class="history-item">{item}</div>',
            unsafe_allow_html=True
        )


st.markdown(
"""
<div class="keyboard">
    ⌨ 0–9 &nbsp; + − * / &nbsp; ENTER = &nbsp;
    BACKSPACE = DEL &nbsp; ESC = AC
</div>
""",
unsafe_allow_html=True
)


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# KEYBOARD SUPPORT
# ============================================================

components.html(
"""
<script>

(function () {

    const parent = window.parent.document;

    if (parent.__nexaKeyboard) {
        return;
    }

    parent.__nexaKeyboard = true;

    parent.addEventListener(
        "keydown",
        function(event) {

            let value = null;

            const key = event.key;

            // NUMBERS
            if (/^[0-9]$/.test(key)) {
                value = key;
            }

            // OPERATORS
            else if (key === "+") {
                value = "+";
            }

            else if (key === "-") {
                value = "−";
            }

            else if (key === "*") {
                value = "×";
            }

            else if (key === "/") {
                value = "÷";
            }

            else if (key === "%") {
                value = "%";
            }

            else if (key === ".") {
                value = ".";
            }

            // ENTER
            else if (
                key === "Enter" ||
                key === "="
            ) {
                value = "=";
            }

            // DELETE
            else if (key === "Backspace") {
                value = "⌫";
            }

            // CLEAR
            else if (key === "Escape") {
                value = "AC";
            }

            if (!value) {
                return;
            }

            event.preventDefault();

            const buttons =
                parent.querySelectorAll(
                    "button"
                );

            for (const button of buttons) {

                if (
                    button.innerText.trim()
                    === value
                ) {

                    button.click();

                    break;
                }

            }

        }

    );

})();

</script>
""",
height=0
)
