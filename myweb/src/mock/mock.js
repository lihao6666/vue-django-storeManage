const Mock = require('mockjs')

Mock.mock('/test', 'post', require('./json/test'))
