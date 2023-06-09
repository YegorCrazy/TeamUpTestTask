import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Test
import random
from datetime import datetime


@api_view(['POST'])
def CreateTest(request):
    '''
    there is no check if we can create new test login, because
    there are 10^52 possible, it is too much to store them all in once
    '''
    available_syms = ([chr(ord('a') + i)
                       for i in range(ord('z') - ord('a') + 1)] +
                      [chr(ord('A') + i)
                       for i in range(ord('Z') - ord('A') + 1)])
    while True:
        test_login = ''.join(random.choices(available_syms, k=10))
        if len(Test.objects.filter(Login=test_login)) == 0:
            Test(Login=test_login).save()
            break
    return JsonResponse({'test_login': test_login}, status=200)


@api_view(['POST'])
def AddResultIQ(request):
    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'code': 76,
                             'payload': 'can\'t parse body'},
                            status=400)
    test_login = body.get('test_login')
    points = body.get('points')
    if test_login is None or points is None:
        return JsonResponse({'code': 77,
                             'payload': 'some of fields are missing'},
                            status=400)
    if points < 0 or points > 50:
        return JsonResponse({'code': 79,
                             'payload': 'wrong points number'},
                            status=400)

    answer_time = datetime.now()
    test = Test.objects.filter(Login=test_login)
    if len(test) == 0:
        return JsonResponse({'code': 78,
                             'payload': 'test not found'},
                            status=404)
    test = test[0]
    test.IQTestPoints = points
    test.IQTestAnswerTime = answer_time
    test.save()

    return JsonResponse({'test_login': test_login,
                         'test_result': {
                             'points': test.IQTestPoints,
                             'answer_datetime': test.IQTestAnswerTime
                             }
                         }, status=200)


@api_view(['POST'])
def AddResultEQ(request):
    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'code': 76,
                             'payload': 'can\'t parse body'},
                            status=400)
    test_login = body.get('test_login')
    answer = body.get('answer')
    if test_login is None or answer is None:
        return JsonResponse({'code': 77,
                             'payload': 'some of fields are missing'},
                            status=400)
    if len(answer) != 5 or not set(answer).issubset({'а', 'б', 'в', 'г', 'д'}):
        return JsonResponse({'code': 79,
                             'payload': 'wrong test answer'},
                            status=400)

    answer_time = datetime.now()
    test = Test.objects.filter(Login=test_login)
    if len(test) == 0:
        return JsonResponse({'code': 78,
                             'payload': 'test not found'},
                            status=404)
    test = test[0]
    test.EQTestResult = answer
    test.EQTestAnswerTime = answer_time
    test.save()

    return JsonResponse({'test_login': test_login,
                         'test_result': {
                             'answer': test.EQTestResult,
                             'answer_datetime': test.EQTestAnswerTime
                             }
                         }, status=200)


@api_view(['GET'])
def GetResult(request, test_login):
    test = Test.objects.filter(Login=test_login)
    if len(test) == 0:
        return JsonResponse({'code': 78,
                             'payload': 'test not found'},
                            status=404)
    test = test[0]

    response = {'test_login': test_login}
    if test.IQTestPoints is not None:
        response['iq_test_result'] = {
            'points': test.IQTestPoints,
            'answer_datetime': test.IQTestAnswerTime
            }
    if test.EQTestResult is not None:
        response['eq_test_result'] = {
            'answer': test.EQTestResult,
            'answer_datetime': test.EQTestAnswerTime
            }

    return JsonResponse(response, status=200)
