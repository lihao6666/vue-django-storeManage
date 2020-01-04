from django.db.models import Max
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .Serializer import UserProfileSerializer, AreaSerializer, RoleSerializer, CustomerSerializer, \
    OrganizationSerializer, BrandSerializer, TotalWareHouseSerializer, CenterSerializer, \
    SupplierSerializer, MeterageSerializer, MaterialTypeSerializer, MaterialSerializer, DepartmentSerializer
from rest_framework.response import Response
# Create your views here.
from django.shortcuts import render, redirect
from base import models
import json
# Create your views here.
from django.http import HttpResponse


def departmentToList(departments_name_list):
    dpm_list = []
    for department_name in departments_name_list:
        id = str(models.Department.objects.get(dpm_name=department_name).id)
        dpm_list.append(id)
    dpm_name = "-".join(dpm_list)

    return dpm_name


def roleToList(roles_name_list):
    role_list = []
    for role_name in roles_name_list:
        id = str(models.Role.objects.get(role=role_name).id)
        role_list.append(id)
    role_name = "-".join(role_list)

    return role_name


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
        json_data = json.loads(self.request.body.decode("utf-8"))
        # user_now = models.UserNow.objects.get()
        # if user_now:
        #     return Response({"message": "老子已经在线了，你还想挤掉我"})
        user_iden = json_data['user_iden']
        user_passwd = json_data['user_passwd']
        # user_iden = self.request.data.get('user_iden')
        # user_passwd = self.request.data.get('user_passwd')
        try:
            user = authenticate(username=user_iden, password=user_passwd)
        except models.UserProfile.DoesNotExist:
            return Response({'message': '登录异常', 'signal': '3'})
        else:
            if user:
                if user.is_active == 1:
                    login(request, user)
                    user = models.UserProfile.objects.get(username=user_iden)
                    user_id = user.id
                    username = user.username
                    user_name = user.user_name
                    area_name = user.area_name
                    user_departments = user.user_departments
                    user_roles = user.user_roles

                    models.UserNow.objects.create(user_id=user_id, user_iden=username, user_name=user_name,
                                                  area_name=area_name,
                                                  user_departments=user_departments, user_roles=user_roles)

                    return Response({'message': '登录成功', 'signal': '0'})
                elif user.is_active == 0:
                    return Response({'message': '账号已关闭,请联系管理员开启', 'signal': '1'})
            else:
                return Response({'message': '用户名或密码错误', 'signal': '2'})


class LoginExitView(APIView):
    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        models.UserNow.objects.get(user_iden=user_now_iden).delete()  # 删除当前用户表信息
        logout(request)
        return Response({"message": "退出登录成功"})


class UserView(APIView):

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            try:
                user = models.UserProfile.objects.get(username=user_now.user_iden)
            except models.UserProfile.DoesNotExist:
                return Response({'message': '查询不到用户信息'})
            else:
                user_serializer = UserProfileSerializer(user)
                return Response({"user": user_serializer.data})
        return Response({"message": "用户未登录"})


class UserNewView(APIView):
    def get(self, request):
        max_id = models.UserProfile.objects.all().aggregate(Max('username'))['username__max']
        departments = models.Department.objects.filter(dpm_status=1).values_list('dpm_name', flat=True)
        roles = models.Role.objects.filter(role_status=1).values_list('role', flat=True)
        areas = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)

        return Response({"max_iden": max_id, "departments": departments, "roles": roles, "areas": areas})


class UserAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "注册成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):

        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
        username = json_data['username']
        password = json_data['password']
        user_name = json_data['user_name']
        user_phone_number = json_data['user_phone_number']
        email = json_data['email']

        # max_id = models.UserProfile.objects.all().aggregate(Max('username'))['username__max']
        # user_iden = str(int(max_id) + 1)  # 编号后台处理过了

        user_departments = departmentToList(json_data['user_departments'])  # 传过来的是名字列表
        user_roles = roleToList(json_data['user_roles'])  # 传过来的是角色列表

        area_name = json_data['area_name']

        # user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        # user_creator = user_now.user_name
        # user_creator_iden = user_now.user_iden

        # area = models.Area.objects.filter(area_name=area_name).first()
        # user_createDate = json_data['user_createDate']
        if self.idCheck(username):
            if self.phoneCheck(user_phone_number):
                if self.emailCheck(email):
                    models.UserProfile.objects.create_user(username=username, password=password,
                                                           user_name=user_name, user_phone_number=user_phone_number,
                                                           email=email, is_active=0,
                                                           user_departments=user_departments, user_roles=user_roles,
                                                           user_creator=self.user_now_name,
                                                           user_creator_iden=user_now_iden,
                                                           area_name=area_name)
                    # pass
        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, user_iden):
        try:
            user = models.UserProfile.objects.get(username=user_iden)
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

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        id = json_data["id"]
        username = json_data['username']  # 需要传过来要修改用户的id
        # user_passwd = json_data['user_passwd']
        user_name = json_data['user_name']

        user_phone_number = json_data['user_phone_number']
        email = json_data['email']
        user_departments = departmentToList(json_data['user_departments'])  # 传过来的是名字列表
        user_roles = roleToList(json_data['user_roles'])  # 传过来的是角色列表
        # user_creator = json_data['user_creator']
        area_name = json_data['area_name']
        # area = models.Area.objects.filter(area_name=area_name).first()
        user = models.UserProfile.objects.filter(id=id)
        if self.idCheck(username, id):
            if self.phoneCheck(user_phone_number, id):
                if self.emailCheck(email, id):
                    if user:
                        user.update(username=username, user_name=user_name, user_phone_number=user_phone_number,
                                    email=email,
                                    user_departments=user_departments, user_roles=user_roles,
                                    area_name=area_name)
                    else:
                        self.message = "员工查询出错"
                        self.signal = 1

        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, user_iden, id):
        try:
            user = models.UserProfile.objects.get(~Q(id=id), username=user_iden)
        except models.UserProfile.DoesNotExist:
            return True
        else:
            self.message = "员工id已存在"
            self.signal = 1
            return False

    def phoneCheck(self, phone, id):
        try:
            user = models.UserProfile.objects.get(~Q(id=id), user_phone_number=phone)
        except models.UserProfile.DoesNotExist:
            return True
        else:
            if user.username == self.user_iden:
                return True
            else:
                self.message = "员工电话号码已存在"
                self.signal = 2
                return False

    def emailCheck(self, email, id):
        try:
            user = models.UserProfile.objects.get(~Q(id=id), email=email)
        except models.UserProfile.DoesNotExist:
            return True
        else:
            if user.username == self.user_iden:
                return True
            else:
                self.message = "员工email已存在"
                self.signal = 3
                return False


class UserStatusView(APIView):
    def post(self):
        json_data = json.loads(self.request.body.decode("utf-8"))
        is_active = json_data['is_active']
        username = json_data['username']
        user = models.UserProfile.objects.filter(username=username)
        if user:
            user.update(is_active=is_active, )
            return Response({"message": "状态更改成功", "signal": 0})
        else:
            return Response({"message": "未查询到用户,状态更改失败"})


class UsersView(APIView):

    # @login_required
    def get(self, request):
        users = models.UserProfile.objects.all()
        if users:
            departments_list = []
            roles_list = []
            users_serializer = UserProfileSerializer(users, many=True)
            for user in users:
                department_list = []
                role_list = []
                departments = user.user_departments.split("-")
                roles = user.user_roles.split("-")
                if user.user_departments:
                    for department in departments:
                        department_list.append(models.Department.objects.get(id=department).dpm_name)
                if user.user_roles:
                    for role in roles:
                        role_list.append(models.Role.objects.get(id=role).role)
                departments_list.append(department_list)
                roles_list.append(role_list)
            return Response({"users": users_serializer.data, "departments": departments_list, "roles": roles_list})


"""
区域管理接口,暂时没实现添加功能
"""


class AreasView(APIView):
    def get(self, request):
        areas = models.Area.objects.filter(area_status=1).all()
        if areas:
            area_serializer = AreaSerializer(areas, many=True)
            return Response({"areas": area_serializer.data})
        else:
            return Response({"message": "未查询到信息"})


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
        else:
            return Response({"message": "未查询到信息"})


class RoleAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
        role = json_data['role']  # 角色名字
        role_power = json_data['role_power']  # 角色权限
        role_description = json_data['role_description']  # 角色描述
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            # creator = user_now.user_name
            # creator_iden = user_now.user_iden
            if self.nameCheck(role):
                models.Role.objects.create(role=role, role_power=role_power, role_description=role_description,
                                           role_status=0,
                                           role_creator=self.user_now_name,
                                           role_creator_iden=user_now_iden)
        else:
            self.message = "用户未登录"
            self.signal = 2

        return Response({'message': self.message, 'signal': self.signal})

    def nameCheck(self, name):
        try:
            user = models.Role.objects.get(role=name)
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
        id = json_data['id']
        role_power = json_data['role_power']
        role = json_data['role']

        # role_status = json_data['role_status']
        role_description = json_data['role_description']
        if self.nameCheck(role, id):
            try:
                models.Role.objects.filter(id=id).update(role_power=role_power, role=role,
                                                         role_description=role_description)
            except:
                self.message = "更新失败"
                self.signal = 1

        return Response({'message': self.message, 'signal': self.signal})

    def nameCheck(self, name, id):
        try:
            user = models.Role.objects.get(~Q(id=id), role=name)
        except models.Role.DoesNotExist:
            return True
        else:
            self.message = "角色名字已经存在"
            self.signal = 2
            return False


class RoleStatusView(APIView):
    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))

        role_status = json_data['role_status']
        id = json_data['id']
        # role_name = json_data['role']

        role = models.Role.objects.filter(id=id)

        if role:
            role.update(role_status=role_status)
            return Response({"message": "状态更改成功", "signal": 0})
        else:
            return Response({"message": "未查询到角色,状态更改失败"})


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
            return Response({"max_id": max_id, "customers": customers_serializer.data})
        else:
            return Response({"message": "未查询到信息"})


class CustomerAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name

        max_id = models.Customer.objects.all().aggregate(Max('customer_iden'))['customer_iden__max']
        customer_iden = str(int(max_id) + 1)  # 编号后台处理过了

        customer_name = json_data['customer_name']
        customer_type = json_data['customer_type']
        customer_remarks = json_data['customer_remarks']

        if self.idCheck(customer_iden, id):
            models.Customer.objects.create(customer_iden=customer_iden, customer_name=customer_name,
                                           customer_type=customer_type,
                                           customer_remarks=customer_remarks, customer_status=0,
                                           customer_creator=self.user_now_name,
                                           customer_creator_iden=user_now_iden)
        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, customer_iden, id):
        try:
            user = models.Customer.objects.get(~Q(id=id), customer_iden=customer_iden)
        except models.Customer.DoesNotExist:
            return True
        else:
            self.message = "客户id已存在"
            self.signal = 1
            return False


class CustomerUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        id = json_data["id"]
        customer_iden = json_data['customer_iden']
        customer_name = json_data['customer_name']
        customer_type = json_data['customer_type']
        customer_remarks = json_data['customer_remarks']
        # customer_status = json_data['customer_status']
        # customer_creator = json_data['customer_creator']
        if self.idCheck(customer_iden, id):
            try:
                models.Customer.objects.filter(id=id).update(customer_name=customer_name, customer_iden=customer_iden,
                                                             customer_type=customer_type,
                                                             customer_remarks=customer_remarks)
            except:
                self.message = "更新失败"
                self.signal = 2
        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, customer_iden, id):
        try:
            user = models.Customer.objects.get(~Q(id=id), customer_iden=customer_iden)
        except models.Customer.DoesNotExist:
            return True
        else:
            self.message = "客户id已存在"
            self.signal = 1
            return False


class CustomerStatusView(APIView):
    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))

        customer_status = json_data['role_status']
        customer_iden = json_data['customer_iden']

        customer = models.Customer.objects.filter(customer_iden=customer_iden)

        if customer:
            customer.update(customer_status=customer_status)
            return Response({"message": "状态更改成功", "signal": 0})
        else:
            return Response({"message": "未查询到客户,状态更改失败"})


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
        else:
            return Response({"message": "未查询到信息"})


