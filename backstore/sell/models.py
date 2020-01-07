from django.db import models


# Create your models here.

class SellOrder(models.Model):
    """
    销售订单
    """
    SELL_ORDER_CHOICES = (
        (0, '普通发票'),
        (1, '退换货')
    )
    SO_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    so_iden = models.CharField(max_length=15, verbose_name='销售订单编号')
    so_serial = models.CharField(max_length=4, verbose_name='流水号')
    organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='orga_so',
                                     on_delete=models.CASCADE)
    so_type = models.IntegerField(choices=SELL_ORDER_CHOICES, verbose_name='订单类型')
    customer = models.ForeignKey('base.Customer', verbose_name='客户', related_name='customer_so',
                                 on_delete=models.CASCADE)
    so_date = models.DateField(auto_now_add=True, verbose_name='订单日期')
    deliver_ware_house = models.CharField(max_length=20, verbose_name='发货仓库名字')
    deliver_ware_house_iden = models.CharField(max_length=6, verbose_name='发货仓库编码')
    so_remarks = models.TextField(max_length=400, verbose_name='订单备注')
    so_status = models.IntegerField(choices=SO_STATUS_CHOICES, verbose_name='销售订单状态')
    so_creator = models.CharField(max_length=20, verbose_name='订单创建人名字')
    so_creator_iden = models.CharField(max_length=20, verbose_name='订单创建人编码')
    so_createDate = models.DateTimeField(auto_now_add=True, verbose_name='订单创建日期')

    class Meta:
        verbose_name = "销售订单"


class SoDetail(models.Model):
    """
    销售订单明细
    """
    id = models.AutoField(primary_key=True)
    sell_order = models.ForeignKey('SellOrder', verbose_name='销售订单', related_name='so_sod', on_delete=models.Model)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_sod',
                                 on_delete=models.CASCADE)
    sod_num = models.IntegerField(verbose_name='销售数量')
    sod_taxRate = models.IntegerField(default=13, verbose_name='税率',null=True)
    sod_tax_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税单价',null=True)
    sod_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价',null=True)
    sod_tax_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税总额',null=True)
    sod_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额',null=True)
    sod_tax_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='税金总额',null=True)
    sod_remarks = models.TextField(max_length=200, verbose_name='订单明细备注',null=True)

    class Meta:
        verbose_name = "销售订单明细"
