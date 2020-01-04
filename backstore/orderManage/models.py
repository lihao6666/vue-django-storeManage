from django.db import models


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
    organization = models.ForeignKey('base.Organization', related_name='orga_pr', verbose_name='组织',
                                     on_delete=models.CASCADE)
    pr_need_type = models.CharField(max_length=20, verbose_name='需求类型')
    # material_type = models.ForeignKey('base.MaterialType', verbose_name='物料类别', on_delete=models.CASCADE)
    pr_department = models.CharField(max_length=20, verbose_name='请购部门')
    pr_date = models.DateTimeField(auto_now_add=True, verbose_name='请购日期')
    pr_remarks = models.TextField(max_length=400, verbose_name='请购备注')
    pr_status = models.IntegerField(choices=REQ_PUR_STATUS_CHOICES, verbose_name='请购状态')
    pr_creator = models.CharField(max_length=20, verbose_name='请购创建者')
    pr_createDate = models.DateTimeField(auto_now_add=True, verbose_name='请购创建时间')
    pr_closer = models.CharField(max_length=20, verbose_name='请购关闭者')
    pr_closeDate = models.DateTimeField(auto_now_add=True, verbose_name='请购关闭时间')
    pr_closeReason = models.TextField(max_length=200, verbose_name='请购关闭原因')

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
    purchase_request = models.ForeignKey('PurchaseRequest', related_name='pr_prd', verbose_name='请购单',
                                         on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_prd',
                                 on_delete=models.CASCADE)  # attention
    prd_num = models.IntegerField(verbose_name='请购数量')
    prd_remarks = models.TextField(max_length=400, verbose_name='物料请购备注')
    prd_used = models.IntegerField(choices=PRD_USE_STATUS_CHOICES, verbose_name='明细单是否使用')

    class Meta:
        verbose_name = "请购单物料明细"


class PurchaseContract(models.Model):
    """
    采购合同
    """

    PC_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )

    id = models.AutoField(primary_key=True)
    pc_iden = models.CharField(max_length=15, verbose_name='合同编号')
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_pc',
                                     on_delete=models.CASCADE)
    pc_name = models.CharField(max_length=20, verbose_name='合同名称')
    supplier = models.ForeignKey('base.Supplier', verbose_name='供应商', related_name='supplier_pc',
                                 on_delete=models.CASCADE)
    pc_date = models.DateTimeField(auto_now_add=True, verbose_name='合同签订日期')
    pc_sum = models.IntegerField(verbose_name='合同总额')
    pc_remarks = models.TextField(max_length=400, verbose_name='合同备注')
    pc_status = models.IntegerField(choices=PC_STATUS_CHOICES, verbose_name='合同状态')
    pc_creator = models.CharField(max_length=20, verbose_name='合同创建者')
    pc_createDate = models.DateTimeField(auto_now_add=True, verbose_name='合同创建时间')

    class Meta:
        verbose_name = "采购合同"

    def __str__(self):
        return self.pc_name


class CdDetail(models.Model):
    """
    合同物料明细
    """
    CD_USE_STATUS_CHOICES = (
        (0, '未使用'),
        (1, '已使用')
    )
    id = models.AutoField(primary_key=True)
    purchase_contract = models.ForeignKey('PurchaseContract', verbose_name='采购合同', related_name='pc_cd',
                                          on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_cd',
                                 on_delete=models.CASCADE)

    cd_num = models.IntegerField(verbose_name='物料数量')
    cd_taxRate = models.IntegerField(default=13, verbose_name='税率')
    cd_tax_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税单价')
    cd_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价')
    cd_tax_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税总额')
    cd_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额')
    cd_rp_iden = models.CharField(max_length=15, verbose_name='请购单编号')
    cd_rpd_remarks = models.TextField(max_length=400, verbose_name='物料备注')
    cd_used = models.IntegerField(choices=CD_USE_STATUS_CHOICES, verbose_name='明细单是否使用')

    class Meta:
        verbose_name = "合同物料明细"

    def __str__(self):
        return self.cd_num


