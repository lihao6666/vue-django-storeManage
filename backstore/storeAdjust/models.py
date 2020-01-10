from datetime import datetime

from django.db import models

# Create your models here.
from django.utils import timezone


class TransferRequest(models.Model):
    """
    转库申请单
    """
    STR_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    str_iden = models.CharField(max_length=15, verbose_name='转库申请单编号')
    str_serial = models.CharField(max_length=4, verbose_name='转库申请单流水号')
    organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='orga_str',
                                     on_delete=models.CASCADE)
    str_to_house = models.CharField(max_length=20, verbose_name='转入仓库名字')
    str_from_house = models.CharField(max_length=20, verbose_name='转出仓库名字')
    str_date = models.DateTimeField(default=datetime.now, verbose_name='转库申请日期')
    str_department = models.CharField(max_length=20, verbose_name='转库申请部门')
    str_status = models.IntegerField(choices=STR_STATUS_CHOICES, default=0, verbose_name='转库申请单状态')
    str_creator = models.CharField(max_length=20, verbose_name='转库出库单创建人名字')
    str_creator_iden = models.CharField(max_length=20, verbose_name='转库出库单创建人工号')
    str_createDate = models.DateTimeField(auto_now_add=True, verbose_name='销售出库单创建日期')

    class Meta:
        verbose_name = "转库申请单"

    def __str__(self):
        return self.str_iden


class TrDetail(models.Model):
    """
    转库申请单明细
    """
    USED_CHOICES = (
        (0, '未使用'),
        (1, '已使用')
    )
    id = models.AutoField(primary_key=True)
    transfer_request = models.ForeignKey('TransferRequest', verbose_name='转库申请单', related_name='str_trd',
                                         on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_trd',
                                 on_delete=models.CASCADE)
    trd_num = models.IntegerField(verbose_name='转库申请数量')
    trd_present_num = models.IntegerField(verbose_name='材料现存量')
    trd_used = models.IntegerField(choices=USED_CHOICES, default=0, verbose_name='是否使用过')
    trd_remarks = models.TextField(max_length=400, verbose_name='转库单明细备注')

    class Meta:
        verbose_name = "转库申请单详情"


class Transfer(models.Model):
    """
    转库单
    """
    ST_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    st_iden = models.CharField(max_length=15, verbose_name='转库单编号')
    st_serial = models.CharField(max_length=4, verbose_name='转库单流水号')
    organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='orga_st',
                                     on_delete=models.CASCADE)
    # transfer_request = models.OneToOneField('TransferRequest', verbose_name='转库申请单', on_delete=models.CASCADE)
    # str_iden = models.CharField(max_length=15, verbose_name='转库申请单编号', null=True)  # 转库申请单编号，如果为空就为新增
    st_to_house = models.CharField(max_length=20, verbose_name='转入仓库名字')
    st_from_house = models.CharField(max_length=20, verbose_name='转出仓库名字')
    st_date = models.DateTimeField(default=datetime.now, verbose_name='转库日期')
    st_status = models.IntegerField(choices=ST_STATUS_CHOICES, default=0, verbose_name='转库单状态')
    st_creator = models.CharField(max_length=20, verbose_name='转库单创建者名字')
    st_creator_iden = models.CharField(max_length=20, verbose_name='转库单创建者编号')
    st_createDate = models.DateTimeField(auto_now_add=True, verbose_name='转库单创建时间')

    class Meta:
        verbose_name = "转库单"

    def __str__(self):
        return self.st_iden


class StDetail(models.Model):
    """
    转库单明细
    """
    id = models.AutoField(primary_key=True)
    transfer = models.ForeignKey('Transfer', verbose_name='转库单', related_name='st_td', on_delete=models.CASCADE)
    str_iden = models.CharField(max_length=15, verbose_name='转库申请单编号', null=True)  # 转库申请单编号，如果为空就为新增
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_td',
                                 on_delete=models.CASCADE)
    # 转库申请数量可以通过转库单调用转库申请单再调用申请单详情实现
    td_apply_num = models.IntegerField(verbose_name='转库申请数量')
    td_real_num = models.IntegerField(verbose_name='转库实发数量')

    td_present_num = models.IntegerField(verbose_name='材料现存量')
    # 转库申请iden可以通过转库单调用转库申请实现
    td_remarks = models.TextField(max_length=400, verbose_name='转库单明细备注')

    class Meta:
        verbose_name = "转库单明细"
