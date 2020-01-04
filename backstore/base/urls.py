from django.urls import path

from . import views

app_name = "base"
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('loginExit', views.LoginExitView.as_view(), name='loginExit'),
    path('user', views.UserView.as_view(), name='user'),
    path('userNew', views.UserNewView.as_view(), name='userNew'),
    path('userAdd', views.UserAddView.as_view(), name='userAdd'),
    path('userUpdate', views.UserUpdateView.as_view(), name='userUpdate'),
    path('userStatus', views.UserStatusView.as_view(), name='userStatus'),
    path('users', views.UsersView.as_view(), name='users'),

    path('areas', views.AreasView.as_view(), name='areas'),

    path('roles', views.RolesView.as_view(), name='roles'),
    path('roleAdd', views.RoleAddView.as_view(), name='roleAdd'),
    path('roleUpdate', views.RoleUpdateView.as_view(), name='roleUpdate'),
    path('roleStatus', views.RoleStatusView.as_view(), name='roleStatus'),



    path('customers', views.CustomersView.as_view(), name='customers'),
    path('customerAdd', views.CustomerAddView.as_view(), name='customerAdd'),
    path('customerUpdate', views.CustomerUpdateView.as_view(), name='customerUpdate'),
    path('customerStatus', views.CustomerStatusView.as_view(), name='customerStatus'),


    path('organizations', views.OrganizationsView.as_view(), name='organizations'),
    path('organizationNew', views.OrganizationNewView.as_view(), name='organizationNew'),
    path('organizationAdd', views.OrganizationAddView.as_view(), name='organizationAdd'),
    path('organizationUpdate', views.OrganizationUpdateView.as_view(), name='organizationUpdate'),
    path('organizationStatus', views.OrganizationStatusView.as_view(), name='organizationStatus'),


    path('brands', views.BrandsView.as_view(), name='brands'),
    path('brandAdd', views.BrandAddView.as_view(), name='brandAdd'),
    path('brandUpdate', views.BrandUpdateView.as_view(), name='brandUpdate'),

    path('totalWareHouses', views.TotalWareHousesView.as_view(), name='totalWareHouses'),
    path('totalWareHouseNew', views.TotalWareHouseNewView.as_view(), name='totalWareHouseNew'),
    path('totalWareHouseAdd', views.TotalWareHouseAddView.as_view(), name='totalWareHouseAdd'),
    path('totalWareHouseUpdate', views.TotalWareHouseUpdateView.as_view(), name='totalWareHouseUpdate'),

    path('centers', views.CentersView.as_view(), name='centers'),
    path('centerNew', views.CenterNewView.as_view(), name='centerNew'),
    path('centerAdd', views.CenterAddView.as_view(), name='centerAdd'),
    path('centerUpdate', views.CenterUpdateView.as_view(), name='centerUpdate'),

    # path('centerWareHouses', views.CenterWareHousesView.as_view(), name='centerWareHouses'),
    # path('centerWareHouseNew', views.CenterWareHouseNewView.as_view(), name='centerWareHouseNew'),
    # path('centerWareHouseAdd', views.CenterWareHouseAddView.as_view(), name='centerWareHouseAdd'),
    # path('centerWareHouseUpdate', views.CenterWareHouseUpdateView.as_view(), name='centerWareHouseUpdate'),

    path('suppliers', views.SuppliersView.as_view(), name='suppliers'),
    path('supplierAdd', views.SupplierAddView.as_view(), name='supplierAdd'),
    path('supplierUpdate', views.SupplierUpdateView.as_view(), name='supplierUpdate'),

    path('meterages', views.MeteragesView.as_view(), name='meterages'),
    path('meterageAdd', views.MeterageAddView.as_view(), name='meterageAdd'),
    path('meterageUpdate', views.MeterageUpdateView.as_view(), name='meterageUpdate'),

    path('materialTypes', views.MaterialTypesView.as_view(), name='materialTypes'),
    path('materialTypeAdd', views.MaterialTypeAddView.as_view(), name='materialTypeAdd'),
    path('materialTypeUpdate', views.MaterialTypeUpdateView.as_view(), name='materialTypeUpdate'),

    path('materials', views.MaterialsView.as_view(), name='materials'),
    path('materialNew', views.MaterialNewView.as_view(), name='materialNew'),
    path('materialAdd', views.MaterialAddView.as_view(), name='materialAdd'),
    path('materialUpdate', views.MaterialUpdateView.as_view(), name='materialUpdate'),



    # path('area',)
]
