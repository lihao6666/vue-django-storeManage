from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from storeManage import models
from base.models import Organization, Material, Department
from base.Serializer import MaterialSerializer
import json


class TotalStockView(APIView):

    def get(self, request):
        pass





