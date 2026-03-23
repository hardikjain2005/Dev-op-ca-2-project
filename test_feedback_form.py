"""
test_feedback_form.py
---------------------
Selenium automated test suite for the Student Feedback Registration Form.

Requirements
------------
    pip install selenium

Run (unittest)
--------------
    python test_feedback_form.py

Run (pytest – richer output)
-----------------------------
    pip install pytest
    pytest test_feedback_form.py -v

Note: Ensure Google Chrome and the matching ChromeDriver binary are present
      in the same directory or on your PATH.
"""

import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ── Configuration ──────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
FORM_URL    = f"file:///{BASE_DIR}/index.html"
DRIVER_PATH = os.path.join(BASE_DIR, "chromedriver")


class FeedbackFormTests(unittest.TestCase):
    """End-to-end Selenium tests for the Student Feedback Registration Form."""

    # ── Setup / Teardown ───────────────────────────────────────────────────────

    def setUp(self):
        """Initialise headless Chrome before every test."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")

        service = Service(executable_path=DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait   = WebDriverWait(self.driver, timeout=10)
        self.driver.get(FORM_URL)

    def tearDown(self):
        """Quit the browser after every test."""
        self.driver.quit()

    # ── Helper: fill the form ──────────────────────────────────────────────────

    def _fill_form(
        self,
        name:       str = "Hardik Jain",
        email:      str = "hardik@example.com",
        mobile:     str = "9876543210",
        department: str = "cse",
        gender:     str = "Male",
        feedback:   str = "This is a sample feedback comment for testing purposes.",
    ):
        """Populate every field on the feedback form."""
        d = self.driver

        d.find_element(By.ID, "studentName").clear()
        d.find_element(By.ID, "studentName").send_keys(name)

        d.find_element(By.ID, "studentEmail").clear()
        d.find_element(By.ID, "studentEmail").send_keys(email)

        d.find_element(By.ID, "mobileNumber").clear()
        d.find_element(By.ID, "mobileNumber").send_keys(mobile)

        if department:
            Select(d.find_element(By.ID, "department")).select_by_value(department)

        if gender:
            radio = d.find_element(
                By.XPATH, f"//input[@name='gender'][@value='{gender}']"
            )
            if not radio.is_selected():
                radio.click()

        d.find_element(By.ID, "feedbackComments").clear()
        d.find_element(By.ID, "feedbackComments").send_keys(feedback)

    def _get_alert_text(self) -> str:
        """Wait for a browser alert, capture its text, and dismiss it."""
        alert = self.wait.until(EC.alert_is_present())
        text  = alert.text
        alert.accept()
        return text

    def _is_alert_present(self) -> bool:
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.driver.switch_to.alert.dismiss()
            return True
        except Exception:
            return False

    def _get_error(self, error_id: str) -> str:
        return self.driver.find_element(By.ID, error_id).text.strip()

    # ── Test cases ─────────────────────────────────────────────────────────────

    def test_01_page_loads_correctly(self):
        """Verify page title and form heading are rendered."""
        self.assertIn("Student Feedback", self.driver.title)
        heading = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Student Feedback", heading)

    def test_02_all_fields_present(self):
        """Verify all required input fields exist in the DOM."""
        for field_id in ("studentName", "studentEmail", "mobileNumber",
                         "department", "feedbackComments"):
            elem = self.driver.find_element(By.ID, field_id)
            self.assertTrue(elem.is_displayed(), f"Field '{field_id}' is not visible.")

        for gender_val in ("Male", "Female", "Other"):
            radio = self.driver.find_element(
                By.XPATH, f"//input[@name='gender'][@value='{gender_val}']"
            )
            self.assertTrue(radio.is_displayed())

    def test_03_submit_button_present(self):
        """Verify Submit and Reset buttons are present."""
        self.assertTrue(self.driver.find_element(By.ID, "submitBtn").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "resetBtn").is_displayed())

    def test_04_valid_submission_shows_success(self):
        """A fully filled form should trigger the success alert."""
        self._fill_form()
        self.driver.find_element(By.ID, "submitBtn").click()
        alert_text = self._get_alert_text()
        self.assertIn("Thank you", alert_text)

    def test_05_empty_name_shows_error(self):
        """Submitting with an empty name should show an inline error."""
        self._fill_form(name="")
        self.driver.find_element(By.ID, "submitBtn").click()
        error = self._get_error("nameError")
        self.assertIn("name", error.lower())

    def test_06_invalid_email_shows_error(self):
        """An invalid email should show an inline error."""
        self._fill_form(email="not-valid-email")
        self.driver.find_element(By.ID, "submitBtn").click()
        error = self._get_error("emailError")
        self.assertIn("email", error.lower())

    def test_07_invalid_mobile_shows_error(self):
        """A mobile number not matching 10-digit Indian format should show an error."""
        self._fill_form(mobile="12345")
        self.driver.find_element(By.ID, "submitBtn").click()
        error = self._get_error("mobileError")
        self.assertIn("mobile", error.lower())

    def test_08_no_department_shows_error(self):
        """Submitting without selecting a department should show an error."""
        self._fill_form(department="")    # skip department selection
        self.driver.find_element(By.ID, "submitBtn").click()
        error = self._get_error("deptError")
        self.assertIn("department", error.lower())

    def test_09_no_gender_shows_error(self):
        """Submitting without selecting a gender should show an error."""
        self._fill_form(gender="")        # skip gender
        self.driver.find_element(By.ID, "submitBtn").click()
        error = self._get_error("genderError")
        self.assertIn("gender", error.lower())

    def test_10_short_feedback_shows_error(self):
        """Feedback shorter than 10 characters should show an error."""
        self._fill_form(feedback="Short")
        self.driver.find_element(By.ID, "submitBtn").click()
        error = self._get_error("feedbackError")
        self.assertIn("feedback", error.lower())

    def test_11_character_counter_updates(self):
        """Character counter should reflect the number of typed characters."""
        textarea = self.driver.find_element(By.ID, "feedbackComments")
        textarea.clear()
        sample = "Hello World"
        textarea.send_keys(sample)
        count_text = self.driver.find_element(By.ID, "charCount").text
        self.assertIn(str(len(sample)), count_text)

    def test_12_reset_clears_form(self):
        """Reset button should clear all form fields."""
        self._fill_form()
        self.driver.find_element(By.ID, "resetBtn").click()
        time.sleep(0.5)
        name_val = self.driver.find_element(By.ID, "studentName").get_attribute("value")
        self.assertEqual(name_val, "")

    def test_13_all_departments_selectable(self):
        """Verify all department options can be selected."""
        select  = Select(self.driver.find_element(By.ID, "department"))
        options = ["cse", "it", "ece", "mech", "civil", "mba", "mca"]
        for opt in options:
            select.select_by_value(opt)
            self.assertEqual(
                select.first_selected_option.get_attribute("value"), opt
            )

    def test_14_all_gender_options_selectable(self):
        """Verify Male, Female, and Other radio buttons work."""
        for val in ("Male", "Female", "Other"):
            radio = self.driver.find_element(
                By.XPATH, f"//input[@name='gender'][@value='{val}']"
            )
            radio.click()
            self.assertTrue(radio.is_selected(), f"{val} radio not selected.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
