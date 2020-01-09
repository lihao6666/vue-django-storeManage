from rest_framework import serializers
from sell import models


class SellOrderSerializer(serializers.ModelSerializer):
    orga_name = serializers.CharField(source='organization.orga_name')
    area_name = serializers.CharField(source='organization.area_name')
    customer_iden = serializers.CharField(source='customer.customer_iden')
    customer_name = serializers.CharField(source='customer.customer_name')

    class Meta:
        model = models.SellOrder
        fields = (
            'id', 'so_iden', 'orga_name', 'area_name', 'so_type', 'customer_iden', 'customer_name',
            'so_date', 'deliver_ware_house', 'so_remarks', 'so_status',
            'so_creator', 'so_creator_iden', 'so_createDate'
        )


class SoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        so_iden = serializers.CharField(source='sell_order.so_iden')
        sod_iden = serializers.CharField(source='material.material_iden')
        sod_name = serializers.CharField(source='material.material_name')
        sod_specification = serializers.CharField(source='material.material_specification')
        sod_model = serializers.CharField(source='material.material_model')
        sod_meterage = serializers.CharField(source='material.meterage_name')
        model = models.SoDetail
        fields = ('id', 'so_iden', 'sod_iden', 'sod_name', 'sod_specification',
                  'sod_model', 'sod_meterage', 'sod_num', 'sod_taxRate', 'sod_tax_unitPrice', 'sod_unitPrice',
                  'sod_tax_sum', 'sod_sum', 'sod_tax_price', 'sod_remarks')
