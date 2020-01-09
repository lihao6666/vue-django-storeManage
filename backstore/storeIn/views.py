from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from .Serializer import BisDSerializer, BisSerializer
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, redirect
from storeIn import models
from base.models import Organization, Material, Department, UserNow, Supplier, TotalWareHouse
from base.Serializer import MaterialSerializer
from storeManage.models import TotalStock
import json
from django.db.models import Q, Sum


class BissView(APIView):
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

        power = json_data['power']
        print(power)

        if power == '1':
            biss = models.BuyInStore.objects.filter(~Q(bis_status=0), organization__area_name=self.area_name).all()
        elif power == '2':
            biss = models.BuyInStore.objects.filter(bis_creator_iden=user_now_iden,
                                                    organization__area_name=self.area_name).all()
        else:
            biss1 = models.BuyInStore.objects.filter(~Q(bis_status=0), organization__area_name=self.area_name).all()
            biss2 = models.BuyInStore.objects.filter(bis_creator_iden=user_now_iden,
                                                     organization__area_name=self.area_name).all()
            biss = biss1 | biss2
        if biss:
            biss_serializer = BisSerializer(biss, many=True)
            return Response({"biss": biss_serializer.data, "signal": 0})
        else:
            return Response({"message": "未查询到信息"})


class BisNewView(APIView):
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
        orga_names = Organization.objects.filter(area_name=self.area_name).values_list("id", "orga_name")
        supply_names = Supplier.objects.filter(supply_status=1).values_list('id', 'supply_name')
        in_ware_houses = TotalWareHouse.objects.filter(organization__area_name=self.area_name, total_status=1). \
            values_list("id", "total_name", "organization__orga_name")
        try:
            bis_iden = json_data['bis_iden']
        except:
            return Response({"supply_names": supply_names, "in_ware_houses": in_ware_houses,
                             "orga_names": orga_names, "signal": 0})
        else:
            bds = models.BisDetail.objects.filter(buy_in_store__bis_iden=bis_iden).all()
            bds_serializer = BisDSerializer(bds, many=True)
            return Response({"supply_names": supply_names, "in_ware_houses": in_ware_houses,
                             "bds": bds_serializer.data, "signal": 1})


class BisUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0
        self.user_now_name = ""
        self.area_name = ""
        self.pc_new_iden = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name
        orga_name = json_data['orga_name']
        organization = Organization.objects.get(area_name=self.area_name, orga_name=orga_name)
        supply_name = json_data['supply_name']
        supplier = Supplier.objects.get(supply_name=supply_name)
        in_ware_house = json_data['in_ware_house']
        in_ware_house = TotalWareHouse.objects.get(organization__area_name=self.area_name,total_name=in_ware_house)
        bis_date =
