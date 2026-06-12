# SentinelPass 🔐

SentinelPass is a Flask-based cybersecurity dashboard designed to help users analyze password strength, detect breached passwords, generate secure passwords, and improve password security awareness.

---

## Features

* Password Strength Analysis
* Security Score Calculation
* Entropy Measurement
* Password Crack Time Estimation
* Real Breach Detection using Have I Been Pwned (HIBP)
* Secure Password Generator
* PDF Security Report Generation
* Dark Mode & Light Mode Support
* Custom Accent Themes (Green, Blue, Purple)
* Responsive Cybersecurity Dashboard UI

---

## Technology Stack

* Python
* Flask
* HTML5
* CSS3
* JavaScript
* ReportLab
* Have I Been Pwned (HIBP) API

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Sebah1802/sentinelpass.git
cd sentinelpass
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## Project Structure

```text
sentinelpass/
│
├── app.py
├── requirements.txt
├── README.md
│
├── datasets/
│   └── leaked_passwords.txt
│
├── static/
│   ├── style.css
│   └── script.js
│
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── generator.html
    ├── breach.html
    ├── settings.html
    └── about.html
```


## Future Improvements

* Advanced Security Analytics
* Multi-Factor Authentication Checker
* Enhanced Dashboard Visualizations
* User Authentication System

---

## Author

**Sebah Mariyam K M**

Cybersecurity Enthusiast | Python & Flask Developer

---

## Copyright

Copyright © 2026 Sebah Mariyam K M

All Rights Reserved.
