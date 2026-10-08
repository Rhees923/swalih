import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="iPhone Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

HTML_PAGE = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    min-height: 100%;
    background: #000;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "SF Pro Display",
        "Segoe UI",
        sans-serif;
}

body {
    min-height: 700px;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 25px 15px;

    background:
        radial-gradient(
            circle at 50% 20%,
            rgba(255,255,255,.055),
            transparent 35%
        ),
        #000;
}

/* =========================================
   PHONE CALCULATOR
========================================= */

.calculator {
    width: min(100%, 370px);
    padding: 30px 20px 25px;

    border-radius: 42px;

    background:
        linear-gradient(
            145deg,
            #181818,
            #080808
        );

    box-shadow:
        0 35px 80px rgba(0,0,0,.8),
        inset 0 1px 1px rgba(255,255,255,.08);

    border: 1px solid rgba(255,255,255,.06);

    animation: phoneIn .7s cubic-bezier(.2,.8,.2,1);
}

@keyframes phoneIn {

    from {
        opacity: 0;
        transform:
            translateY(35px)
            scale(.92);
    }

    to {
        opacity: 1;
        transform:
            translateY(0)
            scale(1);
    }
}

/* =========================================
   TOP BAR
========================================= */

.top {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 0 5px 15px;
}

.logo {
    color: #777;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #30d158;

    box-shadow:
        0 0 12px rgba(48,209,88,.7);

    animation: pulse 2s infinite;
}

@keyframes pulse {

    0%,100% {
        opacity: .7;
        transform: scale(1);
    }

    50% {
        opacity: 1;
        transform: scale(1.35);
    }
}

/* =========================================
   DISPLAY
========================================= */

.display {
    min-height: 145px;

    padding:
        15px 10px 18px;

    display: flex;
    flex-direction: column;

    justify-content: flex-end;
    align-items: flex-end;

    overflow: hidden;
}

.expression {

    width: 100%;

    min-height: 25px;

    text-align: right;

    color: #666;

    font-size: 18px;

    font-weight: 400;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;

    margin-bottom: 3px;
}

.result {

    width: 100%;

    text-align: right;

    color: #fff;

    font-size: clamp(
        54px,
        15vw,
        70px
    );

    line-height: 1;

    font-weight: 300;

    letter-spacing: -3px;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;

    animation: resultIn .18s ease;
}

