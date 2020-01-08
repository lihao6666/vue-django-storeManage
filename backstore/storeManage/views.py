from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from storeManage import models
from base.models import UserNow, Area
from base.models import Organization, Material, Department
from .Serializer import TotalStockSerializer
import json


class TotalStockView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_now_name = ""
        self.area_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name

        total_stocks = models.TotalStock.objects.filter(totalwarehouse__organization__area_name=self.area_name)
        if total_stocks:
            total_stocks_serializer = TotalStockSerializer(total_stocks, many=True)
            return Response({"total_stocks": total_stocks_serializer.data})
        else:
            return Response({"message": "未查询到当地仓储信息"})
