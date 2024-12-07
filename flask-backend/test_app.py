import unittest
from app import app, scrape_headlines

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    # Test: /scrape-headlines endpoint with a valid URL
    def test_scrape_headlines_valid_url(self):
        response = self.app.post('/scrape-headlines', json={
            "url": "https://www.bbc.com/news",
            "start_index": 0,
            "batch_size": 2
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("headlines", data)
        self.assertGreater(len(data["headlines"]), 0)

    # Test: /scrape-headlines endpoint with missing URL
    def test_scrape_headlines_missing_url(self):
        response = self.app.post('/scrape-headlines', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "URL not provided")


    # Test: scrape_headlines function directly
    def test_scrape_headlines_function(self):
        headlines = scrape_headlines("https://www.bbc.com/news", start_index=0, batch_size=2)
        self.assertIsInstance(headlines, list)

    # Test: /process-headlines endpoint with valid input
    def test_process_headlines_valid(self):
        response = self.app.post('/process-headlines', json={
            "headlines": [
                "The government announces new healthcare policies.",
                "The football match ended in a thrilling draw."
            ]
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        for result in data:
            self.assertIn("headline", result)
            self.assertIn("sentiment", result)
            self.assertIn("confidence", result)
            self.assertIn("topic", result)

    # Test: /process-headlines endpoint with empty headlines
    def test_process_headlines_empty(self):
        response = self.app.post('/process-headlines', json={"headlines": []})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "No headlines provided")

    # Test: /process-headlines endpoint with missing headlines key
    def test_process_headlines_missing_key(self):
        response = self.app.post('/process-headlines', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "No headlines provided")

if __name__ == '__main__':
    unittest.main()
