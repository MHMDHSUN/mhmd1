from flask import Flask, request, redirect
from markupsafe import escape

app = Flask(__name__)
operation_log = []

# تحويل رقم من أي نظام إلى آخر
def convert_number(number_str, from_base, to_base):
    try:
        decimal = int(number_str, from_base)
        if to_base == 10:
            return str(decimal), [f"الرقم {number_str} في النظام {from_base} يساوي {decimal} في النظام العشري."]
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""
        steps = [f"تحويل {number_str} من النظام {from_base} إلى النظام {to_base}:"]
        while decimal > 0:
            remainder = decimal % to_base
            result = digits[remainder] + result
            steps.append(f"{decimal} ÷ {to_base} = {decimal // to_base} والباقي = {remainder}")
            decimal //= to_base
        return result or "0", steps
    except Exception:
        return "خطأ في التحويل", ["تأكد من إدخال رقم صحيح وقواعد النظامين."]

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    steps = []
    number = ""
    from_base = 10
    to_base = 2
    show_steps = request.args.get("show_steps", "false").lower() == "true"
    show_log = request.args.get("show_log", "false").lower() == "true"

    if request.method == "POST":
        number = request.form.get("number", "").strip().upper()
        from_base = int(request.form.get("from_base", 10))
        to_base = int(request.form.get("to_base", 2))

        if number:
            result, steps = convert_number(number, from_base, to_base)
            operation_log.append(f"{number} (base {from_base}) → {result} (base {to_base})")

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>محول الأنظمة</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background-color: #f0f4f8;
                color: #333;
                text-align: center;
                padding-top: 50px;
            }}
            .container {{
                background: #fff;
                max-width: 500px;
                margin: auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            }}
            input, select {{
                width: 80%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 6px;
                border: 1px solid #ccc;
            }}
            button {{
                padding: 10px 25px;
                margin: 10px 5px;
                border: none;
                border-radius: 8px;
                background-color: #0077cc;
                color: white;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #005fa3;
            }}
            .secondary {{
                background-color: #28a745;
            }}
            .secondary:hover {{
                background-color: #1e7e34;
            }}
            .danger {{
                background-color: #dc3545;
            }}
            .danger:hover {{
                background-color: #c82333;
            }}
            ul {{
                text-align: right;
                direction: rtl;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔢 محول الأنظمة العددية</h2>
            <form method="POST">
                <input name="number" placeholder="أدخل الرقم" value="{escape(number)}" required>
                <br>
                من:
                <select name="from_base">
                    {''.join([f'<option value="{i}" {"selected" if i == from_base else ""}>{i}</option>' for i in range(2, 37)])}
                </select>
                إلى:
                <select name="to_base">
                    {''.join([f'<option value="{i}" {"selected" if i == to_base else ""}>{i}</option>' for i in range(2, 37)])}
                </select>
                <br>
                <button type="submit">تحويل</button>
            </form>
            <p><strong>النتيجة:</strong> {result}</p>

            <a href="/?show_steps={'false' if show_steps else 'true'}">
                <button class="secondary">{'إخفاء' if show_steps else 'إظهار'} طريقة الحل</button>
            </a>
            <a href="/?show_log={'false' if show_log else 'true'}">
                <button class="secondary">{'إخفاء' if show_log else 'إظهار'} السجل</button>
            </a>
            <a href="/clear_log">
                <button class="danger">حذف السجل</button>
            </a>

            {"<h3>طريقة الحل:</h3><ul>" + ''.join([f"<li>{escape(step)}</li>" for step in steps]) + "</ul>" if show_steps and steps else ""}
            {"<h3>السجل:</h3><ul>" + ''.join([f"<li>{escape(op)}</li>" for op in operation_log]) + "</ul>" if show_log and operation_log else ""}
        </div>
    </body>
    </html>
    """
    return html

@app.route("/clear_log")
def clear_log():
    operation_log.clear()
    return redirect("/?show_log=true")

if __name__ == "__main__":
    app.run(debug=True)
