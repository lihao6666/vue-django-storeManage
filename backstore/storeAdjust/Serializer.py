from rest_framework import serializers
from storeAdjust import models


class TrSerializer(serializers.ModelSerializer):
    orga_name = serializers.CharField(source='organization.orga_name')

    class Meta:
        model = models.TransferRequest
        fields = (
            'id', 'str_iden', 'orga_name', 'str_to_house', 'str_from_house', 'str_date', 'str_department', 'str_status',
            'str_creator', 'str_creator_iden', 'str_createDate')


class TrDSerializer(serializers.ModelSerializer):
    str_iden = serializers.CharField(source='transfer_request.str_iden')
    trd_iden = serializers.CharField(source='material.material_iden')
    trd_name = serializers.CharField(source='material.material_name')
    trd_specification = serializers.CharField(source='material.material_specification')
    trd_model = serializers.CharField(source='material.material_model')
    trd_meterage = serializers.CharField(source='material.meterage_name')

    class Meta:
        model = models.TrDetail
        fields = ('id', 'str_iden', 'trd_iden', 'trd_name', 'trd_specification', 'trd_model', 'trd_meterage',
                  'trd_num', 'trd_present_num', 'trd_used', 'trd_remarks')


class TransferSerializer(serializers.ModelSerializer):
    orga_name = serializers.CharField(source='organization.orga_name')

    class Meta:
        model = models.Transfer
        fields = ('id', 'st_iden', 'orga_name', 'st_to_house', 'st_from_house', 'st_date', 'st_status', 'st_creator',
                  'st_creator_iden', 'st_createDate')


class StDSerializer(serializers.ModelSerializer):
    st_iden = serializers.CharField(source='transfer.st_iden')
    td_iden = serializers.CharField(source='material.material_iden')
    td_name = serializers.CharField(source='material.material_name')
    td_specification = serializers.CharField(source='material.material_specification')
    td_model = serializers.CharField(source='material.material_model')
    td_meterage = serializers.CharField(source='material.meterage_name')

    class Meta:
        model = models.StDetail
        fields = ('id', 'str_iden', 'st_iden', 'td_iden', 'td_name', 'td_specification', 'td_model', 'td_meterage',
                  'td_apply_num', 'td_real_num ', 'td_present_num', 'td_remarks')
