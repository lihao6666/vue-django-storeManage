from rest_framework import serializers
from purchase import models


class PCSerializer(serializers.ModelSerializer):
    orga_name = serializers.CharField(source='organization.orga_name')
    area_name = serializers.CharField(source='organization.area_name')
    supply_name = serializers.CharField(source='supplier.supply_name')
    supply_iden = serializers.CharField(source='supplier.supply_iden')

    class Meta:
        model = models.PurchaseContract
        fields = ('id', 'pc_iden', 'orga_name', 'area_name', 'pc_name', 'supply_name', 'supply_iden', 'pc_date',
                  'pc_sum', 'pc_remarks', 'pc_status', 'pc_creator', 'pc_creator_iden', 'pc_createDate')


class CdDSerializer(serializers.ModelSerializer):
    pc_iden = serializers.CharField(source='purchase_contract.pc_iden')
    cd_iden = serializers.CharField(source='material.material_iden')
    cd_name = serializers.CharField(source='material.material_name')
    cd_specification = serializers.CharField(source='material.material_specification')
    cd_model = serializers.CharField(source='material.material_model')
    cd_meterage = serializers.CharField(source='material.meterage_name')

    class Meta:
        model = models.CdDetail
        fields = ('id', 'cd_iden', 'pc_iden', 'cd_name', 'cd_specification',
                  'cd_model', 'cd_meterage', 'cd_num', 'cd_taxRate', 'cd_tax_unitPrice', 'cd_unitPrice',
                  'cd_tax_sum', 'cd_sum', 'cd_tax_price', 'cd_pr_iden', 'cd_prd_remarks')


class CdPaySerializer(serializers.ModelSerializer):
    pc_iden = serializers.CharField(source='purchase_contract.pc_iden')

    class Meta:
        model = models.CdPayDetail
        fields = ('id', 'pc_iden', 'pay_batch', 'pay_rate', 'pay_price', 'pay_planDate', 'pay_preay', 'pay_remarks')


class POSerializer(serializers.ModelSerializer):
    orga_name = serializers.CharField(source='organization.orga_name')
    area_name = serializers.CharField(source='organization.area_name')
    supply_name = serializers.CharField(source='supplier.supply_name')
    supply_iden = serializers.CharField(source='supplier.supply_iden')

    class Meta:
        model = models.PurchaseOrder
        fields = ('id', 'po_iden', 'po_serial', 'orga_name', 'area_name', 'supply_name', 'supply_iden', 'po_date',
                  'po_sum', 'po_remarks', 'pc_iden', 'po_status', 'po_creator', 'po_creator_iden', 'po_createDate')


class OrDSerializer(serializers.ModelSerializer):
    po_iden = serializers.CharField(source='purchase_order.po_iden')
    od_iden = serializers.CharField(source='material.material_iden')
    od_name = serializers.CharField(source='material.material_name')
    od_specification = serializers.CharField(source='material.material_specification')
    od_model = serializers.CharField(source='material.material_model')
    od_meterage = serializers.CharField(source='material.meterage_name')

    class Meta:
        model = models.OrDetail
        fields = ('id', 'po_iden', 'od_iden', 'od_name', 'od_specification',
                  'od_model', 'od_meterage', 'od_num', 'od_taxRate', 'od_tax_unitPrice', 'od_unitPrice',
                  'od_tax_sum', 'od_sum', 'od_tax_price', 'od_pr_iden', 'od_prd_remarks')
