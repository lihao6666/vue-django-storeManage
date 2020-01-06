import Vue from 'vue'
import App from './App'

import store from './store'

import config from './common/config.js'
Vue.prototype.config = config

import request from './common/request.js'
Vue.prototype.$http = request

Vue.config.productionTip = false

Vue.prototype.$store = store

//检查登录函数
//参数:backpage:登录后返回的页面 backtype:返回类型(一般传switchTab,因为需要返回下方Tab的位置,也可选择其他方式)
Vue.prototype.checkLogin = function(backpage, backtype) {
	var uid = uni.getStorageSync('user_id')
	if(uid === ''){ //如果用户工号为空,则返回登录界面
		uni.redirectTo({
			url: "/pages/login/login?backpage=" + backpage + "&backtype=" + backtype
		});
		return false;
	}
	return uid;
}

App.mpType = 'app'

const app = new Vue({
    store,
    ...App
})
app.$mount()
