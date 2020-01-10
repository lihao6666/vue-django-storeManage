import traceback

from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from .Serializer import BisDSerializer, BisSerializer
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, redirect
from storeIn import models
from purchase.models import OrDetail, PurchaseOrder
from purchase.Serializer import POSerializer, OrDSerializer, OrDToBisDSerializer
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
        self.bis_new_iden = ""

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
        in_ware_house = TotalWareHouse.objects.get(organization__area_name=self.area_name, total_name=in_ware_house)
        bis_date = json_data['bis_date']
        bis_remarks = json_data['bis_remarks']

        try:
            bis_iden = json_data['bis_iden']
        except:
            date_str = timezone.now().strftime("%Y-%m-%d")
            date = "".join(date_str.split("-"))
            pre_iden = "BI" + date
            max_id = models.BuyInStore.objects.all().aggregate(Max('bis_serial'))['bis_serial__max']
            if max_id:
                bis_serial = str(int(max_id) + 1).zfill(4)
            else:
                bis_serial = "0001"
            bis_new_iden = pre_iden + bis_serial
            self.bis_new_iden = bis_new_iden
            try:
                if models.BuyInStore.objects.create(bis_iden=self.bis_new_iden, bis_serial=bis_serial,
                                                    organization=organization, totalwarehouse=in_ware_house,
                                                    supplier=supplier, bis_date=bis_date, bis_remarks=bis_remarks,
                                                    bis_status=0, bis_creator=self.user_now_name,
                                                    bis_creator_iden=user_now_iden):

                    self.message = "新建采购入库单成功"
                    self.signal = 0
                else:
                    self.message = "新建采购入库单失败"
                    self.signal = 1
            except:
                traceback.print_exc()
                self.message = "新建采购入库单失败"
                self.signal = 1
        else:
            bis = models.BuyInStore.objects.filter(bis_iden=bis_iden)
            if bis:
                bis.update(organization=organization, totalwarehouse=in_ware_house, supplier=supplier,
                           bis_date=bis_date,
                           bis_remarks=bis_remarks)
            else:
                self.message = "更新失败"
                self.signal = 1
        return Response({"message": self.message, "signal": self.signal, "bis_new_iden": self.bis_new_iden})


class POChoiceView(APIView):
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
        try:
            orga_name = json_data['orga_name']
        except:
            return Response({"message": "不传了，气死我了"})
        else:
            ods = OrDetail.objects.filter(purchase_order__organization__orga_name=orga_name,
                                          purchase_order__organization__area_name=self.area_name,
                                          purchase_order__po_status=1).all()
            bds_serializer = OrDToBisDSerializer(ods, many=True)
            return Response({"bds": bds_serializer.data, "signal": 1})


class BisDSaveView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "采购入库单详情保存成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        bds = json_data["bds"]
        bis_iden = json_data["bis_iden"]
        models.BisDetail.objects.filter(buy_in_store__bis_iden=bis_iden).delete()
        bis = models.BuyInStore.objects.get(bis_iden=bis_iden)
        for bd in bds:
            bd_iden = bd['bd_iden']
            material = Material.objects.get(material_iden=bd_iden)
            bd_paper_num = bd['bd_paper_num']
            bd_real_num = bd['bd_real_num']
            bd_unitPrice = bd['bd_unitPrice']
            bd_sum = bd['bd_sum']
            po_iden = bd['po_iden']
            pr_iden = bd['pr_iden']

            try:
                if models.BisDetail.objects.create(buy_in_store=bis, material=material, bd_paper_num=bd_paper_num,
                                                   bd_real_num=bd_real_num, bd_unitPrice=bd_unitPrice, bd_sum=bd_sum,
                                                   po_iden=po_iden, pr_iden=pr_iden):
                    pass
                else:
                    self.message = "采购入库单详情保存失败"
                    self.signal = 1
            except:
                traceback.print_exc()
                self.message = "采购入库单详情保存失败"
                self.signal = 1

        return Response({'message': self.message, 'signal': self.signal})


class BisDSubmitView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "采购入库单提交保存成功"
        self.signal = 0
        self.user_now_name = ""
        self.area_name = ""

    def post(self, request):
        """
        提交后将草稿改为已审批，需要数据为
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name

        bis_iden = json_data["bis_iden"]
        bds = json_data["bds"]
        in_ware_house = json_data["in_ware_house"]
        orga_name = json_data["orga_name"]
        try:
            if models.BuyInStore.objects.filter(bis_iden=bis_iden).update(bis_status=1):
                pass
            else:
                self.message = "采购入库单提交保存失败"
                self.signal = 1
        except:
            traceback.print_exc()
            self.message = "采购入库单提交保存失败"
            self.signal = 1
        for bd in bds:
            bd_iden = json_data['bd_iden']  # 物料编码
            bd_real_num = bd['bd_real_num']
            bd_unitPrice = bd['bd_unitPrice']

            totaL_stock = TotalStock.objects.get(totalwarehouse__total_name=in_ware_house,
                                                 totalwarehouse__organization__area_name=self.area_name,
                                                 totalwarehouse__organization__orga_name=orga_name,
                                                 material__material_iden=bd_iden)
            ts_present_num = totaL_stock.ts_present_num
            ts_present_price = totaL_stock.ts_present_price

            ts_new_num = ts_present_num + bd_real_num
            ts_new_price = (bd_real_num * bd_unitPrice + ts_present_num * ts_present_price) / ts_new_num

            try:
                if TotalStock.objects.filter(totalwarehouse__total_name=in_ware_house,
                                             totalwarehouse__organization__area_name=self.area_name,
                                             totalwarehouse__organization__orga_name=orga_name,
                                             material__material_iden=bd_iden).update(ts_present_num=ts_new_num,
                                                                                     ts_present_price=ts_new_price):
                    pass
                else:
                    self.message = "仓库价格更新错误"
                    self.signal = 1
            except:
                traceback.print_exc()
                self.message = "仓库价格更新错误"
                self.signal = 1

        return Response({'message': self.message, 'signal': self.signal})


class BisDeleteView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "删除采购入库单成功"
        self.signal = 0

    def post(self, request):
        """
        需要数据为合同编号
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        bis_iden = json_data['bis_iden']

        try:
            if models.BuyInStore.objects.filter(bis_iden=bis_iden).delete()[0]:
                pass
            else:
                self.message = "删除采购入库单失败"
                self.signal = 1
        except:
            traceback.print_exc()
            self.message = "删除采购入库单失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
其它出库
"""

