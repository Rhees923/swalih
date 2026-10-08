from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Calculator</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
        }

        .calculator {
            width: 350px;
            padding: 25px;
            border-radius: 25px;
            background: rgba(255,255,255,0.08);
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
            backdrop-filter: blur(15px);
        }

        h1 {
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }

        .display {
            width: 100%;
            height: 80px;
            border: none;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 20px;
            background: #020617;
            color: white;
            font-size: 30px;
            text-align: right;
            outline: none;
        }

        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }

        button {
            height: 65px;
            border: none;
            border-radius: 15px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            background: #334155;
            color: white;
            transition: 0.15s;
        }

        button:hover {
            transform: scale(1.05);
            background: #475569;
        }

        .operator {
            background: #7c3aed;
        }

        .operator:hover {
            background: #8b5cf6;
        }

        .clear {
            background: #dc2626;
        }

        .equal {
            background: #16a34a;
        }

        .zero {
            grid-column: span 2;
        }

        .footer {
            color: #94a3b8;
            text-align: center;
            margin-top: 20px;
            font-size: 13px;
        }
    </style>
</head>

<body>

<div class="calculator">

    <h1>🐍 Python Calculator</h1>

    <form method="POST">

        <input
            class="display"
            type="text"
            name="expression"
            value="{{ expression }}"
            placeholder="0"
            readonly
        >

        <div class="buttons">

            <button class="clear" name="value" value="C">C</button>
            <button name="value" value="(">(</button>
            <button name="value" value=")">)</button>
            <button class="operator" name="value" value="/">÷</button>

            <button name="value" value="7">7</button>
            <button name="value" value="8">8</button>
            <button name="value" value="9">9</button>
            <button class="operator" name="value" value="*">×</button>

            <button name="value" value="4">4</button>
            <button name="value" value="5">5</button>
            <button name="value" value="6">6</button>
            <button class="operator" name="value" value="-">−</button>

            <button name="value" value="1">1</button>
            <button name="value" value="2">2</button>
            <button name="value" value="3">3</button>
            <button class="operator" name="value" value="+">+</button>

            <button class="zero" name="value" value="0">0</button>
            <button name="value" value=".">.</button>
            <button class="equal" name="value" value="=">=</button>

        </div>

    </form>

    <div class="footer">
        Made with Python 🐍
    </div>

</div>

</body>
</html>
"""

def safe_calculate(expression):
    """Calculate only basic mathematical expressions safely."""

    allowed = "0123456789+-*/(). "

    if not all(char in allowed for char in expression):
        return "Error"

    try:
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except:
        return "Error"


@app.route("/", methods=["GET", "POST"])
def calculator():

    expression = ""

    if request.method == "POST":

        value = request.form.get("value", "")

        if value == "C":
            expression = ""

        elif value == "=":
            old_expression = request.form.get("expression", "")
            expression = safe_calculate(old_expression)

        else:
            old_expression = request.form.get("expression", "")
            expression = old_expression + value

    return render_template_string(
        HTML,
        expression=expression
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
