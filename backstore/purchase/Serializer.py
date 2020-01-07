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
                  'cd_tax_sum', 'cd_sum', 'cd_tax_price', 'cd_remarks')


class CdPaySerializer(serializers.ModelSerializer):
    pc_iden = serializers.CharField(source='purchase_contract.pc_iden')

    class Meta:
        model = models.CdPayDetail
        fields = ('id', 'pc_iden', 'pay_batch', 'pay_rate', 'pay_price', 'pay_planDate', 'pay_preay', 'pay_remarks')
