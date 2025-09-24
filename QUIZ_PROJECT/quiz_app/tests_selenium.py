import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from quiz_app.models import Quiz, Question


class QuizSeleniumTest(LiveServerTestCase):
    """Simulate a user taking the quiz in a real browser"""

    def setUp(self):
        # Start Chrome WebDriver
        self.browser = webdriver.Chrome()

        # Create test quiz and questions
        self.quiz = Quiz.objects.create(title="Python Quiz")
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            text="What will 3 * 'hi' evaluate to?",
            option_a="'hi3'",
            option_b="'hihihi'",
            option_c="'hi hi hi'",
            option_d="Error",
            correct_answer="B"
        )
        self.q2 = Question.objects.create(
            quiz=self.quiz,
            text="What is the primary purpose of a tuple?",
            option_a="A tuple is immutable",
            option_b="Tuples can only store numbers",
            option_c="Tuples are mutable like lists",
            option_d="Tuples are always slower than lists",
            correct_answer="A"
        )

    def tearDown(self):
        self.browser.quit()

    def test_take_quiz(self):
        """Open quiz, select answers, submit, and check score"""

        # Go to quiz page
        self.browser.get(f"{self.live_server_url}/quiz/{self.quiz.id}/")

        # Select answers (assuming inputs are radio buttons with names like question_<id>)
        self.browser.find_element(By.CSS_SELECTOR, f"input[name='question_{self.q1.id}'][value='B']").click()
        self.browser.find_element(By.CSS_SELECTOR, f"input[name='question_{self.q2.id}'][value='A']").click()

        # Submit form
        self.browser.find_element(By.CSS_SELECTOR, "form").submit()

        # Wait for result page to load
        time.sleep(2)

        # Verify result text
        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Your Score: 2 / 2", body_text)
