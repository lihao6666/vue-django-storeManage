const Mock = require('mockjs')

Mock.mock('/req_pur_check', 'post', require('./json/req_pur_check'))
Mock.mock('/req_pur_prd', 'post', require('./json/req_pur_prd'))