class OrganizationNewView(APIView):
    def get(self, request):
        areas = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
        return Response({"areas": areas})


class OrganizationAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
        orga_iden = json_data['orga_iden']
        orga_name = json_data['orga_name']
        area_name = json_data['area_name']
        orga_remarks = json_data['orga_remarks']

        if self.idCheck(orga_iden):
            models.Organization.objects.create(orga_iden=orga_iden, orga_name=orga_name,
                                               area_name=area_name,
                                               orga_remarks=orga_remarks,
                                               orga_status=0,
                                               orga_creator=self.user_now_name,
                                               orga_creator_iden=user_now_iden)
        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, orga_iden):
        try:
            user = models.Organization.objects.get(orga_iden=orga_iden)
        except models.Organization.DoesNotExist:
            return True
        else:
            self.message = "组织id已存在"
            self.signal = 1
            return False


class OrganizationUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        id = json_data["id"]
        orga_iden = json_data['orga_iden']
        orga_name = json_data['orga_name']
        orga_remarks = json_data['orga_remarks']
        # orga_creator = json_data['orga_creator']
        if self.idCheck(orga_iden, id):
            try:
                models.Organization.objects.filter(id=id).update(
                    orga_iden=orga_iden,
                    orga_name=orga_name,
                    orga_remarks=orga_remarks, )
            except:
                self.message = "更新失败"
                self.signal = 2
        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, orga_iden, id):
        try:
            user = models.Organization.objects.get(~Q(id=id), orga_iden=orga_iden)
        except models.Organization.DoesNotExist:
            return True
        else:
            self.message = "组织id已存在"
            self.signal = 1
            return False


class OrganizationStatusView(APIView):
    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))

        orga_status = json_data['orga_status']
        orga_iden = json_data['orga_iden']

        organization = models.Organization.objects.filter(orga_iden=orga_iden)

        if organization:
            organization.update(orga_status=orga_status)
            return Response({"message": "状态更改成功", "signal": 0})
        else:
            return Response({"message": "未查询到组织,状态更改失败"})


"""
部门维护接口(暂时没有实现)
- 查看部门详情业务
- 部门添加
- 部门信息修改
"""


class DepartmentsView(APIView):

    def get(self, request):
        dpms = models.Department.objects.all()
        if dpms:
            dpms_serializer = DepartmentSerializer(dpms, many=True)
            return Response({"departments": dpms_serializer.data})
        else:
            return Response({"message": "未查询到信息"})


class DepartmentAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):

        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
        dpm_name = json_data['dpm_name']
        dpm_remarks = json_data['dpm_remarks']
        dpm_center = json_data['dpm_center']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            if self.nameCheck(dpm_name):
                models.Department.objects.create(dpm_name=dpm_name, dpm_remarks=dpm_remarks,
                                                 dpm_status=0, dpm_center=dpm_center,
                                                 dpm_creator=self.user_now_name,
                                                 creator_iden=user_now_iden)
        else:
            self.message = "用户未登录"
            self.signal = 2

        return Response({'message': self.message, 'signal': self.signal})

    def nameCheck(self, name):
        try:
            user = models.Department.objects.get(dpm=name)
        except models.Department.DoesNotExist:
            return True
        else:
            self.message = "角色已经存在"
            self.signal = 1
            return False


class DepartmentUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        id = json_data['id']
        dpm_remarks = json_data['dpm_remarks']
        dpm_name = json_data['dpm_name']

        # dpm_status = json_data['dpm_status']
        if self.nameCheck(dpm_name, id):
            try:
                models.Department.objects.filter(id=id).update(dpm_name=dpm_name, dpm_remarks=dpm_remarks)
            except:
                self.message = "更新失败"
                self.signal = 1

        return Response({'message': self.message, 'signal': self.signal})

    def nameCheck(self, name, id):
        try:
            user = models.Department.objects.get(~Q(id=id), dpm_name=name)
        except models.Department.DoesNotExist:
            return True
        else:
            self.message = "部门名字已经存在"
            self.signal = 2
            return False


