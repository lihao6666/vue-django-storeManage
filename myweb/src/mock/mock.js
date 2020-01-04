const Mock = require('mockjs')

Mock.mock('/base/login', 'post', require('./json/login'))

Mock.mock('/req_pur_check', 'post', require('./json/req_pur_check'))
Mock.mock('/req_pur_prd', 'post', require('./json/req_pur_prd'))
Mock.mock('/req_pur_prd_add', 'post', require('./json/req_pur_prd_add'))

Mock.mock('/so_check', 'post', require('./json/so_check'))
Mock.mock('/so_sod', 'post', require('./json/so_sod'))
Mock.mock('/so_sod_add', 'post', require('./json/so_sod_add'))

Mock.mock('/pc_check', 'post', require('./json/pc_check'))
Mock.mock('/pc_cd', 'post', require('./json/pc_cd'))
Mock.mock('/pc_pay', 'post', require('./json/pc_pay'))
Mock.mock('/pc_cd_add', 'post', require('./json/pc_cd_add'))

Mock.mock('/po_check', 'post', require('./json/po_check'))
Mock.mock('/po_od', 'post', require('./json/po_od'))
Mock.mock('/po_od_add_rp', 'post', require('./json/po_od_add_rp'))
Mock.mock('/po_od_add_pc', 'post', require('./json/po_od_add_pc'))

Mock.mock('/bis_check', 'post', require('./json/bis_check'))
Mock.mock('/bis_bd', 'post', require('./json/bis_bd'))
Mock.mock('/bis_bd_add', 'post', require('./json/bis_bd_add'))

Mock.mock('/base/departments', 'post', require('./json/department'))

Mock.mock('/base/users', 'get', require('./json/users'))

Mock.mock('/base/roles', 'get', require('./json/role'))
Mock.mock('/base/roleAdd', 'post', require('./json/role'))
Mock.mock('/base/roleUpdate', 'post', require('./json/role'))

Mock.mock('/organization', 'post', require('./json/organization'))

Mock.mock('/area', 'post', require('./json/area'))
Mock.mock('/base/areas', 'post', require('./json/area'))

Mock.mock('/center', 'post', require('./json/center'))
Mock.mock('/brand', 'post', require('./json/brand'))
Mock.mock('/warehouse', 'post', require('./json/warehouse'))
Mock.mock('/store', 'post', require('./json/store'))
Mock.mock('/supplier', 'post', require('./json/supplier'))
Mock.mock('/customer', 'post', require('./json/customer'))
Mock.mock('/meterage', 'post', require('./json/meterage'))
Mock.mock('/material_type', 'post', require('./json/material_type'))
Mock.mock('/material', 'post', require('./json/material'))

Mock.mock('/stock_check', 'post', require('./json/stock_check'))
Mock.mock('/str_check', 'post', require('./json/str_check'))
Mock.mock('/tr_detail', 'post', require('./json/tr_detail'))
Mock.mock('/str_detail_add', 'post', require('./json/str_detail_add'))
