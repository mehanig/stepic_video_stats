import unittest
import requests
import random
import string


def test_post_request_to_new_video(url, data):
    r = requests.post(url, data=data)
    return r.text

class MyTests(unittest.TestCase):


    def test(self):
        url = 'http://127.0.0.1:5000/newVideo'
        data = {'User': 'testUser', 'Name': ''.join(random.choice(string.ascii_letters) for i in range(10)), 'Duration': 'No data',
                'priority': 0, 'status': 0}
        self.assertEqual(test_post_request_to_new_video(url, data), '{"success": true}')
