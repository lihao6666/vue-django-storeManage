from django.shortcuts import render
from django.db.models import Max
from rest_framework.views import APIView
from .Serializer import PCSerializer, CdDSerializer, CdPaySerializer, POSerializer, OrDSerializer
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, redirect
from purchase import models
from purchaseRequest.models import PurchaseRequest, PrDetail
from purchaseRequest.Serializer import PurchaseRequestSerializer, PrDetailSerializer, PrDetail2Serializer
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

        if power == '1':
            pcs = models.PurchaseContract.objects.filter(~Q(pc_status=0), organization__area_name=self.area_name).all()
        elif power == '2':
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


class PCNewView(APIView):
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
                 "pays": pays_serializer.data, "signal": 1})


class PcUpdateView(APIView):
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
            max_id = models.PurchaseContract.objects.all().aggregate(Max('pc_serial'))['pc_serial__max']
            if max_id:
                pc_serial = str(int(max_id) + 1).zfill(4)
            else:
                pc_serial = "0001"
            pc_new_iden = pre_iden + pc_serial
            self.pc_new_iden = pc_new_iden
            try:
                if models.PurchaseContract.objects.create(pc_iden=self.pc_new_iden, pc_serial=pc_serial,
                                                          organization=organization, pc_name=pc_name, supplier=supplier,
                                                          pc_date=pc_date, pc_sum=pc_sum, pc_remarks=pc_remarks,
                                                          pc_status=0, pc_creator=self.user_now_name,
                                                          pc_creator_iden=user_now_iden):

                    self.message = "新建采购合同成功"
                    self.signal = 0
                else:
                    self.message = "新建采购合同失败"
                    self.signal = 1
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
        return Response({"message": self.message, "signal": self.signal, "pc_new_iden": self.pc_new_iden})


class CdDetailSaveView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "合同详情保存成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        cds = json_data['cds']
        pc_iden = json_data['pc_iden']
        pays = json_data['pays']
        models.CdDetail.objects.filter(purchase_contract__pc_iden=pc_iden).delete()
        pc = models.PurchaseContract.objects.get(pc_iden=pc_iden)
        pc_sum = json_data['pc_sum']
        models.PurchaseContract.objects.filter(pc_iden=pc_iden).update(pc_sum=pc_sum)
        for cd in cds:
            cd_iden = cd['cd_iden']
            material = Material.objects.get(material_iden=cd_iden)
            cd_num = cd['cd_num']  # 销售数量
            cd_taxRate = cd['cd_taxRate']
            cd_tax_unitPrice = cd['cd_tax_unitPrice']
            cd_unitPrice = cd['cd_unitPrice']
            cd_tax_sum = cd['cd_tax_sum']
            cd_sum = cd['cd_sum']
            cd_tax_price = cd['cd_tax_price']
            cd_pr_iden = cd['cd_pr_iden']
            cd_prd_remarks = cd['cd_prd_remarks']
            # PrDetail.objects.filter(purchase_request__pr_iden=pc_iden, prd_iden=cd_iden).update(prd_uesd=1)
            # 更新请购单物料使用状态
            try:
                if models.CdDetail.objects.create(purchase_contract=pc, material=material,
                                                  cd_num=cd_num, cd_taxRate=cd_taxRate,
                                                  cd_tax_unitPrice=cd_tax_unitPrice,
                                                  cd_unitPrice=cd_unitPrice,
                                                  cd_tax_sum=cd_tax_sum, cd_sum=cd_sum, cd_tax_price=cd_tax_price,
                                                  cd_pr_iden=cd_pr_iden,
                                                  cd_prd_remarks=cd_prd_remarks):
                    pass
                else:
                    self.message = "合同详情保存失败"
                    self.signal = 1

            except:
                print(pc_iden)
                print(cd_iden)
                self.message = "合同详情保存失败"
                self.signal = 1
        models.CdPayDetail.objects.filter(purchase_contract__pc_iden=pc_iden).delete()
        for pay in pays:
            pay_batch = pay['pay_batch']
            pay_rate = pay['pay_rate']
            pay_price = pay['pay_price']
            pay_planDate = pay['pay_planDate']
            pay_prepay = pay['pay_prepay']
            pay_remarks = pay['pay_remarks']
            try:
                if models.CdPayDetail.objects.create(purchase_contract=pc, pay_batch=pay_batch, pay_rate=pay_rate,
                                                     pay_price=pay_price, pay_planDate=pay_planDate,
                                                     pay_prepay=pay_prepay,
                                                     pay_remarks=pay_remarks):
                    pass
                else:
                    self.message = "合同详情保存失败"
                    self.signal = 1
            except:
                self.message = "合同详情保存失败"
                self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class CdDetailSubmitView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_now_name = ""
        self.area_name = ""
        self.message = "合同明细提交成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name
        pc_iden = json_data['pc_iden']
        cds = json_data['cds']
        try:
            if models.PurchaseContract.objects.filter(pc_iden=pc_iden).update(pc_status=1):
                pass
            else:
                self.message = "合同明细提交失败"
                self.signal = 1
        except:
            self.message = "合同明细提交失败"
            self.signal = 1

        for cd in cds:
            cd_iden = cd['cd_iden']
            cd_pr_iden = cd['cd_pr_iden']
            PrDetail.objects.filter(purchase_request__pr_iden=cd_pr_iden, prd_iden=cd_iden).update(prd_uesd=1)
            prds = PrDetail.objects.filter(purchase_request__pr_iden=cd_pr_iden).all()
            pr = PurchaseRequest.objects.filter(pr_iden=cd_pr_iden)
            flag = 0
            for prd in prds:
                if prd.prd_used == 0:
                    flag = 1
            if flag == 0:
                pr.update(pr_status=2, pr_closer=self.user_now_name, pr_closer_iden=user_now_iden,
                          pr_closeDate=timezone.now, pr_closeReason="自动关闭")
            # 更新请购单物料使用状态

        return Response({'message': self.message, 'signal': self.signal})


