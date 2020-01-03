// 导入封装好的axios实例
import axios from './request'

const http = {
  /**
   * methods: 请求
   * @param url 请求地址
   * @param params 请求参数
   */
  get (url, params) {
    const config = {
      methods: 'get',
      url: url
    }
    if (params) config.params = params
    return axios(config)
  },
  post (url, params) {
    const config = {
      methods: 'post',
      url: url
    }
    if (params) config.data = params
    return axios(config)
  },
  put (url, params) {
    const config = {
      methods: 'put',
      url: url
    }
    if (params) config.params = params
    return axios(config)
  },
  delete (url, params) {
    const config = {
      methods: 'delete',
      url: url
    }
    if (params) config.params = params
    return axios(config)
  }
}
// 导出
export default http
