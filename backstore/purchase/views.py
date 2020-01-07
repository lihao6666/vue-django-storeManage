from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from .Serializer import PCSerializer,CdDSerializer
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, redirect
from purchase import models
from base.models import Organization, Material, Department, UserNow
from base.Serializer import MaterialSerializer
from storeManage.models import TotalStock
import json
from django.db.models import Q, Sum


class PCsView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_now_name = ""
        self.area_name = ""

    def post(self, request):
        """
        需要获取区域名字，用户编号
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name

        power = json_data['power']
        print(power)

        if power == 1:
            pcs = models.PurchaseContract.objects.filter(~Q(pc_status=0), organization__area_name=self.area_name).all()
        elif power == 2:
            pcs = models.PurchaseContract.objects.filter(pc_creator_iden=user_now_iden,
                                                         organization__area_name=self.area_name).all()
        else:
            prs = models.PurchaseContract.objects.filter(~Q(pc_status=0), organization__area_name=self.area_name).all()