class DepartmentStatusView(APIView):
    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))

        dpm_status = json_data['dpm_status']
        id = json_data["id"]
        # dpm_iden = json_data['dpm_iden']

        dpm = models.Department.objects.filter(id=id)

        if dpm:
            dpm.update(dpm_status=dpm_status)
            return Response({"message": "状态更改成功", "signal": 0})
        else:
            return Response({"message": "未查询到部门,状态更改失败"})


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
        else:
            return Response({"message": "未查询到信息"})


class BrandAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
        brand_name = json_data['brand_name']
        brand_description = json_data['brand_description']
        if self.nameCheck(brand_name):
            models.Brand.objects.create(brand_name=brand_name,
                                        brand_description=brand_description,
                                        brand_creator=self.user_now_name,
                                        brand_creator_iden=user_now_iden)
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
        id = json_data['id']
        brand_name = json_data['brand_name']
        brand_description = json_data['brand_description']
        # brand_status = json_data['brand_status']
        # brand_creator = json_data['brand_creator']
        if self.nameCheck(brand_name, id):
            try:
                models.Brand.objects.filter(id=id).update(
                    brand_name=brand_name,
                    brand_description=brand_description, )
            except:
                self.message = "更新失败"
                self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})

    def nameCheck(self, name, id):
        try:
            user = models.Brand.objects.get(~Q(id=id), brand_name=name)
        except models.Brand.DoesNotExist:
            return True
        else:
            self.message = "品牌已经存在"
            self.signal = 2
            return False


class BrandStatusView(APIView):
    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))

        brand_status = json_data['brand_status']
        id = json_data["id"]
        # dpm_iden = json_data['dpm_iden']

        brand = models.Brand.objects.filter(id=id)

        if brand:
            brand.update(brand_status=brand_status)
            return Response({"message": "状态更改成功", "signal": 0})
        else:
            return Response({"message": "未查询到品牌,状态更改失败"})


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
        else:
            return Response({"message": "未查询到信息"})


class TotalWareHouseNewView(APIView):
    def get(self, request):
        brands = models.Brand.objects.filter(brand_status=1).values_list('brand_name', flat=True)
        organizations = {}
        centers = {}
        areas_name = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
        for area_name in areas_name:
            organization = models.Organization.objects.filter(area_name=area_name, orga_status=1).values_list(
                'orga_name', flat=True)
            center = models.Center.objects.filter(area_name=area_name, center_status=1).values_list('center_name',
                                                                                                    flat=True)
            organizations[area_name] = organization
            centers[area_name] = center
        return Response({"brands": brands, "organizations": organizations, "centers": centers, "areas": areas_name})


