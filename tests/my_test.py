import json
import unittest
import requests
from faker import Faker

from lib.recruit_career.authentication import Authenticate
from lib.recruit_career.candidates import Candidates
from lib.recruit_career.rc_client import RecruitClient


class YahooAPITestCase(unittest.TestCase):
    def test_for_successful_response (self):
        result = requests.get("http://www.yahoo.com")
        self.assertEqual(200, result.status_code)
        # OR
        self.assertTrue('OK' == result.reason)


class CareerPortalTests(unittest.TestCase):
    def setUp (self) -> None:
        self.f = Faker()

    def test_login (self):
        client = RecruitClient()
        client.authentication.authenticate('jane@example.com', 'pass')

        # # if you want parallel clients
        # client2 = RecruitClient()
        # client2.authentication.authenticate('bob@example.com', 'Boo')
        #
        # # using A to instantiate P
        #
        # auth_client = Authenticate()
        # auth_client.authenticate()
        #
        # pos_client = Positions(auth_client)

        #############

        positions = client.positions.get_all_positions()
        json_positions = json.loads(positions.text)

        self.assertIsInstance(json_positions, list)
        self.assertGreaterEqual(len(json_positions), 5)

        result = client.authentication.authenticate("student@example.com", "welcome")
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        verify_response = client.authentication.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        candidate_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == 'student@example.com')
        self.assertEqual(8, candidate_id)

        my_positions = client.candidate.get_candidate_positions(candidate_id)
        json_my_positions = json.loads(my_positions.text)

        self.assertLessEqual(1, len(json_my_positions))

        # """
        # test create new candidate and check that data exist
        # 1.login
        # 2.go to base_url + candidates
        # 3.post new candidate data
        # 4.verify that new candidate was created
        #
        # """
        f = self.f

        first_name = f.first_name()
        last_name = f.last_name()
        email = f.email()
        password = f.password()

        candidate_data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password

        }
        response = client.candidate.create_new_candidate(candidate_data)
        json_response = json.loads(response.content)
        print(json_response)
        self.assertIn('id', json_response)

        candidate_id = json_response['id']
        candidate_first_name = json_response['firstName']
        candidate_email = json_response['email']
        print(candidate_id)
        new_data = {
            "firstName": candidate_first_name,
            "lastName": "NewLastName",
            "email": candidate_email,
            "password": "newPASSWORD"
        }
        candidate_page = client.candidate.update_candidate_data(candidate_id, new_data)
        json_candidate_page = json.loads(candidate_page.text)
        print(json_candidate_page)

        self.assertEqual('NewLastName', json_candidate_page['lastName'])
        # self.assertEqual('newPASSWORD', json_candidate_page['password'])

    # def test_cannot_login(self):
    #     sess = Authenticate()
    #     response = sess.authenticate('foo', 'barr')
    #     json_parsed = json.loads(response.text)
    #     self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])


if __name__ == '__main__':
    unittest.main()
