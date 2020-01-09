from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from .Serializer import PurchaseRequestSerializer, PrDetailSerializer
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, redirect
from purchaseRequest import models
from base.models import Organization, Material, Department, UserNow
from base.Serializer import MaterialSerializer
from storeManage.models import TotalStock
import json
from django.db.models import Q, Sum
import traceback

"""
请购单模块接口
- 返回请购单列表(个人的和所在地域全部的）
- 编辑业务需要返回需要的数据(需要判断是否为草稿状态，如果是，返回库存组织选择，返回申请部门和明细数据)
- 更新业务
-- 更新请购单
-- 提交请购单
-- 保存请购单
- 删除业务(前端实现）
- 关闭业务
"""


class PrsView(APIView):
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
        # 判断是个人还是采购专员
        if power == '1':
            prs = models.PurchaseRequest.objects.filter(~Q(pr_status=0), organization__area_name=self.area_name).all()
        elif power == '2':
            prs = models.PurchaseRequest.objects.filter(pr_creator_iden=user_now_iden,
                                                        organization__area_name=self.area_name).all()
        else:
            prs1 = models.PurchaseRequest.objects.filter(~Q(pr_status=0), organization__area_name=self.area_name).all()
            prs2 = models.PurchaseRequest.objects.filter(pr_creator_iden=user_now_iden,
                                                         organization__area_name=self.area_name).all()
            prs = prs1 | prs2
        if prs:
            prs_serializer = PurchaseRequestSerializer(prs, many=True)
            return Response({"prs": prs_serializer.data, "signal": 0})
        else:
            return Response({"message": "未查询到信息"})


class PrNewView(APIView):
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

        orga_names = Organization.objects.filter(area_name=self.area_name, orga_status=1).values_list('id', 'orga_name')
        dpms = Department.objects.filter(dpm_status=1).values_list('id', 'dpm_name', 'dpm_center')
        try:
            pr_iden = json_data['pr_iden']
            orga_name = json_data['orga_name']
        except:
            return Response({"orga_names": orga_names, "dpms": dpms, "signal": 0})
        else:
            prds = models.PrDetail.objects.filter(purchase_request__pr_iden=pr_iden)
            prds_serializers = PrDetailSerializer(prds, many=True)
            prds_present_num = []
            for prd in prds:
                material = prd.material
                prd_present_num = TotalStock.objects.filter(totalwarehouse__organization__orga_name=orga_name,
                                                            totalwarehouse__organization__area_name=self.area_name,
                                                            material=material).aggregate(
                    prd_present_num=Sum('ts_present_num'))['prd_present_num']
                if prd_present_num:
                    pass
                else:
                    prd_present_num = 0
                prds_present_num.append(prd_present_num)

            return Response({"orga_names": orga_names, 'dpms': dpms, "prds": prds_serializers.data,
                             "prds_present_num": prds_present_num, "signal": 1})


# class PrUpdateView(APIView):
#     """
#         只读取添加的数据，订单号自动生成，用于保存新增和编辑的订单
#         """
#
#     def post(self, request):
#
#         message_return = {}
#         json_data = json.loads(self.request.body.decode("utf-8"))
#         pr_status = json_data['pr_status']
#         area_name = json_data['area_name']
#         pr_iden = json_data['pr_iden']
#         pr = models.PurchaseRequest.objects.get(pr_iden=pr_iden)
#         prds = models.PrDetail.objects.filter(purchase_request=pr)
#         if prds:
#             prds_serializer = PrDetailSerializer(prds, many=True)
#             message_return["prds"] = prds_serializer.data
#         else:
#             message_return["prds"] = ""
#
#         if pr_status == 0:
#             orga_names = Organization.objects.filter(area_name=area_name).values_list('orga_name', flat=True)
#             message_return["organizations"] = orga_names
#         else:
#             message_return["message"] = "请购单明细为空"
#         return Response(message_return)


class PrUpdateView(APIView):
    """
       只读取添加的数据，订单号自动生成，用于保存新增和编辑的订单
       """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0
        self.user_now_name = ""
        self.area_name = ""
        self.pr_new_iden = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name
        orga_name = json_data['orga_name']
        organization = Organization.objects.get(area_name=self.area_name, orga_name=orga_name)
        department_name = json_data['pr_department']
        pr_type = json_data['pr_type']
        pr_date = json_data['pr_date']
        pr_remarks = json_data['pr_remarks']

        try:
            pr_iden = json_data['pr_iden']
        except:
            date_str = timezone.now().strftime("%Y-%m-%d")
            date = "".join(date_str.split("-"))
            pre_iden = "PR" + date
            max_id = models.PurchaseRequest.objects.all().aggregate(Max('pr_serial'))['pr_serial__max']
            if max_id:
                pr_serial = str(int(max_id) + 1).zfill(4)
            else:
                pr_serial = "0001"
            pr_new_iden = pre_iden + pr_serial
            self.pr_new_iden = pr_new_iden
            try:
                res = models.PurchaseRequest.objects.create(pr_iden=pr_new_iden, pr_serial=pr_serial,
                                                            organization=organization, pr_department=department_name,
                                                            pr_type=pr_type, pr_date=pr_date,
                                                            pr_remarks=pr_remarks,
                                                            pr_status=0, pr_creator=self.user_now_name,
                                                            pr_creator_iden=user_now_iden)
                if res:
                    self.message = "新建请购单成功"
                    self.signal = 0
                else:
                    self.message = "新建请购单失败"
                    self.signal = 1
            except:
                self.message = "新建请购单失败"
                self.signal = 1
        else:
            pr = models.PurchaseRequest.objects.get(pr_iden=pr_iden)
            if pr:
                if pr.update(organization=organization, pr_department=department_name, pr_type=pr_type, pr_date=pr_date,
                             pr_remarks=pr_remarks):
                    pass
                else:
                    self.message = "更新失败"
                    self.signal = 1
            else:
                self.message = "更新失败"
                self.signal = 1
        return Response({"message": self.message, "signal": self.signal, "pr_new_iden": self.pr_new_iden})


