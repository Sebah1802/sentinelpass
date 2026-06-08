from flask import Flask, render_template, request
import random
import string
import math

app = Flask(__name__)


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

        # Security Score

        security_score = score * 20

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


@app.route("/generator")
def generator():

    return render_template(
        "generator.html"
    )


@app.route("/breach")
def breach():

    return render_template(
        "breach.html"
    )


@app.route("/reports")
def reports():

    return render_template(
        "reports.html"
    )


@app.route("/settings")
def settings():

    return render_template(
        "settings.html"
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )