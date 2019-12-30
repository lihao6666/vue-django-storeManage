const Mock = require('mockjs')

Mock.mock('/req_pur_check', 'post', require('./json/req_pur_check'))
Mock.mock('/req_pur_prd', 'post', require('./json/req_pur_prd'))
Mock.mock('/req_pur_prd_add', 'post', require('./json/req_pur_prd_add'))

Mock.mock('/so_check', 'post', require('./json/so_check'))
Mock.mock('/so_sod', 'post', require('./json/so_sod'))
Mock.mock('/so_sod_add', 'post', require('./json/so_sod_add'))

Mock.mock('/pc_check', 'post', require('./json/pc_check'))
Mock.mock('/pc_cd', 'post', require('./json/pc_cd'))
Mock.mock('/pc_pay', 'post', require('./json/pc_pay'))

Mock.mock('/test2', 'post', require('./json/test2'))
Mock.mock('/basic_data', 'post', require('./json/basic_data'))
