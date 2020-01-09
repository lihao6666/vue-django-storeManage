from django.db import models
import django.utils.timezone as timezone
from datetime import datetime

# Create your models here.

class PurchaseRequest(models.Model):
    """
    请购单
    """

    REQ_PUR_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批'),
        (2, '已关闭')
    )
    id = models.AutoField(primary_key=True)
    pr_iden = models.CharField(max_length=15, verbose_name='请购单编号')
    pr_serial = models.CharField(max_length=4, verbose_name='请购单流水')
    organization = models.ForeignKey('base.Organization', related_name='orga_pr', verbose_name='组织',
                                     on_delete=models.CASCADE)
    pr_type = models.CharField(max_length=20, verbose_name='需求类型')
    # material_type = models.ForeignKey('base.MaterialType', verbose_name='物料类别', on_delete=models.CASCADE)
    pr_department = models.CharField(max_length=20, verbose_name='请购部门')
    pr_date = models.DateTimeField(default=datetime.now, verbose_name='请购日期')
    pr_remarks = models.TextField(max_length=400, verbose_name='请购备注', null=True)
    pr_status = models.IntegerField(choices=REQ_PUR_STATUS_CHOICES, verbose_name='请购状态')
    pr_creator = models.CharField(max_length=20, verbose_name='请购创建名字')
    pr_creator_iden = models.CharField(max_length=20, verbose_name="请购单创建者工号")
    pr_createDate = models.DateTimeField(auto_now_add=True, verbose_name='请购创建时间')
    pr_closer = models.CharField(max_length=20, verbose_name='请购关闭者', null=True)
    pr_closer_iden = models.CharField(max_length=20, verbose_name='请购关闭者工号', null=True)
    pr_closeDate = models.DateTimeField(auto_now_add=True, verbose_name='请购关闭时间', null=True)
    pr_closeReason = models.TextField(max_length=200, verbose_name='请购关闭原因', null=True)

    class Meta:
        verbose_name = "请购单"

    def __str__(self):
        return self.pr_iden


class PrDetail(models.Model):
    """
    请购单物料明细
    """
    # 这里还没完善，需要建立与物料库存的关系
    PRD_USE_STATUS_CHOICES = (
        (0, '未使用'),
        (1, '已使用')
    )
    id = models.AutoField(primary_key=True)
    # pr_iden = models.CharField(max_length=15,verbose_name="请购单编号")
    purchase_request = models.ForeignKey('PurchaseRequest', related_name='pr_prd', verbose_name='请购单',
                                         on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_prd',
                                 on_delete=models.CASCADE)  # attention
    prd_num = models.IntegerField(verbose_name='请购数量')
    prd_present_num = models.IntegerField(verbose_name='现存量')
    prd_remarks = models.TextField(max_length=400, verbose_name='物料请购备注', null=True)
    prd_used = models.IntegerField(choices=PRD_USE_STATUS_CHOICES, verbose_name='明细单是否使用')

    class Meta:
        verbose_name = "请购单物料明细"
