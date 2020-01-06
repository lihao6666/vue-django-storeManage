from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from .Serializer import PurchaseRequestSerializer, PrDetailSerializer
from rest_framework.response import Response
from django.shortcuts import render, redirect
from purchase import models
from base.models import Organization, Material, Department
from base.Serializer import MaterialSerializer
import json

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
    def post(self, request):
        """
        需要获取区域名字，用户编号
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_iden = json_data['user_iden']
        area_name = json_data['area_name']
        # 判断是个人还是采购专员
        if user_iden == "":
            prs = models.PurchaseRequest.objects.filter(area_name=area_name).all()
        else:
            prs = models.PurchaseRequest.objects.filter(pr_creator=user_iden).all()
        if prs:
            prs_serializer = PurchaseRequestSerializer(prs, many=True)
            return Response({"prs": prs_serializer.data})
        else:
            return Response({"message": "未查询到信息"})


class PrNewView(APIView):
    def post(self, request):
        """
        需要获取的数据为区域名字，用户角色发送类似"1-2-3"
        返回的数据为库存组织名字，申请部门名字、是否中心
        """
        dpms = []
        json_data = json.loads(self.request.body.decode("utf-8"))
        area_name = json_data['area_name']
        role = json_data['role']
        orga_names = Organization.objects.filter(area_name=area_name).values_list('orga_name', flat=True)
        roles = map(int, role.split("-"))
        for role in roles:
            dpm = Department.objects.filter(id=role).values_list('id', 'dpm_name', 'dpm_center')
            dpms.append(dpm)
        return Response({"orga_names": orga_names, 'dpms': dpms})


class PrEditView(APIView):
    def post(self, request):
        """
        需要获取请购单状态、区域名字、请购单编号
        """
        message_return = {}
        json_data = json.loads(self.request.body.decode("utf-8"))
        pr_status = json_data['pr_status']
        area_name = json_data['area_name']
        pr_iden = json_data['pr_iden']
        pr = models.PurchaseRequest.objects.get(pr_iden=pr_iden)
        prds = models.PrDetail.objects.filter(purchase_request=pr)
        if prds:
            prds_serializer = PrDetailSerializer(prds, many=True)
            message_return["prds"] = prds_serializer.data
        else:
            message_return["prds"] = ""

        if pr_status == 0:
            orga_names = Organization.objects.filter(area_name=area_name).values_list('orga_name', flat=True)
            message_return["organizations"] = orga_names
        else:
            message_return["message"] = "请购单明细为空"
        return Response(message_return)


class PrUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新请购单成功"
        self.signal = 0

    def post(self, request):
        """
        需要获取请购单编号、区域名字、库存组织名字、部门名称、需求类型、时间、备注
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        pr_iden = json_data['pr_iden']
        pr_date = json_data['pr_date']
        area_name = json_data['area_name']
        orga_name = json_data['orga_name']
        pr_department = json_data['pr_department']
        pr_type = json_data['pr_type']
        pr_remarks = json_data['pr_remarks']
        organization = Organization.objects.get(area_name=area_name, orga_name=orga_name)
        # flag = json_data['flag']  # 判断0就是新增，1就是更新
        if pr_iden == "":
            pr_creator = json_data['pr_creator']
            try:
                max_id = models.PurchaseRequest.objects.all().aggregate(Max('pr_iden'))['pr_iden__max']
                pr_iden = str(int(max_id) + 1)
                models.PurchaseRequest.objects.create(pr_iden=pr_iden, organization=organization, pr_date=pr_date,
                                                      pr_department=pr_department, pr_type=pr_type,
                                                      pr_creator=pr_creator,
                                                      pr_remarks=pr_remarks, pr_status=0
                                                      )
            except:
                self.message = "新建请购单失败"
                self.signal = 1
            else:
                self.message = "新建请购单成功"
                self.signal = 0

            return Response({'message': self.message, 'signal': self.signal})

        else:
            try:
                models.PurchaseRequest.objects.filter(pr_iden=pr_iden).update(
                    organization=organization, pr_date=pr_date, pr_department=pr_department, pr_type=pr_type,
                    pr_remarks=pr_remarks
                )
            except:
                self.message = "更新请购单失败"
                self.signal = 1
            return Response({'message': self.message, 'signal': self.signal})


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
        # pr_iden = json_data['pr_iden']
        prds = json_data['prds']
        for prd in prds:
            prd_iden = prd['prd_iden']  # 物料编码
            prd_num = prd['prd_num']  # 请购数量
            prd_present_num = prd['prd_present_num']  # 实际库存数量
            try:
                models.PrDetail.objects.filter(prd_iden=prd_iden).update(prd_num=prd_num,
                                                                         prd_present_num=prd_present_num)
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
            models.PurchaseRequest.objects.filter(pr_iden=pr_iden).update(pr_status=1)

        except:
            self.message = "请购单提交保存失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class PrdNewView(APIView):
    def get(self, request):
        materials = Material.objects.filter(material_status=1).all()
        if materials:
            materials_serializer = MaterialSerializer(materials, many=True)
            # 现存量单独统计，单独发送字段
            return Response({"materials": materials_serializer.data, "prd_present_num": ""})
        else:
            return Response({"message": "空空如也你不服？"})


class PrdNewSaveView(APIView):
    def post(self, request):
        """
        额外的功能，小程序可能需要
        需要获取物料详情(iden ,现存量，请购量就可以了)，请购单编号
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        pr_iden = json_data['pr_iden']
        prds = json_data['prds']
        for prd in prds:
            prd_iden = prd['prd_iden']
            # prd_num = prd['prd_num']
            prd_present_num = prd['prd_present_num']
            material = Material.objects.get(material_iden=prd_iden)
            pr = models.PurchaseRequest.objects.get(pr_iden=pr_iden)
            try:
                models.PrDetail.objects.create(purchase_request=pr, material=material, prd_num=prd_present_num,
                                               prd_present_num=prd_present_num, prd_used=0)
            except:
                return Response({"message": "新建物料错误"})

        return Response({"message": "新建物料详情成功"})


class PrdDeleteView(APIView):
    def post(self, request):
        """
        需要获取物料编号就可以了
        """
        json_data = json.loads(self.request.body.decode("utf-8"))

        prds = json_data['prds']
        for prd in prds:
            prd_iden = prd['prd_iden']
            try:
                models.PrDetail.objects.filter(prd_iden=prd_iden).delete()
            except:
                return Response({"message": "删除物料错误"})

        return Response({"message": "删除物料成功"})


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
            models.PurchaseRequest.objects.filter(pr_iden=pr_iden).delete()
        except:
            self.message = "删除请购单失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class PrCloseView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "关闭请购单成功"
        self.signal = 0

    def post(self, request):
        """
        需要数据为请购单编号、关闭人、关闭原因
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        pr_iden = json_data['pr_iden']
        pr_closer = json_data['pr_closer']
        pr_closerReason = json_data['pr_closerReason']

        try:
            models.PurchaseRequest.objects.filter(pr_iden=pr_iden).update(pr_status=2, pr_closer=pr_closer,
                                                                          pr_closerReason=pr_closerReason)

        except:
            self.message = "关闭请购单失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})
