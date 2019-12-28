from django.db import models


# Create your models here.


class UserProfile(models.Model):
    """
    定义艺朝艺夕员工
    """
    USER_STATUS_CHOICES = (
        (0, '停用'),
        (1, '启用')
    )
    user_id = models.CharField(max_length=20, verbose_name='工号', primary_key=True)
    user_passwd = models.CharField(max_length=20, default=user_id, verbose_name='用户密码')
    user_name = models.CharField(max_length=20, verbose_name='姓名')
    user_phone_number = models.CharField(max_length=20, verbose_name='手机号', null=True)
    user_mailbox = models.CharField(max_length=30, verbose_name='邮箱', null=True)
    area = models.ForeignKey('Area', verbose_name='区域', related_name='area_user', on_delete=models.CASCADE)
    user_departments = models.CharField(max_length=50, verbose_name='部门')
    user_roles = models.CharField(max_length=50, verbose_name='角色')
    user_status = models.IntegerField(choices=USER_STATUS_CHOICES, verbose_name='员工状态')
    user_creator = models.CharField(max_length=20, verbose_name='员工创建人')
    user_createDate = models.DateTimeField(auto_now_add=True, verbose_name='员工创建时间')

    class Meta:
        verbose_name = "员工"

    def __str__(self):
        return self.user_name


class Department(models.Model):
    """
    部门
    """
    DP_CHOICES = (
        (0, '非中心部门'),
        (1, '中心')
    )
    dpm_name = models.CharField(max_length=20, verbose_name='部门名称')
    dpm_remarks = models.TextField(max_length=400, verbose_name='部门备注')
    dpm_center = models.IntegerField(choices=DP_CHOICES, default=0, verbose_name='是否中心')
    dpm_creator = models.CharField(max_length=20, verbose_name='部门创建人')
    dpm_createDate = models.DateTimeField(auto_now_add=True, verbose_name='部门创建时间')

    class Meta:
        verbose_name = "部门"

    def __str__(self):
        return self.dpm_name


class Role(models.Model):
    """
    定义角色
    """
    role = models.CharField(max_length=15, verbose_name='角色名称', primary_key=True)
    role_description = models.TextField(max_length=400, verbose_name='角色描述')
    role_creator = models.CharField(max_length=20, verbose_name='角色创建人')
    role_createData = models.DateTimeField(auto_now_add=True, verbose_name="创建角色时间")

    class Meta:
        verbose_name = "角色"

    def __str__(self):
        return self.role


class Origanization(models.Model):
    """
    定义组织
    """

    orga_iden = models.CharField(max_length=6, verbose_name='组织编码', primary_key=True)
    orga_name = models.CharField(max_length=20, verbose_name='组织名称')
    area = models.ForeignKey('Area', verbose_name='区域', related_name='area_orga', on_delete=models.CASCADE)
    orga_remarks = models.TextField(max_length=400, verbose_name='组织备注')
    orga_creator = models.CharField(max_length=20, verbose_name='组织创建者')
    orga_createDate = models.DateTimeField(auto_now_add=True, verbose_name="组织创建时间")

    class Meta:
        verbose_name = "组织"

    def __str__(self):
        return self.orga_name


class Area(models.Model):
    """
    区域
    """

    area_name = models.CharField(max_length=8, verbose_name='区域名称', primary_key=True)

    class Meta:
        verbose_name = "区域"

    def __str__(self):
        return self.area_name


class Brand(models.Model):
    """
    品牌
    """
    brand_name = models.CharField(max_length=20, verbose_name='品牌名称', primary_key=True)
    brand_description = models.TextField(max_length=400, verbose_name='品牌描述')
    brand_creator = models.CharField(max_length=20, verbose_name='品牌创建者')
    brand_createDate = models.DateTimeField(auto_now_add=True, verbose_name='品牌创建时间')

    class Meta:
        verbose_name = "品牌"

    def __str__(self):
        return self.brand_name


