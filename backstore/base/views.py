from django.db.models import Max
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .Serializer import UserProfileSerializer, AreaSerializer, RoleSerializer, CustomerSerializer, \
    OrganizationSerializer, BrandSerializer, TotalWareHouseSerializer, CenterSerializer, CenterWareHouseSerializer, \
    SupplierSerializer, MeterageSerializer, MaterialTypeSerializer, MaterialSerializer
from rest_framework.response import Response
# Create your views here.
from django.shortcuts import render, redirect
from base import models
import json
# Create your views here.
from django.http import HttpResponse

"""
用户维护接口
- 登录
- 添加
- 查看详细信息
- 查看所有用户信息
- 更新用户信息(单条)
"""


class LoginView(APIView):

    def post(self, request):
        user_id = self.request.data.get('user_id')
        user_passwd = self.request.data.get('user_passwd')
        try:
            user = authenticate(username=user_id, password=user_passwd)
        except models.UserProfile.DoesNotExist:
            return Response({'message': '用户名或密码错误', 'signal': '2'})
        else:
            if user.is_active == 1:
                login(request, user)
                return Response({'message': '登录成功', 'signal': '0'})
            elif user.is_active == 0:
                return Response({'message': '账号已关闭,请联系管理员开启', 'signal': '1'})


class UserView(APIView):

    def post(self, request):
        user_id = self.request.data.get('user_id')
        try:
            user = models.UserProfile.objects.get(username=user_id)
        except models.UserProfile.DoesNotExist:
            return Response({'message': '查询不到用户信息'})
        else:
            user_serializer = UserProfileSerializer(user)
            return Response({"user": user_serializer.data})


class UserNewView(APIView):
    def get(self, request):
        departments = models.Department.objects.filter(dpm_status=1).values_list('dpm_name', flat=True)
        roles = models.Role.objects.filter(role_status=1).values_list('role_name', flat=True)
        areas = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
        return Response({"departments": departments, "roles": roles, "areas": areas})


class UserAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "注册成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_id = json_data['user_id']
        user_passwd = json_data['user_passwd']
        user_name = json_data['user_name']
        user_phone_number = json_data['user_phone_number']
        user_mailbox = json_data['user_mailbox']
        user_status = json_data['user_status']
        user_departments = json_data['user_departments']
        user_roles = json_data['user_roles']
        user_creator = json_data['user_creator']
        area_name = json_data['area_name']

        # area = models.Area.objects.filter(area_name=area_name).first()
        # user_createDate = json_data['user_createDate']
        if self.idCheck(user_id):
            if self.phoneCheck(user_phone_number):
                if self.emailCheck(user_mailbox):
                    models.UserProfile.objects.create_user(username=user_id, password=user_passwd,
                                                           user_name=user_name, user_phone_number=user_phone_number,
                                                           email=user_mailbox, is_active=user_status,
                                                           user_departments=user_departments, user_roles=user_roles,
                                                           user_creator=user_creator,
                                                           area_name=area_name)
                    # pass
        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, user_id):
        try:
            user = models.UserProfile.objects.get(username=user_id)
        except models.UserProfile.DoesNotExist:
            return True
        else:
            self.message = "员工id已存在"
            self.signal = 1
            return False

    def phoneCheck(self, phone):
        try:
            user = models.UserProfile.objects.get(user_phone_number=phone)
        except models.UserProfile.DoesNotExist:
            return True
        else:
            self.message = "员工电话号码已存在"
            self.signal = 2
            return False

    def emailCheck(self, email):
        try:
            user = models.UserProfile.objects.get(email=email)
        except models.UserProfile.DoesNotExist:
            return True
        else:
            self.message = "员工email已存在"
            self.signal = 3
            return False


class UserUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "修改成功"
        self.signal = 0
        self.user_id = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        self.user_id = json_data['user_id']
        # user_passwd = json_data['user_passwd']
        # user_name = json_data['user_name']

        user_phone_number = json_data['user_phone_number']
        user_mailbox = json_data['user_mailbox']
        user_status = json_data['user_status']
        user_departments = json_data['user_departments']
        user_roles = json_data['user_roles']
        # user_creator = json_data['user_creator']
        area_name = json_data['area_name']
        # area = models.Area.objects.filter(area_name=area_name).first()
        user = models.UserProfile.objects.filter(username=self.user_id)

        if self.phoneCheck(user_phone_number):
            if self.emailCheck(user_mailbox):
                user.update(user_phone_number=user_phone_number,
                            email=user_mailbox, is_active=user_status,
                            user_departments=user_departments, user_roles=user_roles,
                            area_name=area_name)
        return Response({'message': self.message, 'signal': self.signal})

    def phoneCheck(self, phone):
        try:
            user = models.UserProfile.objects.get(user_phone_number=phone)
        except models.UserProfile.DoesNotExist:
            return True
        else:
            if user.username == self.user_id:
                return True
            else:
                self.message = "员工电话号码已存在"
                self.signal = 2
                return False

    def emailCheck(self, email):
        try:
            user = models.UserProfile.objects.get(email=email)
        except models.UserProfile.DoesNotExist:
            return True
        else:
            if user.username == self.user_id:
                return True
            else:
                self.message = "员工email已存在"
                self.signal = 3
                return False


class UsersView(APIView):

    def get(self, request):
        max_id = models.UserProfile.objects.all().aggregate(Max('username'))['username__max']
        users = models.UserProfile.objects.all()
        if users:
            users_serializer = UserProfileSerializer(users, many=True)
            return Response({"max_iden": max_id, "users": users_serializer.data})


"""
区域管理接口,暂时没实现添加功能
"""


class AreasView(APIView):

    def get(self, request):
        areas = models.Area.objects.all()
        if areas:
            area_serializer = AreaSerializer(areas, many=True)
            return Response({"areas": area_serializer.data})


"""
角色维护接口
- 查看角色详情业务
- 角色添加
- 角色状态修改

"""


class RolesView(APIView):

    def get(self, request):
        roles = models.Role.objects.all()
        if roles:
            roles_serializer = RoleSerializer(roles, many=True)
            return Response({"roles": roles_serializer.data})


class RoleAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        role_name = json_data['role_name']
        role_power = json_data['role_power']
        role_description = json_data['role_description']
        role_status = json_data['role_status']
        role_creator = json_data['role_creator']
        if self.nameCheck(role_name):
            models.Role.objects.create(role_name=role_name, role_power=role_power, role_description=role_description,
                                       role_status=role_status,
                                       role_creator=role_creator)
        return Response({'message': self.message, 'signal': self.signal})

    def nameCheck(self, name):
        try:
            user = models.Role.objects.get(role_name=name)
        except models.Role.DoesNotExist:
            return True
        else:
            self.message = "角色已经存在"
            self.signal = 1
            return False


class RoleUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        role_power = json_data['role_power']
        role_name = json_data['role_name']
        role_status = json_data['role_status']
        try:
            models.Role.objects.filter(role_name=role_name).update(role_power=role_power, role_status=role_status)
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
客户维护接口
- 查看客户详情业务
- 客户添加
- 客户信息修改
"""


class CustomersView(APIView):

    def get(self, request):
        max_id = models.Customer.objects.all().aggregate(Max('customer_iden'))['customer_iden__max']
        customers = models.Customer.objects.all()
        if customers:
            customers_serializer = CustomerSerializer(customers, many=True)
            return Response({"max_iden": max_id, "customers": customers_serializer.data})


class CustomerAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        customer_iden = json_data['customer_iden']
        customer_name = json_data['customer_name']
        customer_type = json_data['customer_type']
        customer_remarks = json_data['customer_remarks']
        customer_status = json_data['customer_status']
        customer_creator = json_data['customer_creator']
        models.Customer.objects.create(customer_iden=customer_iden, customer_name=customer_name,
                                       customer_type=customer_type,
                                       customer_remarks=customer_remarks, customer_status=customer_status,
                                       customer_creator=customer_creator)
        return Response({'message': self.message, 'signal': self.signal})


class CustomerUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        customer_iden = json_data['customer_iden']
        customer_name = json_data['customer_name']
        customer_type = json_data['customer_type']
        customer_remarks = json_data['customer_remarks']
        customer_status = json_data['customer_status']
        # customer_creator = json_data['customer_creator']
        try:
            models.Customer.objects.filter(customer_iden=customer_iden).update(customer_name=customer_name,
                                                                               customer_type=customer_type,
                                                                               customer_remarks=customer_remarks,
                                                                               customer_status=customer_status, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
组织维护接口
- 查看组织详情业务
- 组织添加
- 组织信息修改
"""


