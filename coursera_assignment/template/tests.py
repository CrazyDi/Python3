from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class TestEcho(TestCase):
    def test_first(self):
        url = '/template/echo/'
        response = self.client.get(url, {'a': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'get a: 1 statement is empty')

    def test_second(self):
        url = '/template/echo/'
        response = self.client.get(url, {'c': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'get c: 2 statement is empty')

    def test_third(self):
        url = '/template/echo/'
        response = self.client.post(url, {'b': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'post b: 1 statement is empty')

    def test_fourth(self):
        url = '/template/echo/'
        response = self.client.post(url, {'d': '3'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'post d: 3 statement is empty')

    def test_fifth(self):
        url = '/template/echo/'
        header = {'X-Print-Statement': 'test'}
        response = self.client.get(url, **header)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'statement is test')
