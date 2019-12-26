import axios from 'axios'
export const HOST = {
  MAIN: '', // 主服务的 host
  EXAMPLE: '' // 样例服务的 host
}

const http = axios.create({
  baseURL: HOST.EXAMPLE || '../../public/requisition.json',
  timeout: 5000
})
const dataHandler = data => {
  // 可以在这里添加一些数据处理。
  return data
}

export default {
  get (page, callback) {
    http.request({
      method: 'GET',
      params: {
        page: page
      }
    }).then(response => {
      const result = response.data.data.map(item => dataHandler(item));
      // 因为 axios 的请求是异步请求，所以在这里使用了回调函数。
      callback(result)
    })
  },
  post () {},
  put () {},
  delete () {}
}