class CdPayDetail(models.Model):
    """
    合同付款协议
    """
    PAY_PREAY_CHOICES = (
        (0, '是'),
        (1, '否')
    )
    id = models.AutoField(primary_key=True)
    purchase_contract = models.ForeignKey('PurchaseContract', verbose_name='采购合同', related_name='pc_pay',
                                          on_delete=models.CASCADE)
    pay_batch = models.IntegerField(verbose_name='付款批次')
    pay_rate = models.IntegerField(verbose_name='付款比率')
    pay_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='付款金额')
    pay_planDate = models.DateField(verbose_name='计划付款日期')
    pay_preay = models.IntegerField(choices=PAY_PREAY_CHOICES, verbose_name='是否预付款')
    pay_remarks = models.TextField(max_length=400, verbose_name='付款备注')

    class Meta:
        verbose_name = "合同付款协议"

    def __str__(self):
        return self.pay_batch


class PurchaseOrder(models.Model):
    """
    采购订单
    """
    PO_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    po_iden = models.CharField(max_length=15, verbose_name='采购订单编号')
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_po',
                                     on_delete=models.CASCADE)
    supplier = models.ForeignKey('base.Supplier', verbose_name='供应商', related_name='supplier_po',
                                 on_delete=models.CASCADE)
    po_date = models.DateTimeField(auto_now_add=True, verbose_name='采购订单生效日期')
    po_sum = models.IntegerField(verbose_name='采购订单总额')
    po_remarks = models.TextField(max_length=400, verbose_name='采购订单备注')
    purchase_contract = models.ForeignKey('PurchaseContract', verbose_name='采购合同', related_name='pc_po',
                                          on_delete=models.CASCADE)
    purchase_request = models.ForeignKey('PurchaseRequest', verbose_name='请购单', related_name='pr_po',
                                         on_delete=models.Model)
    po_status = models.IntegerField(choices=PO_STATUS_CHOICES, verbose_name='采购订单状态')
    po_creator = models.CharField(max_length=20, verbose_name='采购订单创建者')
    po_createDate = models.DateTimeField(auto_now_add=True, verbose_name='采购订单创建时间')

    class Meta:
        verbose_name = "采购订单"

    def __str__(self):
        return self.po_iden


class OrDetail(models.Model):
    """
    采购订单明细
    """
    id = models.AutoField(primary_key=True)
    purchase_contract = models.ForeignKey('PurchaseContract', verbose_name='采购合同', related_name='pc_od',
                                          on_delete=models.CASCADE)
    pr_detail = models.ForeignKey('PrDetail', verbose_name='请购单物料明细', related_name='pr_od',
                                  on_delete=models.CASCADE)
    cd_detail = models.ForeignKey('CdDetail', verbose_name='合同物料明细', related_name='cd_od', on_delete=models.CASCADE)

    od_num = models.IntegerField(verbose_name='采购数量')
    od_taxRate = models.IntegerField(default=13, verbose_name='税率')
    od_tax_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税单价')
    od_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价')
    od_tax_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税总额')
    od_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额')
    od_rp_iden = models.CharField(max_length=15, verbose_name='请购单编号')
    od_rpd_remarks = models.TextField(max_length=400, verbose_name='物料备注')

    class Meta:
        verbose_name = "采购订单详情"


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
    organization = models.ForeignKey('base.Organization', verbose_name='组织', related_name='orga_so',
                                     on_delete=models.CASCADE)
    so_type = models.IntegerField(choices=SELL_ORDER_CHOICES, verbose_name='订单类型')
    customer = models.ForeignKey('base.Customer', verbose_name='客户', related_name='customer_so',
                                 on_delete=models.CASCADE)
    so_date = models.DateField(auto_now_add=True, verbose_name='订单日期')
    deliver_ware_house_iden = models.CharField(max_length=6, verbose_name='发货仓库编码')  # 这里需要传入总仓或者中心仓库的编码
    so_remarks = models.TextField(max_length=400, verbose_name='订单备注')
    so_status = models.IntegerField(choices=SO_STATUS_CHOICES, verbose_name='销售订单状态')
    so_creator = models.CharField(max_length=20, verbose_name='订单创建人')
    so_createDate = models.DateTimeField(auto_now_add=True, verbose_name='订单创建日期')


