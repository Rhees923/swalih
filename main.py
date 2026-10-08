import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Pastel Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# HTML + CSS + JAVASCRIPT
# ============================================================

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Pastel Calculator</title>

<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    min-height: 100%;
    font-family: "Poppins", "Segoe UI", Arial, sans-serif;
}

body {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;

    background:
        radial-gradient(
            circle at 15% 12%,
            rgba(255,255,255,.50),
            transparent 28%
        ),
        radial-gradient(
            circle at 88% 86%,
            rgba(255,255,255,.30),
            transparent 25%
        ),
        #eac8f5;
}

/* ============================================================
   CALCULATOR
============================================================ */

.calculator {
    width: min(100%, 350px);

    padding: 28px 23px 25px;

    border-radius: 34px;

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #f7f7f9
        );

    box-shadow:
        16px 18px 35px rgba(142,105,157,.22),
        -9px -9px 24px rgba(255,255,255,.55),
        inset 1px 1px 2px rgba(255,255,255,.95);

    animation: rise .65s cubic-bezier(.2,.8,.2,1);
}

@keyframes rise {

    from {
        opacity: 0;
        transform:
            translateY(18px)
            scale(.97);
    }

    to {
        opacity: 1;
        transform:
            translateY(0)
            scale(1);
    }
}

/* ============================================================
   BRAND
============================================================ */

.brand {

    margin:
        0 0 18px 4px;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 3px;

    text-transform: uppercase;

    color: #b39abb;
}

/* ============================================================
   DISPLAY
============================================================ */

.screen {

    min-height: 92px;

    padding:
        15px 18px 13px;

    margin-bottom: 27px;

    border-radius: 25px;

    background: #edf5f5;

    box-shadow:

        inset 5px 5px 12px
        rgba(196,209,210,.25),

        inset -5px -5px 12px
        rgba(255,255,255,.95),

        5px 7px 15px
        rgba(166,169,173,.15);

    display: flex;

    flex-direction: column;

    align-items: flex-end;

    justify-content: center;

    overflow: hidden;
}

