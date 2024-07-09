import os
import sys
import csv
import requests
import unittest
from common import INPUT_CSV_PATH, ZIPPOPOTAM_ROOT

class TestApi(unittest.TestCase):
    """A class to test API responses for given postcodes and place names
    using the Zippopotam API.
    """
    def setUp(self, csv_path=None):
        if csv_path is None:
            current_path = os.path.dirname(os.path.abspath(__file__))
            self.csv_path = os.path.join(current_path, INPUT_CSV_PATH)
        else:
            self.csv_path = csv_path

    def read_input_file(self):
        """Read test data from an input CSV file specified by self.csv_path."""
        filepath = self.csv_path

        if not os.path.isfile(filepath):
            raise Exception(f"The file {filepath} does not exist.")

        if not filepath.endswith('.csv'):
            raise Exception(f"The file {filepath} is not a csv file.")

        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [(row['Country'], row['Postal Code'], row['Place Name']) for row in reader]

    def test_stuttgart_api(self):
        """Test the API response for Stuttgart ensuring correct place information
        and meeting response time standards.
        """
        test_post_code = '70597'
        test_place_name = 'Stuttgart Degerloch'
        url = f"{ZIPPOPOTAM_ROOT}/de/bw/stuttgart"
        response = requests.get(url)

        # Check the response code, content type and elapsed time
        self.assertTrue(response.status_code == 200,
                        f"{url} is not working. Status code: {response.status_code}.")
        self.assertTrue('json' in response.headers['Content-Type'],
                        f"Content type was {response.headers['Content-Type']}.")
        self.assertTrue(response.elapsed.total_seconds() < 1,
                        f"Response time was {response.elapsed.total_seconds()} seconds.")

        data = response.json()

        # Check the response country and state
        self.assertEqual(data['country'], 'Germany',
                         f"Country response was: {data['country']}.")
        self.assertEqual(data['state'], 'Baden-Württemberg', 
                         f"State response was: {data['state']}.")

        # Check the existence of the test values denoted by {test_post_code} and {test_place_name}
        places = [place for place in data['places']
                  if place['post code'] == test_post_code]
        self.assertIn(test_place_name, 'Stuttgart Degerloch',
                      f"{test_place_name} was not found in {test_post_code}.")

    def test_input_values_api(self):
        """Test the API response for various countries and postcodes specified in the input CSV file.
        Verifies if an expected place is correctly returned.
        """
        test_data = self.read_input_file()

        for country, post_code, expected_place in test_data:
            url = f"{ZIPPOPOTAM_ROOT}/{country}/{post_code}"
            response = requests.get(url)

            # Check the response code, content type and elapsed time
            self.assertTrue(response.status_code == 200,
                            f"{url} is not working. Status code: {response.status_code}.")
            self.assertTrue('json' in response.headers['Content-Type'],
                            f"Content type was {response.headers['Content-Type']}.")
            self.assertTrue(response.elapsed.total_seconds() < 1,
                            f"Response time was {response.elapsed.total_seconds()} seconds.")

            data = response.json()

            # Check the existence of {expected_place} provided in the input file
            places = [place['place name'] for place in data['places']]
            self.assertIn(expected_place, places,
                          f"{expected_place} was not found in {post_code}, {country}.")

if __name__ == "__main__":
    unittest.main(argv=sys.argv[:1])