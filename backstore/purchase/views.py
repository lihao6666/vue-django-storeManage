from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from .Serializer import PCSerializer, CdDSerializer, CdPaySerializer
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, redirect
from purchase import models
from purchaseRequest.models import PurchaseRequest, PrDetail
from purchaseRequest.Serializer import PurchaseRequestSerializer, PrDetailSerializer
from base.models import Organization, Material, Department, UserNow, Supplier
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
            pcs1 = models.PurchaseContract.objects.filter(~Q(pc_status=0), organization__area_name=self.area_name).all()
            pcs2 = models.PurchaseContract.objects.filter(pc_creator_iden=user_now_iden,
                                                          organization__area_name=self.area_name).all()
            pcs = pcs1 | pcs2
        if pcs:
            pcs_serializer = PCSerializer(pcs, many=True)
            return Response({"pcs": pcs_serializer.data, "signal": 0})
        else:
            return Response({"message": "未查询到信息"})


class PCNew(APIView):
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
        supply_names = Supplier.objects.filter(supply_status=1).values_list('id', 'supply_name')
        try:
            pc_iden = json_data['pc_iden']
            orga_name = json_data['orga_name']
        except:
            return Response({"orga_names": orga_names, "supply_names": supply_names, "signal": 0})
        else:
            cds = models.CdDetail.objects.filter(purchase_contract__pc_iden=pc_iden)
            cds_serializer = CdDSerializer(cds, many=True)
            pays = models.CdPayDetail.objects.filter(purchase_contract__pc_iden=pc_iden)
            pays_serializer = CdPaySerializer(pays, many=True)
            return Response(
                {"orga_names": orga_names, "supply_names": supply_names, "cds": cds_serializer.data,
                 "pays": pays_serializer, "signal": 1})


class PcUpdateView(APIView):
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

        orga_name = json_data['orga_name']
        organization = Organization.objects.get(area_name=self.area_name, orga_name=orga_name)
        supply_id = json_data['supply_id']
        supplier = Supplier.objects.get(id=supply_id)
        pc_name = json_data['pc_name']
        pc_date = json_data['pc_date']
        pc_sum = json_data['pc_sum']
        pc_remarks = json_data['pc_remarks']

        try:
            pc_iden = json_data['pc_iden']
        except:
            date_str = timezone.now().strftime("%Y-%m-%d")
            date = "".join(date_str.split("-"))
            pre_iden = "PC" + date
            max_id = models.PurchaseContract.objects.all().aggregate(Max('prc_serial'))['pc_serial__max']
            if max_id:
                pc_serial = str(int(max_id) + 1).zfill(4)
            else:
                pc_serial = "0001"
            pc_new_iden = pre_iden + pc_serial
            try:
                models.PurchaseContract.objects.create(pc_iden=pc_new_iden, pc_serial=pc_serial,
                                                       organization=organization, pc_name=pc_name, supplier=supplier,
                                                       pc_date=pc_date, pc_sum=pc_sum, pc_remarks=pc_remarks,
                                                       pc_status=0, pc_creator=self.user_now_name,
                                                       pc_creator_iden=user_now_iden)
                self.message = "新建采购合同成功"
                self.signal = 0
            except:
                self.message = "新建采购合同失败"
                self.signal = 1
        else:
            pc = models.PurchaseContract.objects.get(pc_iden=pc_iden)
            if pc:
                pc.update(organization=organization, pc_name=pc_name, supplier=supplier, pc_date=pc_date,
                          pc_sum=pc_sum, pc_remarks=pc_remarks)
            else:
                self.message = "更新失败"
                self.signal = 1
        return Response({"message": self.message, "signal": self.signal})


class CdDetailNewView(APIView):

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        organization_name = json_data['orga_name']
        prs = PurchaseRequest.objects.filter(organization__orga_name=organization_name, pr_status=1)
        prs_serializer = PurchaseRequestSerializer(prs, many=True)
        pr_prds = []
        if prs:
            for pr in prs:
                pr_iden = pr.pr_iden
                prds = PrDetail.objects.filter(purchase_request__pr_iden=pr_iden)
                prds_serializer = PrDetailSerializer(prds, many=True)
                pr_prds.append(prds.data)
            return Response({"prs": prs_serializer.data, "pr_prds": pr_prds, "signal": 0})
        else:
            return Response({"message": "莫有请购单，怎么办？"})


class CdDetailNewSaveView(APIView):

    def post(self):
        json_data = json.loads(self.request.body.decode("utf-8"))
        pc_iden = json_data['pc_iden']
        pc = models.PurchaseContract.objects.get(pc_iden=pc_iden)
        pr_iden = json_data['pr_iden']
        prds = json_data['prds']
        for prd in prds:
            prd_iden = prd['prd_iden']
            prd_num = prd['prd_num']
            material = Material.objects.get(material_iden=prd_iden)
            # pr = PurchaseRequest.objects.get(pr_iden=pr_iden)
            # 这里面请购单的userd状态还没有改，后面要判断
            try:
                models.CdDetail.objects.create(purchase_contract=pc, material=material,
                                               cd_num=prd_num, cd_rp_iden=pr_iden)
            except:
                return Response({"message": "新建合同详情出现错误"})
        return Response({"message": "新建合同详情采购", "signal": 0})