class CdDetailNewView(APIView):
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
            prds = PrDetail.objects.filter(purchase_request__organization__area_name=self.area_name,
                                           purchase_request__pr_status=1,
                                           prd_used=0).all()
            prds_serializer = PrDetail2Serializer(prds, many=True)
            return Response({"prds": prds_serializer.data, 'signal': 0})
        else:
            prds = PrDetail.objects.filter(purchase_request__organization__orga_name=orga_name,
                                           purchase_request__organization__area_name=self.area_name,
                                           purchase_request__pr_status=1,
                                           prd_used=0).all()
            prds_serializer = PrDetail2Serializer(prds, many=True)
            return Response({"prds": prds_serializer.data, 'signal': 0})


# class CdDetailNewSaveView(APIView):
#
#     def post(self):
#         json_data = json.loads(self.request.body.decode("utf-8"))
#         pc_iden = json_data['pc_iden']
#         pc = models.PurchaseContract.objects.get(pc_iden=pc_iden)
#         pr_iden = json_data['pr_iden']
#         prds = json_data['prds']
#         for prd in prds:
#             prd_iden = prd['prd_iden']
#             prd_num = prd['prd_num']
#             material = Material.objects.get(material_iden=prd_iden)
#             # pr = PurchaseRequest.objects.get(pr_iden=pr_iden)
#             # 这里面请购单的userd状态还没有改，后面要判断
#             try:
#                 models.CdDetail.objects.create(purchase_contract=pc, material=material,
#                                                cd_num=prd_num, cd_pr_iden=pr_iden)
#             except:
#                 return Response({"message": "新建合同物料详情出现错误"})
#         return Response({"message": "新建合同物料详情成功", "signal": 0})


# class CdDetailDeleteView(APIView):
#
#     def post(self, request):
#         json_data = json.loads(self.request.body.decode("utf-8"))
#         cds = json_data['cds']
#         for cd in cds:
#             # cd_rp_iden = cd['cd_rp_iden'] # 请购单号
#             cd_iden = cd['cd_iden']  # 物料编码
#             try:
#                 models.CdDetail.objects.filter(cd_iden=cd_iden).delete()
#             except:
#                 return Response({"message": "删除物料错误"})
#         return Response({"message": "删除物料成功", "signal": 0})


class PcDeleteView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "删除合同成功"
        self.signal = 0

    def post(self, request):
        """
        需要数据为合同编号
        """
        json_data = json.loads(self.request.body.decode("utf-8"))
        pc_iden = json_data['pc_iden']

        try:
            if models.PurchaseContract.objects.filter(pc_iden=pc_iden).delete()[0]:
                pass
            else:
                self.message = "删除合同失败"
                self.signal = 1
        except:
            self.message = "删除合同失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
