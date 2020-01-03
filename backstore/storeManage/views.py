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

    def get(self, request):
        user_now = UserNow.objects.get()
        if user_now:
            area_name = user_now.area_name
            total_stocks = models.TotalStock.objects.filter(totalwarehouse__organization__area_name=area_name)
            if total_stocks:
                total_stocks_serializer = TotalStockSerializer(total_stocks, many=True)
                return Response({"total_stocks": total_stocks_serializer.data})
            else:
                return Response({"message": "未查询到当地仓储信息"})
        else:
            return Response({"message": "用户未登录"})
