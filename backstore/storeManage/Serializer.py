from rest_framework import serializers
from storeManage import models


class TotalStockSerializer(serializers.ModelSerializer):
    total_iden = serializers.CharField(source='totalwarehouse.total_iden')
    total_name = serializers.CharField(source='totalwarehouse.total_name')
    orga_iden = serializers.CharField(source='totalwarehouse.organization.orga_iden')
    orga_name = serializers.CharField(source='totalwarehouse.organization.orga_name')
    material_iden = serializers.CharField(source='material.material_iden')
    material_name = serializers.CharField(source='material.material_name')
    material_specification = serializers.CharField(source='material.material_specification')
    material_model = serializers.CharField(source='material.material_model')
    material_meterage = serializers.CharField(source='material.meterage_name')

    class Meta:
        model = models.TotalStock
        fields = ('id', 'total_iden', 'total_name', 'orga_iden', 'orga_name',
                  'material_iden', 'material_name', 'material_specification',
                  'material_model', 'material_meterage', 'ts_present_num', 'ts_present_price',
                  'ts_present_sum')


class TotalStockToTrSerializer(serializers.ModelSerializer):
    trd_iden = serializers.CharField(source='material.material_iden')
    trd_name = serializers.CharField(source='material.material_name')
    trd_specification = serializers.CharField(source='material.material_specification')
    trd_model = serializers.CharField(source='material.material_model')
    trd_meterage = serializers.CharField(source='material.meterage_name')
    trd_present_num = serializers.IntegerField(source='ts_present_num')

    class Meta:
        model = models.TotalStock
        fields = ('id', 'trd_iden', 'trd_name', 'trd_specification',
                  'trd_model', 'trd_meterage', 'trd_present_num')