class TotalWareHouse(models.Model):
    """
    总仓库
    """
    total_iden = models.CharField(max_length=6, verbose_name='总仓库编码', primary_key=True)
    total_name = models.CharField(max_length=20, verbose_name='总仓名字')
    organization = models.ForeignKey('Origanization', related_name='orga_total_ware_house', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', verbose_name='品牌', on_delete=models.CASCADE)
    total_remarks = models.TextField(max_length=400, verbose_name='总仓备注')
    total_creator = models.CharField(max_length=20, verbose_name="总仓创建者")
    total_createDate = models.DateTimeField(auto_now_add=True, verbose_name='总仓创建时间')

    class Meta:
        verbose_name = "总仓"

    def __str__(self):
        return self.total_name


class CenterWareHouse(models.Model):
    """
    中心仓库
    """
    center_wh_iden = models.CharField(max_length=6, verbose_name='中心仓库编码', primary_key=True)
    center_wh_name = models.CharField(max_length=20, verbose_name='中心仓库名字')
    origanization = models.ForeignKey('Origanization', related_name='orga_center_ware_house', verbose_name='组织',
                                      on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', verbose_name='品牌', on_delete=models.CASCADE)
    center_wh_remarks = models.TextField(max_length=400, verbose_name='中心仓库备注')
    center_wh_creator = models.CharField(max_length=20, verbose_name="中心创建者")
    center_wh_createDate = models.DateTimeField(auto_now_add=True, verbose_name='中心创建时间')

    class Meta:
        verbose_name = "中心仓库"

    def __str__(self):
        return self.center_wh_name


class Supplier(models.Model):
    """
    供应商
    """
    SUPPLY_TYPE_CHOICES = (
        (0, '内部单位'),
        (1, '外部单位')
    )
    supply_iden = models.CharField(max_length=7, verbose_name='供应商编码', primary_key=True)
    supply_name = models.CharField(max_length=20, verbose_name='供应商名称')
    supply_type = models.IntegerField(choices=SUPPLY_TYPE_CHOICES, default=0, verbose_name="供应商类型")
    supply_remarks = models.TextField(max_length=400, verbose_name='供应商备注')
    supply_creator = models.CharField(max_length=20, verbose_name='供应商创建者')
    supply_createDate = models.DateTimeField(auto_now_add=True, verbose_name='供应商创建时间')

    class Meta:
        verbose_name = "供应商"

    def __str__(self):
        return self.supply_name


class Center(models.Model):
    """
    中心
    """
    center_name = models.CharField(max_length=20, verbose_name='中心名称')
    area = models.ForeignKey('Area', verbose_name='区域', related_name='area_center', on_delete=models.CASCADE)
    center_remarks = models.TextField(max_length=400, verbose_name='中心备注')
    center_creator = models.CharField(max_length=20, verbose_name='中心创建者')
    center_createDate = models.DateTimeField(auto_now_add=True, verbose_name='中心创建时间')

    class Meta:
        verbose_name = "中心"

    def __str__(self):
        return self.center_name


class Customer(models.Model):
    """
    客户
    """

    Customer_TYPE_CHOICES = (
        (0, '内部单位'),
        (1, '外部单位')
    )

    customer_iden = models.CharField(max_length=7, verbose_name='客户编码', primary_key=True)
    customer_name = models.CharField(max_length=20, verbose_name='客户名称')
    customer_type = models.IntegerField(choices=Customer_TYPE_CHOICES, default=0, verbose_name="客户类型")
    customer_remarks = models.TextField(max_length=400, verbose_name='客户备注')
    customer_creator = models.CharField(max_length=20, verbose_name='客户创建者')
    customer_createDate = models.DateTimeField(auto_now_add=True, verbose_name='客户创建时间')

    class Meta:
        verbose_name = "客户"

    def __str__(self):
        return self.customer_name


class Meterage(models.Model):
    """
    计量单位
    """
    METERAGE_DIMENSION_CHOICES = (
        (0, '重量'),
        (1, '长度'),
        (2, '面积'),
        (3, '体积'),
        (4, '件数')
    )

    meterage_iden = models.CharField(max_length=6, verbose_name='计量单位编码', primary_key=True)
    meterage_name = models.CharField(max_length=20, verbose_name='计量单位名称')
    meterage_dimension = models.IntegerField(choices=METERAGE_DIMENSION_CHOICES, verbose_name="计量单位量纲")
    meterage_creator = models.CharField(max_length=20, verbose_name='计量单位创建者')
    meterage_createDate = models.DateTimeField(auto_now_add=True, verbose_name='计量单位创建时间')

    class Meta:
        verbose_name = "计量单位"

    def __str__(self):
        return self.meterage_name


class MaterialType(models.Model):
    """
    物料类别
    """
    type_iden = models.CharField(max_length=30, verbose_name='物料类别编码', primary_key=True)
    type_name = models.CharField(max_length=20, verbose_name='物料类别名称')
    type_creator = models.CharField(max_length=20, verbose_name='物料类别创建者')
    type_createDate = models.DateTimeField(auto_now_add=True, verbose_name='物料创建时间')

    class Meta:
        verbose_name = "计量单位"

    def __str__(self):
        return self.type_name


class Material(models.Model):
    """
    物料
    """
    MATERIAL_DIMENSION_CHOICES = (
        (0, '存货'),
        (1, '固定资产'),
        (2, '费用')
    )
    # 物料编码除了后五位其它全为分类编码
    material_iden = models.CharField(max_length=35, verbose_name='物料编码', primary_key=True)
    material_name = models.CharField(max_length=20, verbose_name='物料名称')
    material_specification = models.CharField(max_length=30, verbose_name='物料规格')
    material_model = models.CharField(max_length=30, verbose_name='物料型号')
    meterage = models.ForeignKey('Meterage', verbose_name='计量单位', related_name='meterage_material',
                                 on_delete=models.CASCADE)
    material_attr = models.IntegerField(choices=MATERIAL_DIMENSION_CHOICES, verbose_name='存货属性')
    material_creator = models.CharField(max_length=20, verbose_name='物料创建者')
    material_createDate = models.DateTimeField(auto_now_add=True, verbose_name='物料创建时间')

    class Meta:
        verbose_name = "物料"

    def __str__(self):
        return self.material_name

