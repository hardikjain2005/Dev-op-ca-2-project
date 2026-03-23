# Student Enrollment Portal – DevOps Project

A full-stack demonstration project combining a frontend web form with automated Selenium testing and a Jenkins CI/CD pipeline.

---

## 📁 Project Structure

```
DevOpsProject/
├── index.html                  # Student Enrollment Form (frontend)
├── style.css                   # Modern stylesheet (Inter, gradient card)
├── test_enrollment_form.py     # Python Selenium automated test suite
├── Jenkinsfile                 # Declarative Jenkins CI pipeline
├── chromedriver                # ChromeDriver binary (macOS)
└── README.md                   # Project documentation
```

---

## 🚀 Technologies Used

| Category        | Technology                         |
|-----------------|------------------------------------|
| Frontend        | HTML5, CSS3, JavaScript (ES6+)     |
| Fonts           | Google Fonts – Inter               |
| Testing         | Python 3, Selenium WebDriver       |
| CI/CD           | Jenkins (Declarative Pipeline)     |
| Browser Driver  | ChromeDriver                       |

---

## ✅ Features

- **Student Registration Form** with fields for name, email, password, gender, and program selection
- **Client-side Validation** – instant feedback for empty fields, invalid email, short password, and mismatched passwords
- **Automated Testing** – 8 Selenium test cases covering page load, valid submission, and all validation paths
- **Jenkins Pipeline** – 5-stage CI pipeline: Checkout → Setup → Lint → Test → Archive

---

## 🛠️ Local Setup

### Prerequisites

- Python 3.8+
- Google Chrome (matching the bundled `chromedriver` version)

### Install Python dependencies

```bash
pip install selenium
```

### Run Selenium tests

```bash
python test_enrollment_form.py
```

Or with pytest for richer output:

```bash
pip install pytest
pytest test_enrollment_form.py -v
```

---

## 🔄 Jenkins CI Pipeline

The `Jenkinsfile` defines a **Declarative Pipeline** with the following stages:

| # | Stage              | Description                                |
|---|--------------------|--------------------------------------------|
| 1 | **Checkout**       | Pull source code from SCM                  |
| 2 | **Setup**          | Create Python venv, install `selenium`     |
| 3 | **Lint**           | Run `flake8` static analysis               |
| 4 | **Selenium Tests** | Execute test suite, publish JUnit report   |
| 5 | **Archive**        | Save test reports as build artifacts       |

To use the pipeline:
1. Create a **Pipeline** job in Jenkins.
2. Point it to this repository.
3. Jenkins will automatically detect and run `Jenkinsfile`.

---

## 👤 Author

**Hardik Jain**  
DevOps | Selenium | CI/CD  

---
