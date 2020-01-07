from django.db import models


# Create your models here.

class TotalStock(models.Model):
    """
    仓库存储信息
    """

    id = models.AutoField(primary_key=True)
    totalwarehouse = models.ForeignKey('base.TotalWareHouse', verbose_name='仓库', related_name='total_ware_house_ts',
                                       on_delete=models.CASCADE)

    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_ts',
                                 on_delete=models.CASCADE)
    ts_present_num = models.IntegerField(verbose_name='物料现存量')
    ts_present_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='库存单价')
    ts_present_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='库存总额')

    class Meta:
        verbose_name = "仓库"