class TotalWareHouseAddView(APIView):
    """
    这里绑定组织通过area_name和orga_name再绑定
    可以优化为传入前端orga_iden ，传回的时候传iden
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name

        total_iden = json_data['total_iden']
        total_name = json_data['total_name']
        area_name = json_data['area_name']
        orga_name = json_data['orga_name']
        brand_name = json_data['brand_name']
        total_belong_center = json_data['total_belong_center']
        total_belong_center_iden = json_data['total_belong_center_iden']

        total_remarks = json_data['total_remarks']

        organization = models.Organization.objects.get(area_name=area_name, orga_name=orga_name)
        if self.idCheck(total_iden):
            models.TotalWareHouse.objects.create(total_iden=total_iden, total_name=total_name,
                                                 total_belong_center=total_belong_center,
                                                 total_belong_center_iden=total_belong_center_iden,
                                                 brand_name=brand_name,
                                                 organization=organization,
                                                 total_remarks=total_remarks,
                                                 total_status=0,
                                                 total_creator=self.user_now_name,
                                                 total_creator_iden=user_now_iden)
        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, total_iden):
        try:
            user = models.TotalWareHouse.objects.get(total_iden=total_iden)
        except models.TotalWareHouse.DoesNotExist:
            return True
        else:
            self.message = "仓库id已存在"
            self.signal = 1
            return False


class TotalWareHouseUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        id = json_data['id']
        total_iden = json_data['total_iden']
        total_name = json_data['total_name']
        # total_belong_center = json_data['total_belong_center']

        brand_name = json_data['brand_name']

        total_remarks = json_data['total_remarks']
        # total_status = json_data['total_status']
        if self.idCheck(total_iden, id):
            try:
                models.TotalWareHouse.objects.filter(total_iden=total_iden).update(
                    total_name=total_name,
                    brand_name=brand_name,
                    total_remarks=total_remarks)
            except:
                self.message = "更新失败"
                self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})

    def idCheck(self, total_iden, id):
        try:
            user = models.TotalWareHouse.objects.get(~Q(id=id), total_iden=total_iden)
        except models.TotalWareHouse.DoesNotExist:
            return True
        else:
            self.message = "仓库id已存在"
            self.signal = 1
            return False


class TotalWareHouseStatusView(APIView):
    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))

        total_status = json_data['total_status']
        id = json_data["id"]
        # dpm_iden = json_data['dpm_iden']

        total = models.TotalWareHouse.objects.filter(id=id)

        if total:
            total.update(brand_status=total_status)
            return Response({"message": "状态更改成功", "signal": 0})
        else:
            return Response({"message": "未查询到仓库,状态更改失败"})


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
        else:
            return Response({"message": "未查询到信息"})


class CenterNewView(APIView):
    def get(self, request):
        areas = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
        return Response({"areas": areas})


class CenterAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
        # center_iden = json_data['center_iden']
        center_name = json_data['center_name']
        area_name = json_data['area_name']
        center_remarks = json_data['center_remarks']
        if self.isLegal(center_name, area_name):
            models.Center.objects.create(
                center_name=center_name,
                area_name=area_name,
                center_remarks=center_remarks, center_status=0,
                center_creator=self.user_now_name,
                center_creator_iden=user_now_iden)
        return Response({'message': self.message, 'signal': self.signal})

    def isLegal(self, center_name, area_name):
        try:
            center = models.Center.objects.get(center_name=center_name, area_name=area_name)
        except models.Center.DoesNotExist:
            return True
        else:
            self.message = "中心名字和区域重复"
            self.signal = 1
            return False


class CenterUpdateView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "更新成功"
        self.signal = 0

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        id = json_data['id']

        # center_iden = json_data['center_iden']
        center_name = json_data['center_name']
        area_name = json_data['area_name']
        center_remarks = json_data['center_remarks']
        # center_creator = json_data['center_creator']
        if self.isLegal(center_name, area_name, id):
            try:
                models.Center.objects.filter(id=id).update(
                    center_name=center_name,
                    center_remarks=center_remarks)
            except:
                self.message = "更新失败"
                self.signal = 1
        return Response({'message': self.message, 'signal': self.signal})

    def isLegal(self, center_name, area_name, id):
        try:
            center = models.Center.objects.get(~Q(id=id), center_name=center_name, area_name=area_name)
        except models.Center.DoesNotExist:
            return True
        else:
            self.message = "中心名字和区域重复"
            self.signal = 1
            return False


class CenterStatusView(APIView):
    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))

        center_status = json_data['center_status']
        center_iden = json_data['center_iden']
        id = json_data["id"]
        # dpm_iden = json_data['dpm_iden']

        center = models.Center.objects.filter(id=id)

        if center:
            center.update(center_status=center_status)
            return Response({"message": "状态更改成功", "signal": 0})
        else:
            return Response({"message": "未查询到仓库,状态更改失败"})


"""

中心仓库维护接口
- 查看中心仓库情况
- 增加中心仓库
- 修改中心仓库信息

