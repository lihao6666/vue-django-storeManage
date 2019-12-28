const Mock = require('mockjs')

Mock.mock('/req_pur_check', 'post', require('./json/req_pur_check'))
Mock.mock('/req_pur_prd', 'post', require('./json/req_pur_prd'))

Mock.mock('/so_check', 'post', require('./json/so_check'))
Mock.mock('/so_sod', 'post', require('./json/so_sod'))

Mock.mock('/test2', 'post', require('./json/test2'))
