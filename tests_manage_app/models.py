from django.db import models


class Test(models.Model):

    Login = models.CharField(primary_key=True, unique=True,
                             db_index=True, max_length=10)
    IQTestPoints = models.IntegerField(null=True)
    IQTestAnswerTime = models.DateTimeField(null=True)
    EQTestResult = models.CharField(max_length=5, null=True)
    EQTestAnswerTime = models.DateTimeField(null=True)
