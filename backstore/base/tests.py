from django.test import TestCase

# Create your tests here.
from django.test import Client
from base import models


class TestLogin(TestCase):
    def setUp(self):
        models.Area.objects.create(area_name='合肥')
        models.UserProfile.objects.create(user_id='2017214883', user_passwd='079351', user_name='李恒',
                                          user_departments='0-1', user_roles='0-2',user_status=1, area_id=1)
        models.UserProfile.objects.create(user_id='2017214880', user_passwd='079351', user_name='李浩',
                                          user_departments='0-1', user_roles='0-2',user_status=1, area_id=1)

    def testLogin(self):
        c = Client()
        response = c.post('/base/login', {'user_id': '2017214883','user_passwd':'079351'})
        print(response.data)