.expression {

    width: 100%;

    min-height: 18px;

    text-align: right;

    font-size: 12px;

    color: #9a9da1;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}

.result {

    width: 100%;

    text-align: right;

    font-size: clamp(
        35px,
        10vw,
        43px
    );

    font-weight: 300;

    letter-spacing: -1.5px;

    line-height: 1.2;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;

    color: #74767b;

    animation: numberIn .18s ease;
}

@keyframes numberIn {

    from {
        opacity: .3;
        transform: translateY(3px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ============================================================
   BUTTON GRID
============================================================ */

.keys {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 14px 12px;
}

/* ============================================================
   BUTTONS
============================================================ */

button {

    border: 0;

    min-width: 0;

    aspect-ratio: 1;

    border-radius: 50%;

    background:
        linear-gradient(
            145deg,
            #f2f6f8,
            #e8edf0
        );

    color: #30343a;

    font:
        500 15px
        "Poppins",
        "Segoe UI",
        Arial,
        sans-serif;

    cursor: pointer;

    box-shadow:

        6px 6px 12px
        rgba(179,183,189,.38),

        -5px -5px 11px
        rgba(255,255,255,.96);

    transition:
        transform .14s ease,
        box-shadow .14s ease,
        filter .14s ease;

    -webkit-tap-highlight-color: transparent;
}

button:hover {

    filter: brightness(1.025);

    transform:
        translateY(-2px);

    box-shadow:

        7px 8px 14px
        rgba(179,183,189,.35),

        -5px -5px 11px
        rgba(255,255,255,.98);
}

button:active {

    transform:
        translateY(1px)
        scale(.94);

    box-shadow:

        inset 4px 4px 8px
        rgba(179,183,189,.30),

        inset -4px -4px 8px
        rgba(255,255,255,.9);
}

/* ============================================================
   UTILITY BUTTONS
============================================================ */

button.utility {

    font-size: 13px;

    background:
        linear-gradient(
            145deg,
            #f4f6f8,
            #e9edf0
        );
}

/* ============================================================
   OPERATORS
============================================================ */

button.operator {

    font-size: 19px;

    color: #777780;
}

/* ============================================================
   EQUAL BUTTON
============================================================ */

button.equals {

    grid-column: span 2;

    aspect-ratio: auto;

    border-radius: 999px;

    background:
        linear-gradient(
            145deg,
            #edbad6,
            #e5a7c9
        );

    color: white;

    font-size: 21px;

    font-weight: 600;

    box-shadow:

        6px 7px 14px
        rgba(190,128,162,.30),

        -4px -4px 10px
        rgba(255,255,255,.90);
}

button.equals:hover {

    filter: brightness(1.04);

}

button.equals:active {

    box-shadow:

        inset 4px 4px 8px
        rgba(160,91,129,.22),

        inset -4px -4px 8px
        rgba(255,255,255,.35);
}

/* ============================================================
   FOOTER
============================================================ */

.footer {

    margin:
        22px 0 0;

    text-align: center;

    color: #b3a4b9;

    font-size: 10px;

    letter-spacing: 1.7px;
}

/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 390px) {

    body {
        padding: 14px;
    }

    .calculator {

        padding:
            23px 18px 20px;

        border-radius: 29px;
    }

    .keys {
        gap: 12px 10px;
    }

    button {
        font-size: 14px;
    }
}

</style>
</head>

<body>

<main class="calculator" aria-label="Calculator">

    <p class="brand">
        Soft • Calculate
    </p>

    <section
        class="screen"
        aria-live="polite"
        aria-atomic="true"
    >

        <div
            class="expression"
            id="expression">
        </div>

        <div
            class="result"
            id="result">
            0
        </div>

    </section>

    <section
        class="keys"
        aria-label="Calculator keys"
    >

        <button
            class="utility"
            data-action="clear">
            clr
        </button>

        <button
            class="utility"
            data-action="delete">
            DEL
        </button>

        <button
            class="utility"
            data-action="percent">
            %
        </button>

        <button
            class="operator"
            data-value="/">
            /
        </button>


        <button data-value="7">7</button>
        <button data-value="8">8</button>
        <button data-value="9">9</button>

        <button
            class="operator"
            data-value="*">
            ×
        </button>


        <button data-value="4">4</button>
        <button data-value="5">5</button>
        <button data-value="6">6</button>

        <button
            class="operator"
            data-value="-">
            −
        </button>


        <button data-value="1">1</button>
        <button data-value="2">2</button>
        <button data-value="3">3</button>

        <button
            class="operator"
            data-value="+">
            +
        </button>


        <button data-value=".">.</button>

        <button data-value="0">0</button>

        <button
            class="equals"
            data-action="equals">
            =
        </button>

    </section>

    <p class="footer">
        SIMPLE • SMOOTH • SMART
    </p>

</main>


<script>

(() => {

    const resultEl =
        document.getElementById("result");

    const expressionEl =
        document.getElementById("expression");

    let expression = "";

    let justEvaluated = false;


    /* ========================================================
       DISPLAY
    ======================================================== */

    function render(value = expression || "0") {

        resultEl.textContent = value;

        expressionEl.textContent =
            expression &&
            !justEvaluated
                ? expression
                    .replaceAll("*", "×")
                    .replaceAll("-", "−")
                : "";

    }


    /* ========================================================
       SAFE CALCULATOR
    ======================================================== */

    function safeCalculate(input) {

        input = input.trim();

        if (!input) {
            throw new Error("Incomplete expression");
        }

        /*
         * Only calculator characters.
         */
        if (!/^[0-9+\-*/().\s]+$/.test(input)) {
            throw new Error("Invalid expression");
        }

        /*
         * Expression cannot end with operator.
         */
        if (/[+\-*/.]$/.test(input)) {
            throw new Error("Incomplete expression");
        }

        /*
         * Tokenizer
         */
        const tokens =
            input.match(
                /(?:\d+(?:\.\d*)?|\.\d+|[()+\-*/])/g
            );

        if (!tokens) {
            throw new Error("Invalid expression");
        }

        if (
            tokens.join("") !==
            input.replace(/\s/g, "")
        ) {
            throw new Error("Invalid expression");
        }


        let pos = 0;


        /* ----------------------------------------------------
           Addition / subtraction
        ---------------------------------------------------- */

        function parseExpression() {

            let value = parseTerm();

            while (
                tokens[pos] === "+" ||
                tokens[pos] === "-"
            ) {

                const op = tokens[pos++];

                const right = parseTerm();

                if (op === "+") {
                    value += right;
                } else {
                    value -= right;
                }
            }

            return value;
        }


        /* ----------------------------------------------------
           Multiplication / division
        ---------------------------------------------------- */

        function parseTerm() {

            let value = parseUnary();

            while (
                tokens[pos] === "*" ||
                tokens[pos] === "/"
            ) {

                const op = tokens[pos++];

                const right = parseUnary();

                if (
                    op === "/" &&
                    right === 0
                ) {
                    throw new Error(
                        "Cannot divide by zero"
                    );
                }

                if (op === "*") {
                    value *= right;
                } else {
                    value /= right;
                }
            }

            return value;
        }


        /* ----------------------------------------------------
           Unary operators
        ---------------------------------------------------- */

        function parseUnary() {

            if (tokens[pos] === "+") {

                pos++;

                return parseUnary();
            }

            if (tokens[pos] === "-") {

                pos++;

                return -parseUnary();
            }

            return parsePrimary();
        }


        /* ----------------------------------------------------
           Numbers + parentheses
        ---------------------------------------------------- */

        function parsePrimary() {

            if (tokens[pos] === "(") {

                pos++;

                const value =
                    parseExpression();

                if (tokens[pos++] !== ")") {

                    throw new Error(
                        "Missing bracket"
                    );
                }

                return value;
            }


            const token =
                tokens[pos++];

            if (
                !token ||
                !/^(?:\d+(?:\.\d*)?|\.\d+)$/.test(token)
            ) {

                throw new Error(
                    "Invalid expression"
                );
            }

            return Number(token);
        }


        const answer =
            parseExpression();


        if (
            pos !== tokens.length ||
            !Number.isFinite(answer)
        ) {

            throw new Error(
                "Invalid result"
            );
        }


        return Number(
            answer.toPrecision(12)
        ).toString();

    }


    /* ========================================================
       ADD VALUE
    ======================================================== */

    function addValue(value) {

        if (
            justEvaluated &&
            /[0-9.]/.test(value)
        ) {
            expression = "";
        }

        justEvaluated = false;


        const last =
            expression.slice(-1);


        /*
         * Operators
         */

        if ("+-*/".includes(value)) {

            if (
                !expression &&
                value !== "-"
            ) {
                return;
            }

            if (
                "+-*/".includes(last)
            ) {

                expression =
                    expression.slice(0, -1);
            }
        }


        /*
         * Decimal
         */

        if (value === ".") {

            const currentNumber =
                expression
                    .split(/[+\-*/]/)
                    .pop();

            if (
                currentNumber.includes(".")
            ) {
                return;
            }

            if (!currentNumber) {
                expression += "0";
            }
        }


        expression += value;

        render();
    }


    /* ========================================================
       CALCULATE
    ======================================================== */

    function calculate() {

        try {

            const answer =
                safeCalculate(expression);

            expressionEl.textContent =
                expression
                    .replaceAll("*", "×")
                    .replaceAll("-", "−")
                + " =";

            resultEl.textContent =
                answer;

            expression = answer;

            justEvaluated = true;

        } catch (error) {

            if (
                error.message ===
                "Cannot divide by zero"
            ) {

                resultEl.textContent =
                    "Cannot divide by 0";

            } else {

                resultEl.textContent =
                    "Error";
            }

            justEvaluated = true;
        }
    }


    /* ========================================================
       ACTIONS
    ======================================================== */

    function handleAction(action) {

        /*
         * CLEAR
         */

        if (action === "clear") {

            expression = "";

            justEvaluated = false;

            render("0");
        }


        /*
         * DELETE
         */

        else if (action === "delete") {

            if (justEvaluated) {

                expression = "";

                justEvaluated = false;

            } else {

                expression =
                    expression.slice(0, -1);
            }

            render();
        }


        /*
         * EQUALS
         */

        else if (action === "equals") {

            calculate();
        }


        /*
         * PERCENT
         */

        else if (action === "percent") {

            if (!expression) {
                return;
            }

            try {

                expression =
                    (
                        safeCalculate(expression)
                        / 100
                    ).toString();

                justEvaluated = false;

                render();

            } catch (error) {

                resultEl.textContent =
                    "Error";
            }
        }
    }


    /* ========================================================
       MOUSE / TOUCH
    ======================================================== */

    document
        .querySelector(".keys")
        .addEventListener(
            "click",
            event => {

                const button =
                    event.target.closest(
                        "button"
                    );

                if (!button) {
                    return;
                }


                if (button.dataset.action) {

                    handleAction(
                        button.dataset.action
                    );

                } else {

                    addValue(
                        button.dataset.value
                    );
                }

            }
        );


    /* ========================================================
       KEYBOARD SUPPORT
    ======================================================== */

    document.addEventListener(
        "keydown",
        event => {

            /*
             * Numbers
             */

            if (/^[0-9.]$/.test(event.key)) {

                addValue(event.key);

                return;
            }


            /*
             * Operators
             */

            if (
                ["+", "-", "*", "/"]
                .includes(event.key)
            ) {

                addValue(event.key);

                return;
            }


            /*
             * Enter / =
             */

            if (
                event.key === "Enter" ||
                event.key === "="
            ) {

                event.preventDefault();

                calculate();

                return;
            }


            /*
             * Backspace
             */

            if (
                event.key === "Backspace"
            ) {

                handleAction("delete");

                return;
            }


            /*
             * Escape / Delete
             */

            if (
                event.key === "Escape" ||
                event.key === "Delete"
            ) {

                handleAction("clear");

                return;
            }


            /*
             * Percentage
             */

            if (event.key === "%") {

                handleAction("percent");

            }

        }
    );

})();

</script>

</body>
</html>
"""

# ============================================================
# STREAMLIT APP
# ============================================================

components.html(
    HTML_PAGE,
    height=700,
    scrolling=False,
)
