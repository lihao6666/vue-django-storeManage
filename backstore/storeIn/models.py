from django.db import models
import django.utils.timezone as timezone


# Create your models here.

class BuyInStore(models.Model):
    """
    采购入库单
    """
    BIS_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    bis_iden = models.CharField(max_length=15, verbose_name='入库单编号')
    bis_serial = models.CharField(max_length=4, verbose_name='入库单流水号')
    organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='orga_bis',
                                     on_delete=models.CASCADE)
    totalwarehouse = models.ForeignKey('base.TotalWareHouse', verbose_name='总仓', related_name='total_ware_house_bis',
                                       on_delete=models.CASCADE)
    supplier = models.ForeignKey('base.Supplier', verbose_name='供应商', related_name='supplier_bis',
                                 on_delete=models.CASCADE)
    bis_date = models.DateTimeField(default=timezone.now, verbose_name='采购入库日期')
    bis_remarks = models.TextField(max_length=400, verbose_name='采购入库单备注')
    bis_status = models.IntegerField(choices=BIS_STATUS_CHOICES, default=0, verbose_name='采购入库单状态')
    bis_creator = models.CharField(max_length=20, verbose_name='采购入库单创建人名字')
    bis_creator_iden = models.CharField(max_length=20, verbose_name='采购入库单创建人工号')
    bis_createDate = models.DateTimeField(auto_now_add=True, verbose_name='采购入库单创建日期')

    class Meta:
        verbose_name = "材料出库单"

    def __str__(self):
        return self.bis_iden


class BisDetail(models.Model):
    """
    采购入库单明细
    """
    id = models.AutoField(primary_key=True)
    buy_in_store = models.ForeignKey('BuyInStore', verbose_name='采购入库单', related_name='bis_bd',
                                     on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_bd',
                                 on_delete=models.CASCADE)
    bd_paper_num = models.IntegerField(verbose_name='应入库数量')
    bd_real_num = models.IntegerField(verbose_name='实际入库数量')
    bd_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价')
    bd_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额')
    po_iden = models.CharField(max_length=15, verbose_name='采购订单号')
    pr_iden = models.CharField(max_length=15, verbose_name='请购订单号')

    # bd_remarks = models.TextField(max_length=200, verbose_name='采购入库单明细备注')

    class Meta:
        verbose_name = "采购入库单明细"


# class OtherSi(models.Model):
#     """
#     其它入库单
#     """
#     OSI_TYPE_CHOICES = (
#         (0, '转库入库'),
#         (1, '盘盈出库'),
#     )
#     OSI_STATUS_CHOICES = (
#         (0, '草稿'),
#         (1, '已审批')
#     )
#     id = models.AutoField(primary_key=True)
#     osi_iden = models.CharField(max_length=15, verbose_name='其它入库单编号')
#     osi_serial = models.CharField(max_length=4, verbose_name='其它入库单流水号')
#     organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='orga_osi',
#                                      on_delete=models.CASCADE)
#     transfer = models.OneToOneField('Transfer', verbose_name='转库单', on_delete=models.CASCADE)  # 如果不行保存为转库单iden
#     inventory = models.OneToOneField('Inventory', verbose_name='库存盘点单', on_delete=models.CASCADE)  # 同上
#     osi_ware_house = models.CharField(max_length=15, verbose_name='其它入库仓库名字')
#
#     osi_type = models.IntegerField(choices=OSI_TYPE_CHOICES, verbose_name='其它入库单类型')
#     osi_date = models.DateField(auto_now_add=True, verbose_name='其它出库日期')
#     osi_remarks = models.TextField(max_length=400, verbose_name='其它出库单备注')
#
#     osi_status = models.IntegerField(choices=OSI_STATUS_CHOICES, default=0, verbose_name='其它出库单状态')
#     osi_creator = models.CharField(max_length=20, verbose_name='其它出库单创建人')
#
#     osi_createDate = models.DateTimeField(auto_now_add=True, verbose_name='其它出库单创建日期')
#
#     class Meta:
#         verbose_name = "其它出库单"
#
#     def __str__(self):
#         return self.osi_iden
#
#
# class OsiDetail(models.Model):
#     """
#     其它入库单明细
#     """
#     id = models.AutoField(primary_key=True)
#     other_si = models.ForeignKey('OtherSi', verbose_name='其它入库单', related_name='osi_osid', on_delete=models.CASCADE)
#     material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_osid',
#                                  on_delete=models.CASCADE)
#     osid_paper_num = models.IntegerField(verbose_name='应收数量')
#     osid_real_num = models.IntegerField(verbose_name='实收数量')
#     osid_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价')
#     osid_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额')