#
#
# class Inventory(models.Model):
#     """
#     库存盘点单
#     """
#
#     STA_STATUS_CHOICES = (
#         (0, '草稿'),
#         (1, '已审批')
#     )
#     id = models.AutoField(primary_key=True)
#     sta_iden = models.CharField(max_length=15, verbose_name='库存盘点单编号')
#     sta_serial = models.CharField(max_length=4, verbose_name='库存盘点单流水号')
#     organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='orga_sta',
#                                      on_delete=models.CASCADE)
#     sta_ware_house = models.CharField(max_length=20, verbose_name='库存盘点仓库名字')
#     sta_date = models.DateTimeField(default=datetime.now, verbose_name='库存盘点日期')
#     sta_status = models.IntegerField(choices=STA_STATUS_CHOICES, verbose_name='库存盘点状态')
#     sta_creator = models.CharField(max_length=20, verbose_name='库存盘点单创建者名字')
#     sta_creator_iden = models.CharField(max_length=20, verbose_name='库存盘点单创建者编号')
#     sta_createDate = models.DateTimeField(auto_now_add=True, verbose_name='库存盘点单创建时间')
#
#     class Meta:
#         verbose_name = "库存盘点单"
#
#     def __str__(self):
#         return self.sta_iden
#
#
# class StaDetail(models.Model):
#     """
#     库存盘点明细
#     """
#     id = models.AutoField(primary_key=True)
#     inventory = models.ForeignKey('Inventory', verbose_name='库存盘点单', related_name='sta_sd', on_delete=models.CASCADE)
#     material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_sd',
#                                  on_delete=models.CASCADE)
#     sd_paper_num = models.IntegerField(verbose_name='账面数量')
#     sd_real_num = models.IntegerField(verbose_name='盘点数量')
#     sd_diff_num = models.IntegerField(verbose_name='差异数量')
#     sd_adjm_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='调整单价')  # 读取库存组织下的单价
#     sd_adjm_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='调整金额')
#     sd_remarks = models.TextField(max_length=400, verbose_name='库存盘点明细备注')
#
#     class Meta:
#         verbose_name = "库存盘明细"

# class OpeningInventory(models.Model):
#     """
#     期初库存盘点
#     这个是某些材料写入数据库要统计的表
#     """
#     STA_STATUS_CHOICES = (
#         (0, '草稿'),
#         (1, '已审批')
#     )
#     id = models.AutoField(primary_key=True)
#     oi_iden = models.CharField(max_length=15, verbose_name='期初库存单编号')
#     organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_oi',
#                                      on_delete=models.CASCADE)
#     oi_ware_house_iden = models.CharField(max_length=6, verbose_name='期初库存盘点仓库编码')
#     oi_date = models.DateTimeField(auto_now_add=True, verbose_name='期初库存盘点日期')
#     oi_status = models.IntegerField(choices=STA_STATUS_CHOICES, verbose_name='期初库存盘点状态')
#     oi_creator = models.CharField(max_length=20, verbose_name='期初库存盘点单创建者')
#     oi_createDate = models.DateTimeField(auto_now_add=True, verbose_name='期初库存盘点单创建时间')
#
#     class Meta:
#         verbose_name = "期初库存盘点单"
#
#     def __str__(self):
#         return self.oi_iden
#
#
# class OiDetail(models.Model):
#     """
#     期初库存盘点明细
#     """
#
#     id = models.AutoField(primary_key=True)
#     opening_inventory = models.ForeignKey('OpeningInventory', verbose_name='期初库存盘点', related_name='oi_oid',
#                                           on_delete=models.CASCADE)
#     material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_oid',
#                                  on_delete=models.CASCADE)
#     oid_num = models.IntegerField(verbose_name='入库数量')
#     oid_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='入库单价')
#     oid_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='入库总价')
#     oid_date = models.DateTimeField(auto_now_add=True, verbose_name='入库时间')
#     oid_remarks = models.TextField(max_length=400, verbose_name='期初库存盘点明细备注')
#
#     class Meta:
#         verbose_name = "期初库存盘点明细"
