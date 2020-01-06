import axios from 'axios'
import {Message, Loading} from 'element-ui'
// import qs from 'qs'
// import router from '@/router'
// import {Message, MessageBox} from 'element-ui'

axios.defaults.timeout = 50000 // 设置接口响应时间
// axios.defaults.baseURL = 'https://easy-mock.com/mock/' // 这是调用数据接口,公共接口url+调用接口名
let httpUrl = window.location.host
if (httpUrl.indexOf('.com') !== -1) {
  console.log('生产环境', httpUrl)
} else if (httpUrl.indexOf('.net') !== -1) {
  console.log('测试环境', httpUrl)
  axios.defaults.baseURL = 'http://www.test.com' // 这是调用数据接口,公共接口url+调用接口名
} else if (httpUrl.indexOf('localhost:8080') !== -1) {
  console.log('指定开发环境', httpUrl)
  axios.defaults.baseURL = 'http://49.234.123.211:8000/'
} else {
  console.log('开发环境', httpUrl)
  axios.defaults.baseURL = 'http://49.234.123.211:8000/' // 这是调用数据接口,公共接口url+调用接口名
}

let loading
function startLoading () {
  loading = Loading.service({
    lock: true,
    text: '加载中……',
    background: 'rgba(0, 0, 0, 0.7)'
  })
}
function endLoading () {
  loading.close()
}

let needLoadingRequestCount = 0
export function showFullScreenLoading () {
  if (needLoadingRequestCount === 0) {
    startLoading()
  }
  needLoadingRequestCount++
}
export function tryHideFullScreenLoading () {
  if (needLoadingRequestCount <= 0) return
  needLoadingRequestCount--
  if (needLoadingRequestCount === 0) {
    endLoading()
  }
}

axios.interceptors.request.use(config => {
  if (config.method === 'post') {
    let username = localStorage.getItem('user_now_iden')
    if (username !== null) {
      config.data.user_now_iden = username
    }
  }
  // Vue.$vux.loading.show({
  //   text: 'Loading'
  // })
  showFullScreenLoading()
  console.log(config)
  // let bToken = localStorage.getItem('btoken')
  // if (bToken === null) {
  // } else {
  //   config.data.vwToken = bToken
  // }
  // config.headers = {
  //   'Content-Type': 'application/x-www-form-urlencoded' // 设置跨域头部
  // }
  // config.data = qs.stringify(config.data)
  return config
}, error => {
  tryHideFullScreenLoading()
  Message.error('加载失败')
  return Promise.reject(error)
})

axios.interceptors.response.use(response => {
  // if (response.status === 200) {
  //   // 成功
  //   let returnCode = response.data.code
  //   if (returnCode > 10000 && returnCode < 20000) {
  //     // console.log('成功', response)
  //     Message.success(response.data.msg)
  //   } else if (returnCode >= 20000 && returnCode < 30000) {
  //     // 只弹窗，不操作
  //     // console.log('失败1', response)
  //     Message.error(response.data.msg)
  //   } else if (returnCode >= 30000 && returnCode < 40000) {
  //     // 只弹窗，点击跳到登入页
  //     localStorage.removeItem('user_now_iden')
  //     MessageBox.confirm(response.data.msg, '确定登出', {
  //       confirmButtonText: '重新登录',
  //       cancelButtonText: '取消',
  //       type: 'warning'
  //     }).then(() => {
  //       // console.log('此处应退出登录  重新实例化')
  //       router.push({path: '/login'})
  //     })
  //   }
  // }
  // Vue.$vux.loading.hide()
  tryHideFullScreenLoading()
  return response
}, error => {
  tryHideFullScreenLoading()
  Message.error('加载失败')
  return Promise.resolve(error.response)
})

// get请求
export function getAPI (url, params = null) {
  return axios({
    method: 'get',
    url,
    params, // get 请求时带的参数
    timeout: 10000,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
}

// post请求
export function postAPI (url, params = null) {
  return axios({
    method: 'post',
    url,
    data: params,
    timeout: 10000,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
  })
}
