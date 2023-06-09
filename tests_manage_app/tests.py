from django.test import TestCase, Client
from .models import Test
from datetime import datetime


def MakeNewTest():
    return Client().post('/tests/create/')


def AddIQResult(test_login, points):
    return Client().post('/tests/add_result/iq/', {
        'test_login': test_login,
        'points': points
        }, content_type='application/json')


def AddEQResult(test_login, answer):
    return Client().post('/tests/add_result/eq/', {
        'test_login': test_login,
        'answer': answer
        }, content_type='application/json')


def GetTestResult(test_login):
    return Client().get(f'/tests/get_result/{test_login}/')


class TestAddNewTest(TestCase):

    def testCreateNewTest(self):
        resp = MakeNewTest()
        assert resp.status_code == 200
        test_login = resp.json()['test_login']
        assert len(test_login) == 10
        assert all([(ord(c) >= ord('a') and ord(c) <= ord('z')) or
                    (ord(c) >= ord('A') and ord(c) <= ord('Z'))
                    for c in test_login])
        assert len(Test.objects.filter(Login=test_login)) == 1


class TestAddIQResult(TestCase):

    @classmethod
    def setUpTestData(cls):
        Test(Login='aaaaaaaaaa').save()

    def testAddIQResult(self):
        resp = AddIQResult('aaaaaaaaaa', 30)
        assert resp.status_code == 200
        assert resp.json()['test_login'] == 'aaaaaaaaaa'
        assert resp.json()['test_result']['points'] == 30
        answer_time = datetime.fromisoformat(
            resp.json()['test_result']['answer_datetime'][:-5])
        assert (datetime.now() - answer_time).total_seconds() < 2
        test = Test.objects.filter(Login='aaaaaaaaaa')[0]
        assert test.IQTestPoints == 30
        assert test.IQTestAnswerTime is not None


class TestAddEQResult(TestCase):

    @classmethod
    def setUpTestData(cls):
        Test(Login='aaaaaaaaaa').save()

    def testAddEQResult(self):
        resp = AddEQResult('aaaaaaaaaa', 'абвгд')
        assert resp.status_code == 200
        assert resp.json()['test_login'] == 'aaaaaaaaaa'
        assert resp.json()['test_result']['answer'] == 'абвгд'
        answer_time = datetime.fromisoformat(
            resp.json()['test_result']['answer_datetime'][:-5])
        assert (datetime.now() - answer_time).total_seconds() < 2
        test = Test.objects.filter(Login='aaaaaaaaaa')[0]
        assert test.EQTestResult == 'абвгд'
        assert test.EQTestAnswerTime is not None
        

class TestGetResults(TestCase):

    @classmethod
    def setUpTestData(cls):
        Test(Login='aaaaaaaaaa').save()

    def testGetResults(self):
        resp = AddIQResult('aaaaaaaaaa', 45)
        assert resp.status_code == 200
        resp = AddEQResult('aaaaaaaaaa', 'абвгд')
        assert resp.status_code == 200
        resp = GetTestResult('aaaaaaaaaa')
        assert resp.status_code == 200
        assert resp.json()['test_login'] == 'aaaaaaaaaa'
        assert 'iq_test_result' in resp.json()
        assert 'eq_test_result' in resp.json()