@keyframes resultIn {

    from {
        opacity: .4;
        transform: translateY(5px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* =========================================
   KEYS
========================================= */

.keys {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 12px;
}

/* =========================================
   BUTTON
========================================= */

button {

    border: none;

    width: 100%;

    aspect-ratio: 1;

    border-radius: 50%;

    background:
        linear-gradient(
            145deg,
            #3b3b3d,
            #29292b
        );

    color: white;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "SF Pro Display",
        sans-serif;

    font-size: 27px;

    font-weight: 400;

    cursor: pointer;

    box-shadow:
        inset 0 1px 1px
        rgba(255,255,255,.08),

        0 5px 12px
        rgba(0,0,0,.5);

    transition:
        transform .12s ease,
        filter .12s ease,
        box-shadow .12s ease;
}

button:hover {

    filter: brightness(1.15);

    transform:
        translateY(-2px);
}

button:active {

    transform:
        scale(.88);

    filter:
        brightness(.75);

    box-shadow:
        inset 0 3px 8px
        rgba(0,0,0,.45);
}

/* =========================================
   TOP FUNCTIONS
========================================= */

button.utility {

    background:
        linear-gradient(
            145deg,
            #a6a6a8,
            #858587
        );

    color: #050505;

    font-size: 22px;

    font-weight: 500;
}

/* =========================================
   OPERATORS
========================================= */

button.operator {

    background:
        linear-gradient(
            145deg,
            #ffb340,
            #ff9500
        );

    color: white;

    font-size: 30px;

    font-weight: 500;

    box-shadow:
        0 5px 14px
        rgba(255,149,0,.22);
}

button.operator:hover {

    filter: brightness(1.12);
}

/* =========================================
   ACTIVE OPERATOR
========================================= */

button.operator.active {

    background: white;

    color: #ff9500;
}

/* =========================================
   ZERO
========================================= */

button.zero {

    grid-column: span 2;

    aspect-ratio: auto;

    border-radius: 999px;

    text-align: left;

    padding-left: 30px;
}

/* =========================================
   EQUAL
========================================= */

button.equals {

    background:
        linear-gradient(
            145deg,
            #ffb340,
            #ff9500
        );

    color: white;

    font-size: 30px;

    font-weight: 500;
}

/* =========================================
   FOOTER
========================================= */

.footer {

    text-align: center;

    margin-top: 20px;

    color: #444;

    font-size: 9px;

    letter-spacing: 3px;

    font-weight: 600;
}

/* =========================================
   MOBILE
========================================= */

@media (max-width: 390px) {

    body {
        padding: 10px;
    }

    .calculator {
        padding: 25px 15px 20px;
        border-radius: 35px;
    }

    .keys {
        gap: 10px;
    }

    button {
        font-size: 24px;
    }

    button.operator,
    button.equals {
        font-size: 27px;
    }
}

</style>
</head>

<body>

<div class="calculator">

    <div class="top">

        <div class="logo">
            CALCULATOR
        </div>

        <div class="dot"></div>

    </div>


    <div class="display">

        <div
            class="expression"
            id="expression">
        </div>

        <div
            class="result"
            id="result">
            0
        </div>

    </div>


    <div class="keys">

        <button
            class="utility"
            data-action="clear">
            AC
        </button>

        <button
            class="utility"
            data-action="delete">
            ⌫
        </button>

        <button
            class="utility"
            data-action="percent">
            %
        </button>

        <button
            class="operator"
            data-value="/">
            ÷
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


        <button
            class="zero"
            data-value="0">
            0
        </button>

        <button data-value=".">
            .
        </button>

        <button
            class="equals"
            data-action="equals">
            =
        </button>

    </div>


    <div class="footer">
        SIMPLE • FAST • BEAUTIFUL
    </div>

</div>


<script>

(() => {

    const result =
        document.getElementById("result");

    const expressionDisplay =
        document.getElementById("expression");

    let expression = "";

    let justEvaluated = false;


    /* =========================================
       DISPLAY
    ========================================= */

    function render(value) {

        result.textContent =
            value || expression || "0";

        if (
            expression &&
            !justEvaluated
        ) {

            expressionDisplay.textContent =
                expression
                    .replaceAll("*", "×")
                    .replaceAll("-", "−")
                    .replaceAll("/", "÷");

        } else {

            expressionDisplay.textContent = "";
        }
    }


    /* =========================================
       SAFE CALCULATOR
    ========================================= */

    function calculateExpression(input) {

        input = input.trim();

        if (!input) {
            throw new Error("Empty");
        }

        if (
            !/^[0-9+\-*/().\s]+$/.test(input)
        ) {
            throw new Error("Invalid");
        }

        if (/[+\-*/.]$/.test(input)) {
            throw new Error("Incomplete");
        }


        const tokens =
            input.match(
                /(?:\d+(?:\.\d*)?|\.\d+|[()+\-*/])/g
            );

        if (!tokens) {
            throw new Error("Invalid");
        }


        if (
            tokens.join("") !==
            input.replace(/\s/g, "")
        ) {
            throw new Error("Invalid");
        }


        let pos = 0;


        function expressionParser() {

            let value =
                termParser();

            while (
                tokens[pos] === "+" ||
                tokens[pos] === "-"
            ) {

                const op =
                    tokens[pos++];

                const right =
                    termParser();

                value =
                    op === "+"
                        ? value + right
                        : value - right;
            }

            return value;
        }


        function termParser() {

            let value =
                unaryParser();

            while (
                tokens[pos] === "*" ||
                tokens[pos] === "/"
            ) {

                const op =
                    tokens[pos++];

                const right =
                    unaryParser();

                if (
                    op === "/" &&
                    right === 0
                ) {
                    throw new Error(
                        "Divide by zero"
                    );
                }

                value =
                    op === "*"
                        ? value * right
                        : value / right;
            }

            return value;
        }


        function unaryParser() {

            if (tokens[pos] === "+") {

                pos++;

                return unaryParser();
            }

            if (tokens[pos] === "-") {

                pos++;

                return -unaryParser();
            }

            return primaryParser();
        }


        function primaryParser() {

            if (tokens[pos] === "(") {

                pos++;

                const value =
                    expressionParser();

                if (
                    tokens[pos++] !== ")"
                ) {
                    throw new Error(
                        "Bracket"
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
                throw new Error("Invalid");
            }

            return Number(token);
        }


        const answer =
            expressionParser();


        if (
            pos !== tokens.length ||
            !Number.isFinite(answer)
        ) {
            throw new Error("Invalid");
        }


        return Number(
            answer.toPrecision(12)
        ).toString();
    }


    /* =========================================
       ADD VALUE
    ========================================= */

    function addValue(value) {

        if (
            justEvaluated &&
            /[0-9.]/.test(value)
        ) {

            expression = "";
        }

        justEvaluated = false;


        if (
            "+-*/".includes(value)
        ) {

            if (
                !expression &&
                value !== "-"
            ) {
                return;
            }

            const last =
                expression.slice(-1);

            if (
                "+-*/".includes(last)
            ) {

                expression =
                    expression.slice(0, -1);
            }
        }


        if (value === ".") {

            const current =
                expression
                    .split(/[+\-*/]/)
                    .pop();

            if (
                current.includes(".")
            ) {
                return;
            }

            if (!current) {
                expression += "0";
            }
        }


        expression += value;

        render();
    }


    /* =========================================
       EQUAL
    ========================================= */

    function calculate() {

        try {

            const answer =
                calculateExpression(
                    expression
                );

            expressionDisplay.textContent =
                expression
                    .replaceAll("*", "×")
                    .replaceAll("/", "÷")
                    .replaceAll("-", "−")
                + " =";

            result.textContent =
                answer;

            expression = answer;

            justEvaluated = true;

        } catch (error) {

            result.textContent =
                error.message ===
                "Divide by zero"
                    ? "Error"
                    : "Error";

            justEvaluated = true;
        }
    }


    /* =========================================
       ACTIONS
    ========================================= */

    function action(type) {

        if (type === "clear") {

            expression = "";

            justEvaluated = false;

            render("0");

            return;
        }


        if (type === "delete") {

            if (justEvaluated) {

                expression = "";

                justEvaluated = false;

            } else {

                expression =
                    expression.slice(0, -1);
            }

            render();

            return;
        }


        if (type === "equals") {

            calculate();

            return;
        }


        if (type === "percent") {

            if (!expression) {
                return;
            }

            try {

                const value =
                    calculateExpression(
                        expression
                    );

                expression =
                    (
                        Number(value) / 100
                    ).toString();

                justEvaluated = false;

                render();

            } catch {

                result.textContent =
                    "Error";
            }
        }
    }


    /* =========================================
       BUTTON CLICK
    ========================================= */

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


                if (
                    button.dataset.action
                ) {

                    action(
                        button.dataset.action
                    );

                } else {

                    addValue(
                        button.dataset.value
                    );
                }
            }
        );


    /* =========================================
       KEYBOARD
    ========================================= */

    document.addEventListener(
        "keydown",
        event => {

            if (
                /^[0-9.]$/.test(
                    event.key
                )
            ) {

                addValue(event.key);

                return;
            }


            if (
                ["+", "-", "*", "/"]
                .includes(event.key)
            ) {

                addValue(event.key);

                return;
            }


            if (
                event.key === "Enter" ||
                event.key === "="
            ) {

                event.preventDefault();

                calculate();

                return;
            }


            if (
                event.key === "Backspace"
            ) {

                action("delete");

                return;
            }


            if (
                event.key === "Escape" ||
                event.key === "Delete"
            ) {

                action("clear");

                return;
            }


            if (event.key === "%") {

                action("percent");
            }

        }
    );

})();

</script>

</body>
</html>
"""

components.html(
    HTML_PAGE,
    height=730,
    scrolling=False
)
