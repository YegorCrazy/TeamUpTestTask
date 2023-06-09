from django.urls import path

from .views import *

urlpatterns = [
    path('create/', CreateTest),
    path('add_result/iq/', AddResultIQ),
    path('add_result/eq/', AddResultEQ),
    path('get_result/<slug:test_login>/', GetResult),
    ]
