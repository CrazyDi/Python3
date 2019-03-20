import requests
import re
from django.test import TestCase


# Create your tests here.
class TestRouting(TestCase):
    # Нужно написать view simple_route, которая формирует http ответ с пустым телом со статусом 200 на запрос GET
    # (если запросы отличные от GET - возвращать 405) по /routing/simple_route/:
    def test_simple_routing(self):
        url = 'http://127.0.0.1:8000/routing/simple_route/'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, b'')
        r = requests.get(url + 'sdf')
        self.assertEqual(r.status_code, 404)
        r = requests.post(url, data=None)
        self.assertEqual(r.status_code, 405)
        r = requests.put(url)
        self.assertEqual(r.status_code, 405)

    # slug_route - нужно написать view, которая принимает slug и отдает его в теле ответа.
    # В slug допустимы символы: 0-9, a-z, -, _ . Минимальная длина 1 символ, максимальная длина 16.
    def test_slug_route(self):
        url = 'http://127.0.0.1:8000/routing/slug_route/'
        for slug in ('1234', 'dfrt-g345', 'wet^&', '12345678901234567890'):
            with self.subTest(i=slug):
                r = requests.get(url + slug)
                if re.match('([a-z0-9\-\_]{1,16})$', slug) is not None:
                    self.assertEqual(r.content, slug.encode())
                    self.assertEqual(r.status_code, 200)
                else:
                    self.assertEqual(r.status_code, 404)

    # sum_route - нужно написать view, которая принимает 2 числа и их суммирует, например /routing/sum_route/1/2/
    def test_sum_route(self):
        url = 'http://127.0.0.1:8000/routing/sum_route/'
        for slug in ('1/2/', '1/-2/', '1/b/', 'a/2/'):
            with self.subTest(i=slug):
                r = requests.get(url + slug)
                l = re.findall('(\d)\/(\d)', slug)
                if len(l) > 0:
                    self.assertEqual(int(r.content), int(l[0][0]) + int(l[0][1]))
                    self.assertEqual(r.status_code, 200)
                else:
                    self.assertEqual(r.status_code, 404)

    # sum_get_method - нужно написать view, которая принимает 2 числа из GET параметров a и b и суммирует их.
    # Допускается только метод GET. Например /routing/sum_get_method/?а=1&b=2
    def test_sum_get_method(self):
        url = 'http://127.0.0.1:8000/routing/sum_get_method/'
        for slug in ({'a': '1', 'b': '2'}, {'a': '1', 'b': '-2'}, {'a': '1', 'b': 'b'}, {'a': 'a'}, {'b': '2'}, {}):
            with self.subTest(i=slug):
                r = requests.get(url, params=slug)
                if 'a' in slug and 'b' in slug:
                    if re.match('\d', slug['a']) and re.match('\d', slug['b']):
                        self.assertEqual(r.status_code, 200)
                        self.assertEqual(int(r.content), int(slug['a']) + int(slug['b']))
                    else:
                        self.assertEqual(r.status_code, 400)
                else:
                    self.assertEqual(r.status_code, 400)
                r = requests.post(url, params=slug)
                self.assertEqual(r.status_code, 400)


    #  sum_post_method - нужно написать view, которая принимает 2 числа из POST параметров a и b и суммирует их.
    #  Допускается только метод POST. Например /routing/sum_post_method/
    def test_sum_post_method(self):
        url = 'http://127.0.0.1:8000/routing/sum_post_method/'
        for slug in ({'a': '1', 'b': '2'}, {'a': '1', 'b': '-2'}, {'a': '1', 'b': 'b'}, {'a': 'a'}, {'b': '2'}, {}):
            with self.subTest(i=slug):
                r = requests.post(url, params=slug)
                if 'a' in slug and 'b' in slug:
                    if re.match('\d', slug['a']) and re.match('\d', slug['b']):
                        self.assertEqual(r.status_code, 200)
                        self.assertEqual(int(r.content), int(slug['a']) + int(slug['b']))
                    else:
                        self.assertEqual(r.status_code, 400)
                else:
                    self.assertEqual(r.status_code, 400)
                r = requests.post(url, params=slug)
                self.assertEqual(r.status_code, 400)