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
            'id', 'so_iden', 'orag_name', 'orga_name', 'so_type', 'customer_iden', 'customer_name',
            'so_date', 'deliver_ware_house_iden', 'deliver_ware_house', 'so_remarks', 'so_status',
            'so_creator', 'so_creator_iden', 'so_createDate'
        )


class SoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SoDetail
        fields = ('id', 'sod_iden', 'so_iden', 'material_iden', 'material_name', 'material_specification',
                  'material_model', 'meterage_name', 'sod_num', 'sod_taxRate', 'sod_tax_unitPrice', 'sod_unitPrice',
                  'sod_tax_sum', 'sod_sum', 'sod_tax_price', 'sod_remarks')