class PrdSaveView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "请购单详情保存成功"
        self.signal = 0

    def post(self, request):
        """
        需要获取物料详情信息(主要是iden和请购数量）
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        pr_iden = json_data['pr_iden']

        prds = json_data['prds']
        models.PrDetail.objects.filter(purchase_request__pr_iden=pr_iden).delete()
        pr = models.PurchaseRequest.objects.get(pr_iden=pr_iden)
        for prd in prds:
            prd_iden = prd['prd_iden']  # 物料编码
            # id = prd['prd_id']  # 物料id
            prd_num = prd['prd_num']  # 请购数量
            prd_present_num = prd['prd_present_num']  # 实际库存数量
            prd_remarks = prd['prd_remarks']
            material = Material.objects.get(material_iden=prd_iden)
            try:
                if models.PrDetail.objects.create(purchase_request=pr, prd_num=prd_num,
                                                  material=material,
                                                  prd_used=0,
                                                  prd_present_num=prd_present_num,
                                                  prd_remarks=prd_remarks):
                    pass
                else:
                    self.message = "请购单详情保存失败"
                    self.signal = 1
            except:
                self.message = "请购单详情保存失败"
                self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class PrdSubmitView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "请购单提交成功"
        self.signal = 0

    def post(self, request):
        """
        提交后将草稿改为已审批，需要数据为
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        pr_iden = json_data['pr_iden']

        try:
            if models.PurchaseRequest.objects.filter(pr_iden=pr_iden).update(pr_status=1):
                pass
            else:
                self.message = "请购单提交保存失败"
                self.signal = 1
        except:
            traceback.print_exc()
            self.message = "请购单提交保存失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class PrdNewView(APIView):
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
        orga_name = json_data['orga_name']
        materials = Material.objects.filter(material_status=1).all()

        if materials:
            materials_serializer = MaterialSerializer(materials, many=True)
            prds_present_num = []
            for material in materials:
                prd_present_num = TotalStock.objects.filter(totalwarehouse__organization__orga_name=orga_name,
                                                            totalwarehouse__organization__area_name=self.area_name,
                                                            material=material).aggregate(
                    prd_present_num=Sum('ts_present_num'))['prd_present_num']
                if prd_present_num:
                    pass
                else:
                    prd_present_num = 0
                prds_present_num.append(prd_present_num)

            return Response({"materials": materials_serializer.data, "prds_present_num": prds_present_num, "signal": 0})
        else:
            return Response({"message": "空空如也你不服？"})


# class PrdNewSaveView(APIView):
#     def post(self, request):
#         """
#         需要获取物料详情(iden ,现存量，请购量就可以了)，请购单编号
#         """
#         json_data = json.loads(self.request.body.decode("utf-8"))
#         pr_iden = json_data['pr_iden']
#         prds = json_data['prds']
#         for prd in prds:
#             prd_iden = prd['prd_iden']
#             # prd_num = prd['prd_num']
#             prd_present_num = prd['prd_present_num']
#             material = Material.objects.get(material_iden=prd_iden)
#             pr = models.PurchaseRequest.objects.get(pr_iden=pr_iden)
#             try:
#                 if models.PrDetail.objects.create(purchase_request=pr, material=material, prd_num=prd_present_num,
#                                                   prd_present_num=prd_present_num, prd_used=0):
#                     pass
#                 else:
#                     return Response({"message": "新建物料出现错误"})
#             except:
#                 return Response({"message": "新建物料出现错误"})
#
#         return Response({"message": "新建物料详情成功", "signal": 0})


# class PrdDeleteView(APIView):
#     def post(self, request):
#         """
#         需要获取物料编号就可以了
#         """
#         json_data = json.loads(self.request.body.decode("utf-8"))
#
#         prds = json_data['prds']
#         for prd in prds:
#             prd_iden = prd['prd_iden']
#             try:
#                 if models.PrDetail.objects.filter(prd_iden=prd_iden).delete()[0]:
#                     pass
#                 else:
#                     return Response({"message": "删除物料错误"})
#             except:
#                 return Response({"message": "删除物料错误"})
#
#         return Response({"message": "删除物料成功", "signal": 0})


class PrDeleteView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "删除请购单成功"
        self.signal = 0

    def post(self, request):
        """
        需要数据为请购单编号
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        pr_iden = json_data['pr_iden']

        try:
            if models.PurchaseRequest.objects.filter(pr_iden=pr_iden).delete()[0]:
                pass
            else:
                self.message = "删除请购单失败"
                self.signal = 1
        except:
            traceback.print_exc()
            self.message = "删除请购单失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class PrCloseView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0
        self.user_now_name = ""
        self.area_name = ""
        self.pr_new_iden = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name

        pr_iden = json_data['pr_iden']
        pr_closerReason = json_data['pr_closerReason']

        try:
            if models.PurchaseRequest.objects.filter(pr_iden=pr_iden).update(pr_status=2, pr_closer=self.user_now_name,
                                                                             pr_closer_iden=user_now_iden,
                                                                             pr_closeReason=pr_closerReason):
                pass
            else:
                self.message = "关闭请购单失败"
                self.signal = 1
        except:
            traceback.print_exc()
            self.message = "关闭请购单失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})