class SoDetail(models.Model):
    """
    销售订单明细
    """
    id = models.AutoField(primary_key=True)
    sell_order = models.ForeignKey('SellOrder', verbose_name='销售订单', related_name='so_sod', on_delete=models.Model)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_sod',
                                 on_delete=models.CASCADE)
    sod_num = models.IntegerField(verbose_name='销售数量')
    sod_taxRate = models.IntegerField(default=13, verbose_name='税率')
    sod_tax_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税单价')
    sod_unitPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价')
    sod_tax_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='含税总额')
    sod_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额')
    sod_tax_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='税金总额')
    sod_remarks = models.TextField(max_length=200, verbose_name='订单明细备注')

    class Meta:
        verbose_name = "销售订单明细"


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
    origanization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_bis',
                                      on_delete=models.CASCADE)
    totalwarehouse = models.ForeignKey('base.TotalWareHouse', verbose_name='总仓', related_name='total_ware_house_bis',
                                       on_delete=models.CASCADE)
    supplier = models.ForeignKey('base.Supplier', verbose_name='供应商', related_name='supplier_bis',
                                 on_delete=models.CASCADE)
    bis_date = models.DateField(auto_now_add=True, verbose_name='采购入库日期')
    bis_remarks = models.TextField(max_length=400, verbose_name='采购入库单备注')
    bis_status = models.IntegerField(choices=BIS_STATUS_CHOICES, verbose_name='采购入库单状态')
    bis_creator = models.CharField(max_length=20, verbose_name='采购入库单创建人')
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
    buy_in_store = models.ForeignKey('MaterialSo', verbose_name='材料出库单', related_name='mso_bd',
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


class OtherSi(models.Model):
    """
    其它入库单
    """
    OSI_TYPE_CHOICES = (
        (0, '转库入库'),
        (1, '盘盈出库'),
    )
    OSI_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    osi_iden = models.CharField(max_length=15, verbose_name='其它入库单编号')
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_osi',
                                     on_delete=models.CASCADE)
    transfer = models.OneToOneField('Transfer', verbose_name='转库单', on_delete=models.CASCADE)  # 如果不行保存为转库单iden
    inventory = models.OneToOneField('Inventory', verbose_name='库存盘点单', on_delete=models.CASCADE)  # 同上
    osi_house = models.CharField(max_length=15, verbose_name='其它入库仓库编号')

    osi_type = models.IntegerField(choices=OSI_TYPE_CHOICES, verbose_name='其它入库单类型')
    osi_date = models.DateField(auto_now_add=True, verbose_name='其它出库日期')
    osi_remarks = models.TextField(max_length=400, verbose_name='其它出库单备注')

    osi_status = models.IntegerField(choices=OSI_STATUS_CHOICES, verbose_name='其它出库单状态')
    osi_creator = models.CharField(max_length=20, verbose_name='其它出库单创建人')
    osi_createDate = models.DateTimeField(auto_now_add=True, verbose_name='其它出库单创建日期')

    class Meta:
        verbose_name = "其它出库单"

    def __str__(self):
        return self.osi_iden


class OsiDetail(models.Model):
    """
    其它入库单明细
    """
    id = models.AutoField(primary_key=True)
    other_si = models.ForeignKey('OtherSi', verbose_name='其它入库单', related_name='osi_osid', on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_osid',
                                 on_delete=models.CASCADE)
    osid_paper_num = models.IntegerField(verbose_name='应收数量')
    osid_real_num = models.IntegerField(verbose_name='实收数量')
    osid_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税单价')
    osid_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='无税总额')


class MaterialSo(models.Model):
    """
    材料出库单
    """
    MSO_TYPE_CHOICES = (
        (0, '内部出库'),
        (1, '外部出库'),
    )
    MSO_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    mso_iden = models.CharField(max_length=15, verbose_name='出库单编号')
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_mso',
                                     on_delete=models.CASCADE)
    mso_type = models.IntegerField(choices=MSO_TYPE_CHOICES, verbose_name='材料出库类型')
    # customer = models.ForeignKey('base.Customer', verbose_name='客户', related_name='customer_so',
    #                              on_delete=models.CASCADE)
    deliver_ware_house_iden = models.CharField(max_length=6, verbose_name='出库仓库编码')  # 这里需要传入总仓或者中心仓库的编码
    mso_req_department = models.ForeignKey('base.Department', verbose_name='申请部门', on_delete=models.CASCADE)
    mso_date = models.DateField(auto_now_add=True, verbose_name='材料出库日期')
    mso_remarks = models.TextField(max_length=400, verbose_name='材料出库备注')
    mso_status = models.IntegerField(choices=MSO_STATUS_CHOICES, verbose_name='材料出库单状态')
    mso_creator = models.CharField(max_length=20, verbose_name='材料出库单创建人')
    mso_createDate = models.DateTimeField(auto_now_add=True, verbose_name='材料出库单创建日期')

    class Meta:
        verbose_name = "材料出库单"

    def __str__(self):
        return self.mso_iden


