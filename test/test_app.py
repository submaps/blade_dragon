import unittest
import requests
from main import start
from time import sleep


class TestApp(unittest.TestCase):
    def test1_upload(self):
        sleep(0.5)
        files = {'file': open('../dragon_data_test/file1.txt', 'rb')}
        r = requests.post('http://127.0.0.1:5000/upload', files=files)
        self.assertEqual(r.text, "eb34d0ef36ba6a8c5b2a956a312d1316")

    def test2_download(self):
        sleep(0.5)
        res = requests.get('http://127.0.0.1:5000/download/eb34d0ef36ba6a8c5b2a956a312d1316')
        self.assertEqual(res.text, 'aaa bbb\nccc')

    def test3_delete(self):
        sleep(0.5)
        res_del = requests.get('http://127.0.0.1:5000/delete/eb34d0ef36ba6a8c5b2a956a312d1316')
        self.assertEqual(res_del.text, "deleted eb34d0ef36ba6a8c5b2a956a312d1316")
        sleep(0.5)
        res_download = requests.get('http://127.0.0.1:5000/download/eb34d0ef36ba6a8c5b2a956a312d1316')
        self.assertEqual(res_download.text, 'file not found')