class OrganizationsView(APIView):

    def get(self, request):
        max_id = models.Organization.objects.all().aggregate(Max('orga_iden'))['orga_iden__max']
        organizations = models.Organization.objects.all()
        if organizations:
            organizations_serializer = OrganizationSerializer(organizations, many=True)
            return Response({"max_iden": max_id, "organizations": organizations_serializer.data})


class OrganizationNewView(APIView):
    def get(self, request):
        areas = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
        return Response({"areas": areas})


class OrganizationAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        orga_iden = json_data['orga_iden']
        orga_name = json_data['orga_name']
        area_name = json_data['area_name']
        orga_remarks = json_data['orga_remarks']
        orga_status = json_data['orga_status']
        orga_creator = json_data['orga_creator']
        models.Organization.objects.create(orga_iden=orga_iden, orga_name=orga_name,
                                           area_name=area_name,
                                           orga_remarks=orga_remarks,
                                           orga_status=orga_status,
                                           orga_creator=orga_creator)
        return Response({'message': self.message, 'signal': self.signal})


class OrganizationUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        orga_iden = json_data['orga_iden']
        orga_name = json_data['orga_name']
        orga_remarks = json_data['orga_remarks']
        orga_status = json_data['orga_status']
        # orga_creator = json_data['orga_creator']
        try:
            models.Organization.objects.filter(orga_iden=orga_iden).update(
                orga_name=orga_name,
                orga_remarks=orga_remarks,
                orga_status=orga_status, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
部门维护接口
- 查看部门详情业务
- 部门添加
- 部门信息修改
"""

"""
品牌维护接口
- 查看品牌详情业务
- 品牌添加
- 品牌信息修改
"""


class BrandsView(APIView):

    def get(self, request):
        brands = models.Brand.objects.all()
        if brands:
            brands_serializer = BrandSerializer(brands, many=True)
            return Response({"brands": brands_serializer.data})


class BrandAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        brand_name = json_data['brand_name']
        brand_description = json_data['brand_description']
        brand_status = json_data['brand_status']
        brand_creator = json_data['brand_creator']
        if self.nameCheck(brand_name):
            models.Brand.objects.create(brand_name=brand_name,
                                        brand_description=brand_description,
                                        brand_status=brand_status,
                                        brand_creator=brand_creator)
        return Response({'message': self.message, 'signal': self.signal})

    def nameCheck(self, name):
        try:
            user = models.Brand.objects.get(brand_name=name)
        except models.Brand.DoesNotExist:
            return True
        else:
            self.message = "品牌已经存在"
            self.signal = 1
            return False


class BrandUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        brand_name = json_data['brand_name']
        brand_description = json_data['brand_description']
        brand_status = json_data['brand_status']
        # brand_creator = json_data['brand_creator']
        try:
            models.Brand.objects.filter(brand_name=brand_name).update(
                brand_name=brand_name,
                brand_description=brand_description,
                brand_status=brand_status, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
总仓维护接口
- 查看总仓详情
- 总仓添加
- 总仓信息更新
"""


class TotalWareHousesView(APIView):

    def get(self, request):
        max_id = models.TotalWareHouse.objects.all().aggregate(Max('total_iden'))['total_iden__max']
        totalWareHouses = models.TotalWareHouse.objects.all()
        if totalWareHouses:
            totalWareHouses_serializer = TotalWareHouseSerializer(totalWareHouses, many=True)
            return Response({"max_iden": max_id, "totalWareHouses": totalWareHouses_serializer.data})


class TotalWareHouseNewView(APIView):
    def get(self, request):
        brands = models.Brand.objects.filter(brand_status=1).values_list('brand_name', flat=True)
        organizations = {}
        areas_name = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
        for area_name in areas_name:
            organization = models.Organization.objects.filter(area_name=area_name, orga_status=1).values_list(
                'orga_name', flat=True)
            print(organization)
            organizations[area_name] = organization
        return Response({"brands": brands, "organizations": organizations})


class TotalWareHouseAddView(APIView):
    """
    这里绑定组织通过area_name和orga_name再绑定
    可以优化为传入前端orga_iden ，传回的时候传iden
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        total_iden = json_data['total_iden']
        total_name = json_data['total_name']
        area_name = json_data['area_name']
        orga_name = json_data['orga_name']
        brand_name = json_data['brand_name']
        total_remarks = json_data['total_remarks']
        total_status = json_data['total_status']
        total_creator = json_data['total_creator']
        organization = models.Organization.objects.get(area_name=area_name, orga_name=orga_name)
        models.TotalWareHouse.objects.create(total_iden=total_iden, total_name=total_name,
                                             brand_name=brand_name,
                                             organization=organization,
                                             total_remarks=total_remarks,
                                             total_status=total_status,
                                             total_creator=total_creator)
        return Response({'message': self.message, 'signal': self.signal})


class TotalWareHouseUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        total_iden = json_data['total_iden']
        # total_name = json_data['total_name']
        total_remarks = json_data['total_remarks']
        total_status = json_data['total_status']
        # total_creator = json_data['total_creator']
        try:
            models.TotalWareHouse.objects.filter(total_iden=total_iden).update(
                # total_name=total_name,
                total_remarks=total_remarks,
                total_status=total_status, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
中心维护接口
- 查看中心情况
- 中心添加
- 中心信息更新
"""


class CentersView(APIView):

    def get(self, request):
        centers = models.Center.objects.all()
        if centers:
            centers_serializer = CenterSerializer(centers, many=True)
            return Response({"centers": centers_serializer.data})


class CenterNewView(APIView):
    def get(self, request):
        areas = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
        return Response({"areas": areas})


class CenterAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        center_name = json_data['center_name']
        area_name = json_data['area_name']
        center_remarks = json_data['center_remarks']
        center_status = json_data['center_status']
        center_creator = json_data['center_creator']
        models.Center.objects.create(center_name=center_name,
                                     area_name=area_name,
                                     center_remarks=center_remarks, center_status=center_status,
                                     center_creator=center_creator)
        return Response({'message': self.message, 'signal': self.signal})


class CenterUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        center_name = json_data['center_name']
        area_name = json_data['area_name']
        center_remarks = json_data['center_remarks']
        center_status = json_data['center_status']
        # center_creator = json_data['center_creator']
        try:
            models.Center.objects.filter(center_name=center_name, area_name=area_name).update(center_name=center_name,
                                                                                              center_remarks=center_remarks,
                                                                                              center_status=center_status, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""

中心仓库维护接口
- 查看中心仓库情况
- 增加中心仓库
- 修改中心仓库信息

"""


class CenterWareHousesView(APIView):

    def get(self, request):
        centerWareHouses = models.CenterWareHouse.objects.all()
        if centerWareHouses:
            centerWareHouses_serializer = CenterWareHouseSerializer(centerWareHouses, many=True)
            return Response({"centerWareHouses": centerWareHouses_serializer.data})


class CenterWareHouseNewView(APIView):
    def get(self, request):
        brands = models.Brand.objects.filter(brand_status=1).values_list('brand_name', flat=True)
        organizations = {}
        areas_name = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
        for area_name in areas_name:
            orga_center = []
            organization = models.Organization.objects.filter(area_name=area_name, orga_status=1).values_list(
                'orga_name', flat=True)
            center = models.Center.objects.filter(area_name=area_name, center_status=1).values_list('center_name',
                                                                                                    flat=True)
            orga_center.append(organization)
            orga_center.append(center)
            organizations[area_name] = orga_center
        return Response({"brands": brands, "organizations": organizations})


class CenterWareHouseAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        center_wh_iden = json_data['center_wh_iden']
        center_wh_name = json_data['center_wh_name']
        area_name = json_data['area_name']
        orga_name = json_data['orga_name']
        center_name = json_data['center_name']
        brand_name = json_data['brand_name']
        center_wh_remarks = json_data['center_wh_remarks']
        center_wh_status = json_data['center_wh_status']
        center_wh_creator = json_data['center_wh_creator']
        organization = models.Organization.objects.get(area_name=area_name, orga_name=orga_name)
        center = models.Center.objects.get(center_name=center_name)
        models.CenterWareHouse.objects.create(center_wh_iden=center_wh_iden, center_wh_name=center_wh_name,
                                              organization=organization, center=center,
                                              brand_name=brand_name,
                                              center_wh_remarks=center_wh_remarks, center_wh_status=center_wh_status,
                                              center_wh_creator=center_wh_creator)
        return Response({'message': self.message, 'signal': self.signal})


class CenterWareHouseUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        center_wh_iden = json_data['center_wh_iden']
        center_wh_remarks = json_data['center_wh_remarks']
        center_wh_status = json_data['center_wh_status']
        # center_wh_creator = json_data['center_wh_creator']
        try:
            models.CenterWareHouse.objects.filter(center_wh_iden=center_wh_iden, ).update(
                center_wh_remarks=center_wh_remarks,
                center_wh_status=center_wh_status, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
供应商维护接口
- 查看供应商
- 增加供应商
- 修改供应商信息
"""


class SuppliersView(APIView):

    def get(self, request):
        max_id = models.Supplier.objects.all().aggregate(Max('supply_iden'))['supply_iden__max']
        suppliers = models.Supplier.objects.all()
        if suppliers:
            suppliers_serializer = SupplierSerializer(suppliers, many=True)
            return Response({"max_iden": max_id, "suppliers": suppliers_serializer.data})


class SupplierAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        supply_iden = json_data['supply_iden']
        supply_name = json_data['supply_name']
        supply_type = json_data['supply_type']
        supply_remarks = json_data['supply_remarks']
        supply_status = json_data['supply_status']
        supply_creator = json_data['supply_creator']
        models.Supplier.objects.create(supply_iden=supply_iden, supply_name=supply_name,
                                       supply_type=supply_type,
                                       supply_remarks=supply_remarks, supply_status=supply_status,
                                       supply_creator=supply_creator)
        return Response({'message': self.message, 'signal': self.signal})


class SupplierUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        supply_iden = json_data['supply_iden']
        supply_name = json_data['supply_name']
        supply_type = json_data['supply_type']
        supply_remarks = json_data['supply_remarks']
        supply_status = json_data['supply_status']
        # supply_creator = json_data['supply_creator']
        try:
            models.Supplier.objects.filter(supply_iden=supply_iden).update(supply_name=supply_name,
                                                                           supply_type=supply_type,
                                                                           supply_remarks=supply_remarks,
                                                                           supply_status=supply_status, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
计量单位维护接口
- 查看计量单位
- 增加计量单位
- 修改计量单位信息
"""


class MeteragesView(APIView):

    def get(self, request):
        max_id = models.Meterage.objects.all().aggregate(Max('meterage_iden'))['meterage_iden__max']
        meterages = models.Meterage.objects.all()
        if meterages:
            meterages_serializer = MeterageSerializer(meterages, many=True)
            return Response({"max_iden": max_id, "meterages": meterages_serializer.data})


class MeterageAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        meterage_iden = json_data['meterage_iden']
        meterage_name = json_data['meterage_name']
        meterage_dimension = json_data['meterage_dimension']
        meterage_status = json_data['meterage_status']
        meterage_creator = json_data['meterage_creator']
        models.Meterage.objects.create(meterage_iden=meterage_iden, meterage_name=meterage_name,
                                       meterage_dimension=meterage_dimension,
                                       meterage_status=meterage_status,
                                       meterage_creator=meterage_creator)
        return Response({'message': self.message, 'signal': self.signal})


class MeterageUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        meterage_iden = json_data['meterage_iden']
        meterage_name = json_data['meterage_name']
        meterage_dimension = json_data['meterage_dimension']
        meterage_status = json_data['meterage_status']

        try:
            models.Meterage.objects.filter(meterage_iden=meterage_iden).update(meterage_name=meterage_name,
                                                                               meterage_dimension=meterage_dimension,
                                                                               meterage_status=meterage_status, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})


"""
物料类别维护接口
- 查看物料类别
- 增加物料类别
- 修改物料类别信息
"""


class MaterialTypesView(APIView):

    def get(self, request):
        max_id = models.MaterialType.objects.all().aggregate(Max('type_iden'))['type_iden__max']
        material_types = models.MaterialType.objects.all()
        if material_types:
            material_types_serializer = MaterialTypeSerializer(material_types, many=True)
            return Response({"max_iden": max_id, "meterial_types": material_types_serializer.data})


class MaterialTypeAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.massage = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        type_iden = json_data['type_iden']
        type_name = json_data['type_name']
        type_status = json_data['type_status']
        type_creator = json_data['type_creator']
        models.MaterialType.objects.create(type_iden=type_iden, type_name=type_name,
                                           type_status=type_status,
                                           type_creator=type_creator)
        return Response({'massage': self.massage, 'signal': self.signal})


class MaterialTypeUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.massage = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        type_iden = json_data['type_iden']
        type_name = json_data['type_name']

        try:
            models.MaterialType.objects.filter(type_iden=type_iden).update(type_name=type_name, )
        except:
            self.massage = "更新失败"
            self.signal = 1
        return Response({'massage': self.massage, 'signal': self.signal})


"""
物料维护接口
- 查看物料
- 增加物料
- 修改物料信息
"""


class MaterialsView(APIView):

    def get(self, request):
        Materials = models.Material.objects.all()
        if Materials:
            Materials_serializer = MaterialSerializer(Materials, many=True)
            return Response({"Materials": Materials_serializer.data})


class MaterialNewView(APIView):
    def get(self, request):
        """
        物料类别及其名字和最大流水号编码
        """
        material_types = models.MaterialType.objects.filter(type_status=1).values_list('type_iden', 'type_name')
        material_types = [list(material_type) for material_type in material_types]
        for i, material_type in enumerate(material_types):
            material_iden = models.Material.objects.filter(material_type_iden=material_type[0]).aggregate(Max('material_iden'
                                                                                                         ))[
                'material_iden__max']
            material_types[i].append(material_iden)

        """
        计量单位包括量纲和计量单位名称
        """
        meterages = models.Meterage.objects.filter(meterage_status=1).values_list('meterage_dimension',
                                                                              'meterage_iden', 'meterage_name')
        # 这里没有按照量纲再去区别
        return Response({"material_types": material_types, "meterages": meterages})


class MaterialAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        material_iden = json_data['material_iden']
        material_name = json_data['material_name']
        material_type_iden = json_data['material_type_iden']
        material_specification = json_data['material_specification']
        material_model = json_data['material_model']
        meterage_name = json_data['meterage_name']
        material_attr = json_data['material_attr']
        material_status = json_data['material_status']
        material_creator = json_data['material_creator']

        models.Material.objects.create(material_iden=material_iden, material_name=material_name,
                                       material_type_iden=material_type_iden,
                                       material_specification=material_specification,
                                       material_model=material_model, meterage_name=meterage_name,
                                       material_attr=material_attr, material_status=material_status,
                                       material_creator=material_creator)
        return Response({'message': self.message, 'signal': self.signal})


class MaterialUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        material_iden = json_data['material_iden']
        material_name = json_data['material_name']
        material_specification = json_data['material_specification']
        material_model = json_data['material_model']
        meterage_name = json_data['meterage_name']
        material_attr = json_data['material_attr']

        try:
            models.Material.objects.filter(material_iden=material_iden).update(
                material_name=material_name,
                material_specification=material_specification,
                material_model=material_model, meterage_name=meterage_name,
                material_attr=material_attr, )
        except:
            self.message = "更新失败"
            self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})