class MsoDetail(models.Model):
    """
    材料出库单明细
    """
    id = models.AutoField(primary_key=True)
    material_so = models.ForeignKey('MaterialSo', verbose_name='材料出库单', related_name='mso_msod',
                                    on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_msod',
                                 on_delete=models.CASCADE)
    msod_num = models.IntegerField(verbose_name='材料出库数量')
    msod_present_num = models.IntegerField(verbose_name='材料现存量')
    msod_remarks = models.TextField(max_length=200, verbose_name='材料出库单明细备注')

    class Meta:
        verbose_name = "材料出库单明细"


class SellSo(models.Model):
    """
    销售出库
    """
    # 如果要查销售出库详情可以直接通过销售订单详情查询

    SSO_TYPE_CHOICES = (
        (0, '普通发票'),
        (1, '退换货')
    )
    SSO_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    sso_iden = models.CharField(max_length=15, verbose_name='销售出库单编号')
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_sso',
                                     on_delete=models.CASCADE)
    sell_order = models.OneToOneField('SellOrder', verbose_name='销售订单', on_delete=models.CASCADE)
    sso_status = models.IntegerField(choices=SSO_STATUS_CHOICES, verbose_name='销售出库单状态')
    sso_creator = models.CharField(max_length=20, verbose_name='销售出库单创建人')
    sso_createDate = models.DateTimeField(auto_now_add=True, verbose_name='销售出库单创建日期')

    class Meta:
        verbose_name = "销售出库单明细"

    def __str__(self):
        return self.sso_iden


class OtherSo(models.Model):
    """
    其它出库单
    """
    # 自动生成的单子

    OSO_TYPE_CHOICES = (
        (0, '转库出库'),
        (1, '盘亏出库'),
    )
    OSO_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    oso_iden = models.CharField(max_length=15, verbose_name='其它出库单编号')
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_oso',
                                     on_delete=models.CASCADE)
    transfer = models.OneToOneField('Transfer', verbose_name='转库单', on_delete=models.CASCADE)
    inventory = models.OneToOneField('Inventory', verbose_name='库存盘点单', on_delete=models.CASCADE)

    oso_type = models.IntegerField(choices=OSO_TYPE_CHOICES, verbose_name='其它出库单类型')
    oso_date = models.DateField(auto_now_add=True, verbose_name='其它出库日期')
    oso_remarks = models.TextField(max_length=400, verbose_name='其它出库单备注')
    oso_form_iden = models.CharField(max_length=15, verbose_name='来源单号')
    oso_status = models.IntegerField(choices=OSO_STATUS_CHOICES, verbose_name='其它出库单状态')
    oso_creator = models.CharField(max_length=20, verbose_name='其它出库单创建人')
    oso_createDate = models.DateTimeField(auto_now_add=True, verbose_name='其它出库单创建日期')

    class Meta:
        verbose_name = "其它出库单"

    def __str__(self):
        return self.oso_iden


class OsoDetail(models.Model):
    """
    其它出库单明细
    """
    id = models.AutoField(primary_key=True)
    other_so = models.ForeignKey('OtherSo', verbose_name='其它出库单', related_name='oso_osod', on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_osod',
                                 on_delete=models.CASCADE)
    osod_num = models.IntegerField(verbose_name='其它出库物料数量')
    osod_remarks = models.TextField(max_length=400, verbose_name='其它出库物料明细')

    class Meta:
        verbose_name = "其它出库单明细"


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
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_str',
                                     on_delete=models.CASCADE)
    str_to_house = models.CharField(max_length=6, verbose_name='转入仓库编码')
    str_from_house = models.CharField(max_length=6, verbose_name='转出仓库编码')
    str_date = models.DateField(auto_now_add=True, verbose_name='转库申请日期')
    str_status = models.IntegerField(choices=STR_STATUS_CHOICES, verbose_name='转库申请单状态')
    str_creator = models.CharField(max_length=20, verbose_name='销售出库单创建人')
    str_createDate = models.DateTimeField(auto_now_add=True, verbose_name='销售出库单创建日期')

    class Meta:
        verbose_name = "转库申请单"

    def __str__(self):
        return self.str_iden


