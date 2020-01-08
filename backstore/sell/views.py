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
from django.db.models import Q, Sum
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

        power = json_data['power']
        sos = ""
        if power == 2:
            sos = models.SellOrder.objects.filter(pr_creator_iden=user_now_iden,
                                                  organization__area_name=self.area_name).all()
        elif power == 3:
            sos = models.SellOrder.objects.filter(~Q(pr_status=0), organization__area_name=self.area_name).all()
        if sos:
            sos_serializer = SellOrderSerializer(sos, many=True)
            return Response({"sos": sos_serializer.data, "signal": 0})
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
            orga_name = json_data['orga_name']
        except:
            return Response(
                {"organizations": organizations, "customers": customers, "deliver_ware_houses": deliver_ware_houses,
                 "signal": 0})
        else:
            sods = models.SoDetail.objects.filter(sell_order__so_iden=so_iden)
            sods_serializers = SoDetailSerializer(sods, many=True)
            sods_present_num = []
            for sod in sods:
                material = sod.material
                sod_present_num = TotalStock.objects.filter(material=material,
                                                            totalwarehouse__organization__area_name=self.area_name,
                                                            totalwarehouse__organization__orga_name=orga_name) \
                    .aggregate(sod_present_num=Sum('ts_present_num'))
                sods_present_num.append(sod_present_num)

            return Response(
                {"organizations": organizations, "customers": customers, "deliver_ware_houses": deliver_ware_houses,
                 "sods": sods_serializers.data, "signal": 1})


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
        self.so_new_iden = ""

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
                so_serial = str(int(max_id) + 1).zfill(4)
            else:
                so_serial = "0001"
            so_new_iden = pre_iden + so_serial
            self.so_new_iden = so_new_iden
            try:
                if models.SellOrder.objects.create(so_iden=so_new_iden, so_serial=so_serial, organization=organization,
                                                   so_type=so_type, customer=customer, so_date=so_date,
                                                   deliver_ware_house=deliver_ware_house,
                                                   deliver_ware_house_iden=deliver_ware_house_iden,
                                                   so_remarks=so_remarks,
                                                   so_status=0, so_creator=self.user_now_name,
                                                   so_creator_iden=user_now_iden):
                    self.message = "新建销售订单成功"
                    self.signal = 0
                else:
                    self.message = "新建销售订单失败"
                    self.signal = 1
            except:
                self.message = "新建销售订单失败"
                self.signal = 1


        else:
            so = models.SellOrder.objects.get(so_iden=so_iden)
            if so:
                if so.update(organization=organization, so_type=so_type, customer=customer, so_date=so_date,
                             deliver_ware_house=deliver_ware_house,
                             deliver_ware_house_iden=deliver_ware_house_iden, so_remarks=so_remarks):
                    pass
                else:
                    self.message = "更新失败"
                    self.signal = 1

            else:
                self.message = "更新失败"
                self.signal = 1
        return Response({"message": self.message, "signal": self.signal, "so_new_iden": self.so_new_iden})


class SoDetailSaveView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "销售订单详情保存成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        so_iden = json_data['so_iden']
        sods = json_data['sods']
        for sod in sods:
            # id = sod['id']
            sod_iden = sod['sod_iden']  # 物料编码
            sod_num = sod['sod_num']  # 销售数量
            sod_taxRate = sod['sod_taxRate']
            sod_tax_unitPrice = sod['sod_tax_unitPrice']
            sod_unitPrice = sod['sod_unitPrice']
            sod_tax_sum = sod['sod_tax_sum']
            sod_sum = sod['sod_sum']
            sod_tax_price = sod['sod_tax_price']
            sod_remarks = sod['sod_remarks']

            try:
                if models.SoDetail.objects.filter(sell_order__so_iden=so_iden, sod_iden=sod_iden).update(
                        sod_num=sod_num,
                        sod_taxRate=sod_taxRate,
                        sod_tax_unitPrice=sod_tax_unitPrice,
                        sod_unitPrice=sod_unitPrice,
                        sod_tax_sum=sod_tax_sum,
                        sod_sum=sod_sum,
                        sod_tax_price=sod_tax_price,
                        sod_remarks=sod_remarks):
                    pass
                else:
                    self.message = "销售订单详情保存失败"
                    self.signal = 1
            except:
                self.message = "销售订单详情保存失败"
                self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class SoDetailSubmitView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "销售订单详情提交成功"
        self.signal = 0

    def post(self, request):
        """
        提交后将草稿改为已审批，需要数据为
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        so_iden = json_data['so_iden']

        try:
            if models.SellOrder.objects.filter(so_iden=so_iden).update(so_status=1):
                pass
            else:
                self.message = "销售订单提交保存失败"
                self.signal = 1
        except:
            self.message = "销售订单提交保存失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class SoDetailNewView(APIView):

    def get(self, request):
        materials = Material.objects.filter(material_status=1).all()
        if materials:
            materials_serializer = MaterialSerializer(materials, many=True)
            # 现存量单独统计，单独发送字段

            return Response({"materials": materials_serializer.data, "prd_present_num": ""})
        else:
            return Response({"message": "空空如也你不服？"})


class SoDetailNewSaveView(APIView):

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        so_iden = json_data['so_iden']
        sods = json_data['sods']
        for sod in sods:
            sod_iden = sod['sod_iden']  # 物料编码
            material = Material.objects.get(material_iden=sod_iden)
            so = models.SellOrder.objects.get(so_iden=so_iden)
            try:
                if models.SoDetail.objects.create(sell_order=so, material=material, sod_num=0):
                    pass
                else:
                    return Response({"message": "新建物料错误"})
            except:
                return Response({"message": "新建物料错误"})

        return Response({"message": "新建物料详情成功", "signal": 0})


class SoDetailDeleteView(APIView):
    def post(self, request):
        """
        需要获取物料编号就可以了
        """
        json_data = json.loads(self.request.body.decode("utf-8"))

        sods = json_data['sods']
        for sod in sods:
            sod_iden = sod['sod_iden']
            try:
                if models.SoDetail.objects.filter(sod_iden=sod_iden).delete()[0]:
                    pass
                else:
                    return Response({"message": "删除物料错误"})
            except:
                return Response({"message": "删除物料错误"})

        return Response({"message": "删除物料成功"})


class SellOrderDeleteView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "删除销售订单成功"
        self.signal = 0

    def post(self, request):

        json_data = json.loads(self.request.body.decode("utf-8"))
        so_iden = json_data['so_iden']

        try:
            if models.SellOrder.objects.filter(so_iden=so_iden).delete()[0]:
                pass
            else:
                self.message = "删除销售订单失败"
                self.signal = 1

        except:
            self.message = "删除销售订单失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})

# class SellOrderCloseView(APIView):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.message = "关闭销售订单成功"
#         self.signal = 0
#
#     def post(self, request):
#         """
#         需要数据为请购单编号、关闭人、关闭原因
#         """
#         json_data = json.loads(self.request.body.decode("utf-8"))
#         so_iden = json_data['so_iden']
#         so_closer = json_data['so_closer']
#         so_closerReason = json_data['so_closerReason']
#
#         try:
#             models.PurchaseRequest.objects.filter(so_iden=so_iden).update(so_status=2, so_closer=so_closer,
#                                                                           so_closerReason=so_closerReason)
#
#         except:
#             self.message = "关闭请购单失败"
#             self.signal = 1
#         return Response({'message': self.message, 'signal': self.signal})
