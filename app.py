from reportlab.pdfgen import canvas
from flask import Flask, render_template, request
import random
import string
import math
import hashlib
import requests

app = Flask(__name__)

total_passwords = 0
strong_count = 0
medium_count = 0
weak_count = 0
breached_count = 0
total_score = 0

latest_strength = "Not Checked"
latest_score = 0
latest_length = 0
latest_entropy = 0
latest_crack_time = "Unknown"
latest_status = "SAFE"

# Generate Secure Password
def generate_password(length=14):

    chars = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*"
    )

    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )

def check_pwned_password(password):

    sha1_password = hashlib.sha1(
        password.encode("utf-8")
    ).hexdigest().upper()

    prefix = sha1_password[:5]

    suffix = sha1_password[5:]

    url = (
        f"https://api.pwnedpasswords.com/range/{prefix}"
    )
    try:

        response = requests.get(url,timeout=5)

        if response.status_code != 200:

            return None

    except requests.exceptions.RequestException:

        return None

    hashes = (
        line.split(":")
        for line in response.text.splitlines()
    )

    for h, count in hashes:

        if h == suffix:

            return int(count)

    return 0

@app.route("/", methods=["GET", "POST"])
def dashboard():

    strength = "Not Checked"
    security_score = 0
    breached = False
    crack_time = "Unknown"
    entropy = 0
    length = 0

    suggested_password = generate_password()

    if request.method == "POST":

        global total_passwords
        global strong_count
        global medium_count
        global weak_count
        global breached_count
        global total_score

        global latest_strength
        global latest_score
        global latest_length
        global latest_entropy
        global latest_crack_time
        global latest_status

        password = request.form["password"]

        length = len(password)

        score = 0

        # Strength Checks

        has_upper = any(
            c.isupper()
            for c in password
        )

        has_lower = any(
            c.islower()
            for c in password
        )

        has_digit = any(
            c.isdigit()
            for c in password
        )

        has_special = any(
            not c.isalnum()
            for c in password
        )

        if length >= 8:
            score += 1

        if has_upper:
            score += 1

        if has_lower:
            score += 1

        if has_digit:
            score += 1

        if has_special:
            score += 1

        # Strength Label

        if score <= 2:

            strength = "Weak"

        elif score <= 4:

            strength = "Medium"

        else:

            strength = "Strong"

        total_passwords += 1

        if strength == "Strong":

            strong_count += 1

        elif strength == "Medium":

            medium_count += 1

        else:

            weak_count += 1

        # Security Score

        security_score = score * 20

        total_score += security_score

        # Entropy Calculation

        charset = 0

        if has_lower:
            charset += 26

        if has_upper:
            charset += 26

        if has_digit:
            charset += 10

        if has_special:
            charset += 32

        if charset > 0:

            entropy = round(
                length *
                math.log2(charset),
                2
            )

        # Breach Check

        try:

            with open(
                "datasets/leaked_passwords.txt",
                "r"
            ) as file:

                leaked_passwords = [
                    line.strip()
                    for line in file
                ]

            if password in leaked_passwords:

                breached = True

                breached_count += 1

                security_score = max(
                    security_score - 60,
                    0
                )

        except FileNotFoundError:

            pass

        # Crack Time Estimation

        if security_score <= 20:

            crack_time = "Instant"

        elif security_score <= 40:

            crack_time = "Minutes"

        elif security_score <= 60:

            crack_time = "Hours"

        elif security_score <= 80:

            crack_time = "Years"

        else:

            crack_time = "Centuries"

    latest_strength = strength

    latest_score = security_score

    latest_length = length

    latest_entropy = entropy

    latest_crack_time = crack_time

    if breached:
        
        latest_status = "BREACHED"

    else:

        latest_status = "SAFE"        

    return render_template(

        "dashboard.html",

        strength=strength,

        security_score=security_score,

        breached=breached,

        crack_time=crack_time,

        entropy=entropy,

        length=length,

        suggested_password=suggested_password
    )


@app.route(
    "/generator",
    methods=["GET", "POST"]
)
def generator():

    generated_password = ""

    length = 16

    if request.method == "POST":

        length = int(
            request.form["length"]
        )

        chars = ""

        if request.form.get(
            "uppercase"
        ):
            chars += string.ascii_uppercase

        if request.form.get(
            "lowercase"
        ):
            chars += string.ascii_lowercase

        if request.form.get(
            "numbers"
        ):
            chars += string.digits

        if request.form.get(
            "symbols"
        ):
            chars += "!@#$%^&*()_-+=<>?"

        if chars:

            generated_password = ''.join(

                random.choice(chars)

                for _ in range(length)

            )

    return render_template(
        "generator.html",
        generated_password=
        generated_password,
        length=length
    )


@app.route(
    "/breach",
    methods=["GET", "POST"]
)
def breach():

    result = None

    count = 0

    risk = ""

    recommendation = ""

    if request.method == "POST":

        password = request.form["password"]

        count = check_pwned_password(
            password
        )

        if count is None:

            result = "ERROR"

            recommendation = (
                "Unable to connect to breach database."
            )

        elif count > 0:

            result = "BREACHED"

            if count > 100000:

                risk = "HIGH"

            elif count > 1000:

                risk = "MEDIUM"

            else:

                risk = "LOW"
    
            recommendation = (
        "Change immediately and do not reuse it."
    )
    
        else:

            result = "SAFE"

            risk = "LOW"

            recommendation = (
        "Not found in known breach databases."
    )


    return render_template(
        "breach.html",
        result=result,
        count=count,
        risk=risk,
        recommendation=recommendation
    )


@app.route("/about")
def about():

    return render_template(
        "about.html"
    )

@app.route("/hello")
def hello():
    return "HELLO SENTINELPASS"

@app.route("/settings")
def settings():

    return render_template(
        "settings.html"
    )

@app.route("/download-report")
def download_report():

    from flask import send_file
    from datetime import datetime

    pdf_file = "reports/security_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.setTitle(
        "SentinelPass Security Report"
    )

    c.setFont(
        "Helvetica-Bold",
        22
    )

    c.drawString(
        120,
        800,
        "SentinelPass Security Report"
    )

    c.line(
        100,
        785,
        500,
        785
    )

    c.setFont(
        "Helvetica",
        12
    )

    current_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    c.drawString(
        100,
        740,
        f"Generated: {current_time}"
    )

    c.drawString(
        100,
        700,
        f"Password Strength: {latest_strength}"
    )

    c.drawString(
        100,
        670,
        f"Security Score: {latest_score}/100"
    )

    c.drawString(
        100,
        640,
        f"Password Length: {latest_length}"
    )

    c.drawString(
        100,
        610,
        f"Entropy: {latest_entropy} bits"
    )

    c.drawString(
        100,
        580,
        f"Crack Time: {latest_crack_time}"
    )

    c.drawString(
        100,
        550,
        f"Breach Status: {latest_status}"
    )

    c.line(
        100,
        500,
        500,
        500
    )

    c.drawString(
        100,
        460,
        "Generated by SentinelPass"
    )

    c.drawString(
        100,
        440,
        "Cybersecurity Password Analysis Tool"
    )

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )

if __name__ == "__main__":

    app.run(
        debug=True
    )