from django.db import models


# Create your models here.

class TotalStock(models.Model):
    """
    总仓存储信息
    """
    totalwarehouse = models.ForeignKey('base.TotalWareHouse', verbose_name='总仓', related_name='total_ware_house_ts',
                                       on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_ts',
                                 on_delete=models.CASCADE)
    ts_present_num = models.IntegerField(verbose_name='物料现存量')


class CenterStock(models.Model):
    """
    中心仓库存储信息
    """
    centerwarehouse = models.ForeignKey('base.CenterWareHouse', verbose_name='中心仓库',
                                        related_name='center_ware_house_cs', on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_cs',
                                 on_delete=models.CASCADE)
    cs_present_num = models.IntegerField(verbose_name='物料现存量')

