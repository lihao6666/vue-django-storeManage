const Mock = require('mockjs')

Mock.mock('/test', 'get', require('./json/test'))
