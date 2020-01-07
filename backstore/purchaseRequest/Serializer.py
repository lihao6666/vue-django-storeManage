from rest_framework import serializers
from purchaseRequest import models


class PurchaseRequestSerializer(serializers.ModelSerializer):
    orga_name = serializers.CharField(source='organization.orga_name')
    area_name = serializers.CharField(source='organization.area_name')

    class Meta:
        model = models.PurchaseRequest
        fields = ('id', 'pr_iden', 'orga_name', 'area_name', 'pr_type', 'pr_department',
                  'pr_date', 'pr_remarks', 'pr_status', 'pr_creator','pr_creator_iden', 'pr_createDate', 'pr_closer', 'pr_closeDate',
                  'pr_closeReason')


class PrDetailSerializer(serializers.ModelSerializer):
    pr_iden = serializers.CharField(source='purchase_request.pr_iden')
    prd_iden = serializers.CharField(source='material.material_iden')
    prd_name = serializers.CharField(source='material.material_name')
    prd_specification = serializers.CharField(source='material.material_specification')
    prd_model = serializers.CharField(source='material.material_model')
    prd_meterage = serializers.CharField(source='material.meterage_name')

    class Meta:
        model = models.PrDetail
        fields = ('id', 'prd_iden', 'pr_iden', 'prd_name', 'prd_specification', 'prd_model', 'prd_meterage',
                  'prd_num', 'prd_present_num', 'prd_remarks', 'prd_used')