采购订单
"""


class POsView(APIView):
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

        if power == '1':
            pos = models.PurchaseOrder.objects.filter(~Q(po_status=0), organization__area_name=self.area_name).all()
        elif power == '2':
            pos = models.PurchaseOrder.objects.filter(po_creator_iden=user_now_iden,
                                                      organization__area_name=self.area_name).all()
        else:
            pos1 = models.PurchaseOrder.objects.filter(~Q(po_status=0), organization__area_name=self.area_name).all()
            pos2 = models.PurchaseOrder.objects.filter(po_creator_iden=user_now_iden,
                                                       organization__area_name=self.area_name).all()
            pos = pos1 | pos2
        if pos:
            pos_serializer = POSerializer(pos, many=True)
            return Response({"pos": pos_serializer.data, "signal": 0})
        else:
            return Response({"message": "未查询到信息"})


class PONewView(APIView):
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
            po_iden = json_data['po_iden']
        except:

            return Response({"orga_names": orga_names, "supply_names": supply_names, "signal": 0})
        else:
            ords = models.OrDetail.objects.filter(purchase_order__po_iden=po_iden).all()
            ords_serializer = OrDSerializer(ords, many=True)
            return Response({"supply_names": supply_names, "ords": ords_serializer.data, "signal": 1})


class PrChoiceView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_now_name = ""
        self.area_name = ""
        self.prds_serializer = ""

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
            prds = PrDetail.objects.filter(purchase_request__organization__area_name=self.area_name,
                                           purchase_request__pr_status=1,
                                           prd_used=0).all()
            self.prds_serializer = PrDetail2Serializer(prds, many=True)
        else:
            prds = PrDetail.objects.filter(purchase_request__organization__orga_name=orga_name,
                                           purchase_request__organization__area_name=self.area_name,
                                           purchase_request__pr_status=1,
                                           prd_used=0).all()
            self.prds_serializer = PrDetail2Serializer(prds, many=True)
        finally:
            return Response({"prds": self.prds_serializer.data, 'signal': 0})


# class PONewByPcView(APIView):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.user_now_name = ""
#         self.area_name = ""
#         self.pcs = ""
#
#     def post(self, request):
#         json_data = json.loads(self.request.body.decode("utf-8"))
#         user_now_iden = json_data['user_now_iden']
#         user_now = UserNow.objects.get(user_iden=user_now_iden)
#         if user_now:
#             self.user_now_name = user_now.user_name
#             self.area_name = user_now.area_name
#         orga_names =
#         try:
#             po_iden = json_data['po_iden']
#         except:
#             # self.pcs = models.PurchaseContract.objects.filter(organization__area_name=self.area_name,
#             #                                                   pc_status=1).all()
#             # pcs_serializer = PCSerializer(self.pcs, many=True)
#             # cds_list = []
#             # for pc in self.pcs:
#             #     pc_iden = pc.pc_iden
#             #     cds = models.CdDetail.objects.filter(purchase_contract__pc_iden=pc_iden).all()
#             #     cds_serializer = CdDSerializer(cds, many=True)
#             #     cds_list.append(cds_serializer.data)
#             # return Response({"pcs": pcs_serializer.data, "cds": cds_list, "signal": 0})  # 合同和对应的合同明细
#             return Response({})
#         else:
#             ods = models.OrDetail.objects.filter(purchase_order__po_iden=po_iden).all()
#             ods_serializer = OrDSerializer(ods, many=True)
#             return Response({"ods": ods_serializer.data, "signal": 1})


class PcChoiceView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_now_name = ""
        self.area_name = ""
        self.pcs = ""

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
            self.pcs = models.PurchaseContract.objects.filter(organization__area_name=self.area_name,
                                                              pc_status=1).all()
        else:
            self.pcs = models.PurchaseContract.objects.filter(organization__area_name=self.area_name,
                                                              organization__orga_name=orga_name,
                                                              pc_status=1).all()
        finally:
            pcs_serializer = PCSerializer(self.pcs, many=True)
            cds_list = []
            for pc in self.pcs:
                pc_iden = pc.pc_iden
                cds = models.CdDetail.objects.filter(purchase_contract__pc_iden=pc_iden).all()
                cds_serializer = CdDSerializer(cds, many=True)
                cds_list.append(cds_serializer.data)
            return Response({"pcs": pcs_serializer.data, "cds": cds_list, "signal": 0})  # 合同和对应的合同明细


class POUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0
        self.user_now_name = ""
        self.area_name = ""
        self.po_new_iden = ""

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
        po_date = json_data['po_date']
        po_sum = json_data['po_sum']
        po_remarks = json_data['po_remarks']

        try:
            po_iden = json_data['po_iden']
        except:
            date_str = timezone.now().strftime("%Y-%m-%d")
            date = "".join(date_str.split("-"))
            pre_iden = "PO" + date
            max_id = models.PurchaseOrder.objects.all().aggregate(Max('po_serial'))['po_serial__max']
            if max_id:
                po_serial = str(int(max_id) + 1).zfill(4)
            else:
                po_serial = "0001"
            po_new_iden = pre_iden + po_serial
            self.po_new_iden = po_new_iden
            try:
                if models.PurchaseContract.objects.create(po_iden=po_new_iden, po_serial=po_serial,
                                                          organization=organization, supplier=supplier,
                                                          po_date=po_date, po_sum=po_sum, po_remarks=po_remarks,
                                                          po_status=0, po_creator=self.user_now_name,
                                                          po_creator_iden=user_now_iden):

                    self.message = "新建采购订单成功"
                    self.signal = 0
                else:
                    self.message = "新建采购订单失败"
                    self.signal = 1
            except:
                self.message = "新建采购订单失败"
                self.signal = 1
        else:
            po = models.PurchaseContract.objects.get(po_iden=po_iden)
            if po:
                po.update(organization=organization, supplier=supplier, po_date=po_date,
                          po_sum=po_sum, po_remarks=po_remarks)
            else:
                self.message = "更新失败"
                self.signal = 1
        return Response({"message": self.message, "signal": self.signal, "po_new_iden": self.po_new_iden})


class POSaveView(APIView):
    """
    为了实现接口通用，通过发送来源合同字段
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "采购订单详情保存成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        ods = json_data['ods']
        po_iden = json_data['po_iden']
        models.OrDetail.objects.filter(purchase_order__po_iden=po_iden).delete()
        po = models.PurchaseOrder.objects.get(po_iden=po_iden)
        for od in ods:
            od_iden = od['od_iden']  # 物料编号
            od_num = od['od_num']  # 销售数量
            od_taxRate = od['od_taxRate']
            od_tax_unitPrice = od['od_tax_unitPrice']
            od_unitPrice = od['od_unitPrice']
            od_tax_sum = od['od_tax_sum']
            od_sum = od['od_sum']
            od_tax_price = od['od_tax_price']
            od_pr_iden = od['od_pr_iden']
            od_prd_remarks = od['od_remarks']
            material = Material.objects.get(material_iden=od_iden)
            try:
                if models.OrDetail.objects.create(purchase_order=po, material=material, od_num=od_num,
                                                  od_taxRate=od_taxRate, od_tax_unitPrice=od_tax_unitPrice,
                                                  od_tax_sum=od_tax_sum, od_sum=od_sum, od_unitPrice=od_unitPrice,
                                                  od_tax_price=od_tax_price, od_pr_iden=od_pr_iden,
                                                  od_prd_remarks=od_prd_remarks):
                    pass
                else:
                    self.message = "采购订单详情保存失败"
                    self.signal = 1
            except:
                self.message = "采购订单详情保存失败"
                self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