"""

# class CenterWareHousesView(APIView):
#
#     def get(self, request):
#         centerWareHouses = models.CenterWareHouse.objects.all()
#         if centerWareHouses:
#             centerWareHouses_serializer = CenterWareHouseSerializer(centerWareHouses, many=True)
#             return Response({"centerWareHouses": centerWareHouses_serializer.data})
#
#
# class CenterWareHouseNewView(APIView):
#     def get(self, request):
#         brands = models.Brand.objects.filter(brand_status=1).values_list('brand_name', flat=True)
#         organizations = {}
#         areas_name = models.Area.objects.filter(area_status=1).values_list('area_name', flat=True)
#         for area_name in areas_name:
#             orga_center = []
#             organization = models.Organization.objects.filter(area_name=area_name, orga_status=1).values_list(
#                 'orga_name', flat=True)
#             center = models.Center.objects.filter(area_name=area_name, center_status=1).values_list('center_name',
#                                                                                                     flat=True)
#             orga_center.append(organization)
#             orga_center.append(center)
#             organizations[area_name] = orga_center
#         return Response({"brands": brands, "organizations": organizations})
#
#
# class CenterWareHouseAddView(APIView):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.message = "添加成功"
#         self.signal = 0
#
#     def post(self, request):
#         json_data = json.loads(self.request.body.decode("utf-8"))
#         center_wh_iden = json_data['center_wh_iden']
#         center_wh_name = json_data['center_wh_name']
#         area_name = json_data['area_name']
#         orga_name = json_data['orga_name']
#         center_name = json_data['center_name']
#         brand_name = json_data['brand_name']
#         center_wh_remarks = json_data['center_wh_remarks']
#         center_wh_status = json_data['center_wh_status']
#         center_wh_creator = json_data['center_wh_creator']
#         organization = models.Organization.objects.get(area_name=area_name, orga_name=orga_name)
#         center = models.Center.objects.get(center_name=center_name)
#         models.CenterWareHouse.objects.create(center_wh_iden=center_wh_iden, center_wh_name=center_wh_name,
#                                               organization=organization, center=center,
#                                               brand_name=brand_name,
#                                               center_wh_remarks=center_wh_remarks, center_wh_status=center_wh_status,
#                                               center_wh_creator=center_wh_creator)
#         return Response({'message': self.message, 'signal': self.signal})
#
#
# class CenterWareHouseUpdateView(APIView):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.message = "更新成功"
#         self.signal = 0
#
#     def post(self, request):
#         json_data = json.loads(self.request.body.decode("utf-8"))
#         center_wh_iden = json_data['center_wh_iden']
#         center_wh_remarks = json_data['center_wh_remarks']
#         center_wh_status = json_data['center_wh_status']
#         # center_wh_creator = json_data['center_wh_creator']
#         try:
#             models.CenterWareHouse.objects.filter(center_wh_iden=center_wh_iden, ).update(
#                 center_wh_remarks=center_wh_remarks,
#                 center_wh_status=center_wh_status, )
#         except:
#             self.message = "更新失败"
#             self.signal = 1
#         return Response({'message': self.message, 'signal': self.signal})


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
        else:
            return Response({"message": "未查询到信息"})


class SupplierAddView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = "添加成功"
        self.signal = 0
        self.user_now_name = ""

    def post(self, request):
        json_data = json.loads(self.request.body.decode("utf-8"))
        user_now_iden = json_data['user_now_iden']
        user_now = models.UserNow.objects.get(user_iden=user_now_iden)
        if user_now:
            self.user_now_name = user_now.user_name
        supply_iden = json_data['supply_iden']
        supply_name = json_data['supply_name']
        supply_type = json_data['supply_type']
        supply_remarks = json_data['supply_remarks']
        models.Supplier.objects.create(supply_iden=supply_iden, supply_name=supply_name,
                                       supply_type=supply_type,
                                       supply_remarks=supply_remarks,
                                       supply_creator=self.user_now_name,
                                       supply_creator_iden=user_now_iden)
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
        # supply_status = json_data['supply_status']
        # supply_creator = json_data['supply_creator']
        try:
            models.Supplier.objects.filter(supply_iden=supply_iden).update(supply_name=supply_name,
                                                                           supply_type=supply_type,
                                                                           supply_remarks=supply_remarks)
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
        else:
            return Response({"message": "未查询到信息"})


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
        else:
            return Response({"message": "未查询到信息"})


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
        else:
            return Response({"message": "未查询到信息"})


class MaterialNewView(APIView):
    def get(self, request):
        """
        物料类别及其名字和最大流水号编码
        """
        material_types = models.MaterialType.objects.filter(type_status=1).values_list('type_iden', 'type_name')
        material_types = [list(material_type) for material_type in material_types]
        for i, material_type in enumerate(material_types):
            material_iden = \
                models.Material.objects.filter(material_type_iden=material_type[0]).aggregate(Max('material_iden'
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
