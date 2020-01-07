from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from sell import models
from django.utils import timezone
from storeManage.models import TotalStock
from base.models import Organization, Material, Department, UserNow, Customer, TotalWareHouse
from base.Serializer import MaterialSerializer
from .Serializer import SellOrderSerializer, SoDetailSerializer
from storeManage.Serializer import TotalStockSerializer
import json

"""
销售订单模块接口
- 返回销售订单列表
-
"""


class SellOrdersView(APIView):
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
        sos = models.SellOrder.objects.filter(organization__area_name=self.area_name).all()
        if sos:
            sos_serializer = SellOrderSerializer(sos, many=True)
            return Response({"sos": sos_serializer.data})
        else:
            return Response({"message": "未查询到数据"})


class SellOrderNewView(APIView):
    """
    新建和编辑的时候都可以post这个
    返回的数据为组织名字和id、客户名字和id、发货仓库的组织名字，仓库名字和id
    """

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
        organizations = Organization.objects.filter(area_name=self.area_name).values_list("id", "orga_name")
        customers = Customer.objects.values_list("id", "customer_name")
        deliver_ware_houses = TotalWareHouse.objects.filter(organization__area_name=self.area_name). \
            values_list("id", "total_name", "organization__orga_name")

        try:
            so_iden = json_data['so_iden']
        except:
            return Response(
                {"organizations": organizations, "customers": customers, "deliver_ware_houses": deliver_ware_houses,
                 "signal": 0})
        else:
            sods = models.SoDetail.objects.filter(sell_order__so_iden=so_iden)
            sods_serializers = SoDetailSerializer(sods, many=True)

            return Response(
            {"organizations": organizations, "customers": customers, "deliver_ware_houses": deliver_ware_houses,
             "sods": sods_serializers.data,"signal":1})


class SellOrderUpdateView(APIView):
    """
        只读取添加的数据，订单号自动生成，用于保存新增和编辑的订单
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0
        self.user_now_name = ""
        self.area_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name
        orga_id = json_data['organization']['id']
        organization = Organization.objects.get(id=orga_id)
        customer_id = json_data['customer']['id']
        customer = Customer.objects.get(id=customer_id)
        deliver_ware_house_id = json_data['deliver_ware_house']['id']
        deliver_ware_house = TotalWareHouse.objects.get(id=deliver_ware_house_id).total_name
        deliver_ware_house_iden = TotalWareHouse.objects.get(id=deliver_ware_house_id).total_iden
        so_type = json_data['so_type']
        so_date = json_data['so_date']
        so_remarks = json_data['so_remarks']

        try:
            so_iden = json_data['so_iden']
        except:
            date_str = timezone.now().strftime("%Y-%m-%d")
            date = "".join(date_str.split("-"))
            pre_iden = "SO" + date
            max_id = models.SellOrder.objects.all().aggregate(Max('so_serial'))['so_serial__max']
            if max_id:
                so_serial = str(int(max_id) + 1)
            else:
                so_serial = "0001"
            so_new_iden = pre_iden + so_serial
            try:
                models.SellOrder.objects.create(so_iden=so_new_iden, so_serial=so_serial, organization=organization,
                                                so_type=so_type, customer=customer, so_date=so_date,
                                                deliver_ware_house=deliver_ware_house,
                                                deliver_ware_house_iden=deliver_ware_house_iden, so_remarks=so_remarks,
                                                so_status=0, so_creator=self.user_now_name,
                                                so_creator_iden=user_now_iden)
                self.message = "新建销售订单成功"
                self.signal = 0
            except:
                self.message = "新建销售订单失败"
                self.signal = 1


        else:
            so = models.SellOrder.objects.get(so_iden=so_iden)
            if so:
                so.Update(organization=organization, so_type=so_type, customer=customer, so_date=so_date,
                          deliver_ware_house=deliver_ware_house,
                          deliver_ware_house_iden=deliver_ware_house_iden, so_remarks=so_remarks)
            else:
                self.message = "更新失败"
                self.signal = 1


class SoDetailNewView(APIView):

    def get(self, request):
        materials = Material.objects.filter(material_status=1).all()
        if materials:
            materials_serializer = MaterialSerializer(materials, many=True)
            # 现存量单独统计，单独发送字段

            return Response({"materials": materials_serializer.data, "prd_present_num": ""})
        else:
            return Response({"message": "空空如也你不服？"})


class SoDetailSaveView(APIView):
    pass
