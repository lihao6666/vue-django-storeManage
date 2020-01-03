import axios from 'axios' // 引用axios
import {MessageBox, Message} from 'element-ui'
import Qs from 'qs' // 引入数据格式化
import router from '@/router'
// axios 配置
axios.defaults.timeout = 50000 // 设置接口响应时间
// axios.defaults.baseURL = 'https://easy-mock.com/mock/' // 这是调用数据接口,公共接口url+调用接口名
let httpUrl = window.location.host
if (httpUrl.indexOf('.com') !== -1) {
  console.log('生产环境', httpUrl)
} else if (httpUrl.indexOf('.net') !== -1) {
  console.log('测试环境', httpUrl)
  axios.defaults.baseURL = 'http://www.test.com' // 这是调用数据接口,公共接口url+调用接口名
} else if (httpUrl.indexOf('localhost:8088') !== -1) {
  console.log('指定开发环境', httpUrl)
  axios.defaults.baseURL = 'http://localhost:8088/'
} else {
  console.log('开发环境', httpUrl)
  axios.defaults.baseURL = 'http://localhost:8090/' // 这是调用数据接口,公共接口url+调用接口名
}
axios.defaults.withCredentials = true

// http request 拦截器，通过这个，我们就可以把Cookie传到后台
axios.interceptors.request.use(
  config => {
    console.log('请求路径', config.url)
    if (config.url === '/b/login/checkLogin') {
      config.headers = {
        'Content-Type': 'application/x-www-form-urlencoded' // 设置跨域头部
      }
      config.data = Qs.stringify(config.data)
    } else if (config.url === '/b/carModel/createCarModelVersion') {
      // 此处设置文件上传，配置单独请求头
      config.headers = {
        'Content-Type': 'multipart/form-data'
      }
    } else {
      let username = localStorage.getItem('ms_username')
      if (username === null) {
        return null
      }
      let bToken = localStorage.getItem('btoken')
      if (bToken === null) {
      } else {
        config.data.vwToken = bToken
      }
      config.headers = {
        'Content-Type': 'application/x-www-form-urlencoded' // 设置跨域头部
      }
      config.data = Qs.stringify(config.data)
    }
    return config
  },
  err => {
    return Promise.reject(err)
  }
)
// http response 拦截器
axios.interceptors.response.use(
  response => {
    // console.log('请求拦截返回参数', response)
    if (response.status === 200) {
      // 成功
      let returnCode = response.data.code
      if (returnCode > 10000 && returnCode < 20000) {
        // console.log('成功', response)
        Message.success(response.data.msg)
      } else if (returnCode >= 20000 && returnCode < 30000) {
        // 只弹窗，不操作
        // console.log('失败1', response)
        Message.error(response.data.msg)
      } else if (returnCode >= 30000 && returnCode < 40000) {
        // 只弹窗，点击跳到登入页
        localStorage.removeItem('ms_username')
        MessageBox.confirm(response.data.msg, '确定登出', {
          confirmButtonText: '重新登录',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          // console.log('此处应退出登录  重新实例化')
          router.push({path: '/login'})
        })
      }
    }
    return response
  },
  error => {
    // console.log('error', error.toString())
    if (
      error.toString().trim() ===
      "TypeError: Cannot read property 'cancelToken' of null"
    ) {
      localStorage.removeItem('ms_username')
      MessageBox.confirm(
        '会话凭证失效，可以取消继续留在该页面，或者重新登录',
        '确定登出',
        {
          confirmButtonText: '重新登录',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        //  console.log('此处应退出登录  重新实例化')
        router.push({path: '/login'})
      })
    }
    // console.log(error.toString().trim())
    if (error.toString().trim() === 'Error: Network Error') {
      MessageBox.alert('网络请求异常，请稍后重试', '出错了', {
        confirmButtonText: '确定',
        callback: action => {
        }
      })
    }
    return Promise.reject(error.response.data)
  }
)
export default axios
