import config from "./config.js";

export default {
	config: {
		baseUrl: config.webUrl,
		header: {
			'Content-Type' : 'application/json;charset=UTF-8'
		},
		data: {},
		method: "POST",
		dataType: "json",
	},
	request(options={}) {
		options.header = options.header || this.config.header;
		options.method = options.method || this.config.method;
		options.dataType = options.dataType || this.config.dataType;
		options.url = this.config.baseUrl+options.url;
		//TODO: token等操作
		// if(options.token) {
		// 	if(options.checkToken && !User.token) {
		// 		uni.showToast({ title: '您未登录', icon:"none" })
		// 		return uni.navigateTo({
		// 			url: '/pages/login/login'
		// 		});
		// 	}
		// 	options.header.token = User.token;
		// }
		
		return uni.request(options);
	},
	get(url, data, options={}){
		options.url = url;
		options.data = data;
		options.method = 'GET';
		return this.request(options);
	},
	post(url, data, options={}){
		options.url = url;
		options.data = data;
		options.method = 'POST';
		return this.request(options);
	}
}