class TrDetail(models.Model):
    """
    转库申请单明细
    """
    id = models.AutoField(primary_key=True)
    transfer_request = models.ForeignKey('TransferRequest', verbose_name='转库申请单', related_name='str_trd',
                                         on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_trd',
                                 on_delete=models.CASCADE)
    trd_num = models.IntegerField(verbose_name='转库申请数量')
    trd_present_num = models.IntegerField(verbose_name='材料现存量')
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
    transfer_request = models.OneToOneField('TransferRequest', verbose_name='转库申请单', on_delete=models.CASCADE)
    st_date = models.DateField(auto_now_add=True, verbose_name='转库日期')
    st_status = models.IntegerField(choices=ST_STATUS_CHOICES, verbose_name='转库单状态')
    st_creator = models.CharField(max_length=20, verbose_name='转库单创建者')
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
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_td',
                                 on_delete=models.CASCADE)
    # 转库申请数量可以通过转库单调用转库申请单再调用申请单详情实现
    td_real_num = models.IntegerField(verbose_name='转库实发数量')

    td_present_num = models.IntegerField(verbose_name='材料现存量')
    # 转库申请iden可以通过转库单调用转库申请实现
    td_remarks = models.TextField(max_length=400, verbose_name='转库单明细备注')

    class Meta:
        verbose_name = "转库单明细"


class Inventory(models.Model):
    """
    库存盘点单
    """

    STA_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    sta_iden = models.CharField(max_length=15, verbose_name='库存盘点单编号')
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_sta',
                                     on_delete=models.CASCADE)
    sta_ware_house_iden = models.CharField(max_length=6, verbose_name='库存盘点仓库编码')
    sta_date = models.DateTimeField(auto_now_add=True, verbose_name='库存盘点日期')
    sta_status = models.IntegerField(choices=STA_STATUS_CHOICES, verbose_name='库存盘点状态')
    sta_creator = models.CharField(max_length=20, verbose_name='库存盘点单创建者')
    sta_createDate = models.DateTimeField(auto_now_add=True, verbose_name='库存盘点单创建时间')

    class Meta:
        verbose_name = "库存盘点单"

    def __str__(self):
        return self.sta_iden


class StaDetail(models.Model):
    """
    库存盘点明细
    """
    id = models.AutoField(primary_key=True)
    inventory = models.ForeignKey('Inventory', verbose_name='库存盘点单', related_name='sta_sd', on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_sd',
                                 on_delete=models.CASCADE)
    sd_paper_num = models.IntegerField(verbose_name='账面数量')
    sd_real_num = models.IntegerField(verbose_name='盘点数量')
    sd_diff_num = models.IntegerField(verbose_name='差异数量')
    sd_adjm_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='调整单价')  # 读取库存组织下的单价
    sd_adjm_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='调整金额')
    sd_remarks = models.TextField(max_length=400, verbose_name='库存盘点明细备注')

    class Meta:
        verbose_name = "库存盘明细"


class OpeningInventory(models.Model):
    """
    期初库存盘点
    这个是某些材料写入数据库要统计的表
    """
    STA_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已审批')
    )
    id = models.AutoField(primary_key=True)
    oi_iden = models.CharField(max_length=15, verbose_name='期初库存单编号')
    organization = models.ForeignKey('base.Origanization', verbose_name='组织', related_name='orga_oi',
                                     on_delete=models.CASCADE)
    oi_ware_house_iden = models.CharField(max_length=6, verbose_name='期初库存盘点仓库编码')
    oi_date = models.DateTimeField(auto_now_add=True, verbose_name='期初库存盘点日期')
    oi_status = models.IntegerField(choices=STA_STATUS_CHOICES, verbose_name='期初库存盘点状态')
    oi_creator = models.CharField(max_length=20, verbose_name='期初库存盘点单创建者')
    oi_createDate = models.DateTimeField(auto_now_add=True, verbose_name='期初库存盘点单创建时间')

    class Meta:
        verbose_name = "期初库存盘点单"

    def __str__(self):
        return self.oi_iden


class OiDetail(models.Model):
    """
    期初库存盘点明细
    """

    id = models.AutoField(primary_key=True)
    opening_inventory = models.ForeignKey('OpeningInventory', verbose_name='期初库存盘点', related_name='oi_oid',
                                          on_delete=models.CASCADE)
    material = models.ForeignKey('base.Material', verbose_name='物料', related_name='material_oid',
                                 on_delete=models.CASCADE)
    oid_num = models.IntegerField(verbose_name='入库数量')
    oid_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='入库单价')
    oid_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='入库总价')
    oid_date = models.DateTimeField(auto_now_add=True, verbose_name='入库时间')
    oid_remarks = models.TextField(max_length=400, verbose_name='期初库存盘点明细备注')

    class Meta:
        verbose_name = "期初库存盘点明细"