class POSubmitView(APIView):
    """
   为了实现接口通用，通过发送来源合同字段
   """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_now_name = ""
        self.area_name = ""
        self.message = "请购单提交成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
            self.area_name = user_now.area_name
        po_iden = json_data['po_iden']
        ods = json_data['ods']
        pc_iden = json_data['pc_iden']  # 标识是来自合同还是请购单

        try:
            if models.PurchaseOrder.objects.filter(po_iden=po_iden).update(po_status=1):
                pass
            else:
                self.message = "请购单提交失败"
                self.signal = 1
        except:
            self.message = "请购单提交失败"
            self.signal = 1

        if pc_iden:
            pass
        else:
            for od in ods:
                od_iden = od['od_iden']
                od_pr_iden = od['od_pr_iden']
                PrDetail.objects.filter(purchase_request__pr_iden=od_pr_iden, prd_iden=od_iden).update(prd_uesd=1)
                prds = PrDetail.objects.filter(purchase_request__pr_iden=od_pr_iden).all()
                pr = PurchaseRequest.objects.filter(pr_iden=od_pr_iden)
                flag = 0
                for prd in prds:
                    if prd.prd_used == 0:
                        flag = 1
                if flag == 0:
                    pr.update(pr_status=2, pr_closer=self.user_now_name, pr_closer_iden=user_now_iden,
                              pr_closeDate=timezone.now(), pr_closeReason="自动关闭")

                # 更新请购单物料使用状态


class PODeleteView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "删除采购订单成功"
        self.signal = 0

    def post(self, request):

        json_data = json.loads(self.request.body.decode("utf-8"))
        po_iden = json_data['po_iden']

        try:
            if models.PurchaseOrder.objects.filter(po_iden=po_iden).delete()[0]:
                pass
            else:
                self.message = "删除采购订单失败"
                self.signal = 1

        except:
            self.message = "删除采购订单失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})
