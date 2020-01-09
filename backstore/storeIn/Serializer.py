from rest_framework import serializers
from storeIn import models


class BisSerializer(serializers.ModelSerializer):
    orga_name = serializers.CharField(source='organization.orga_name')
    area_name = serializers.CharField(source='organization.area_name')

    supply_name = serializers.CharField(source='supplier.supply_name')
    supply_iden = serializers.CharField(source='supplier.supply_iden')

    total_name = serializers.CharField(source='totalwarehouse.total_name')

    class Meta:
        model = models.BuyInStore
        fields = ('id', 'orga_name', 'area_name', 'total_name', 'supply_name', 'supply_iden', 'bis_iden', 'bis_date',
                  'bis_remarks', 'bis_status', 'bis_creator', 'bis_creator_iden', 'bis_createDate')


class BisDSerializer(serializers.ModelSerializer):
    bis_iden = serializers.CharField(source='buy_in_store.bis_iden')
    bd_iden = serializers.CharField(source='material.material_iden')
    bd_name = serializers.CharField(source='material.material_name')
    bd_specification = serializers.CharField(source='material.material_specification')
    bd_model = serializers.CharField(source='material.material_model')
    bd_meterage = serializers.CharField(source='material.meterage_name')

    class Meta:
        model = models.BisDetail
        fields = ('id', 'bis_iden', 'bd_iden', 'bd_name', 'bd_specification',
                  'bd_model', 'bd_meterage', 'bd_paper_num', 'bd_real_num', 'bd_unitPrice', 'bd_sum', 'po_iden',
                  'pr_iden')
