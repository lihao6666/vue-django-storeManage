<template>
	<view class="content">
		<!-- 头部logo -->
		<!-- <view class="header">
			<image :src="logoImage"></image>
		</view> -->
		<!-- 主体表单 -->
		<view class="main">
			<wInput
				v-model="loginData.user_iden"
				type="text"
				maxlength="20"
				placeholder="用户名"
			></wInput>
			<wInput
				v-model="loginData.user_passwd"
				type="password"
				maxlength="20"
				placeholder="密码"
			></wInput>
		</view>
		<wButton 
			text="登 录"
			:rotate="isRotate" 
			@click.native="startLogin()"
		></wButton>
	</view>
</template>

<script>
	import wInput from '../../components/watch-login/watch-input.vue' //input
	import wButton from '../../components/watch-login/watch-button.vue' //button
	import myAccunt from '../../data/accunt.js'
	var _this;
	
	export default {
		data() {
			return {
				//logo图片 base64
				loginData: {
					user_iden: '', //用户/电话
					user_passwd: '', //密码
				},
				isRotate: false, //是否加载旋转
				mydata: myAccunt.data
			};
		},
		components:{
			wInput,
			wButton,
		},
		mounted() {
			_this = this;
			this.isLogin();
		},
		methods: {
		    startLogin(){
				//登录
				if(this.isRotate){
					//判断是否加载中，避免重复点击请求
					return false;
				}
				_this.isRotate=true
				setTimeout(function(){
					_this.isRotate=false
				},1200)

				//请求登录
				this.$http.post('/base/login', _this.loginData).then(([err,res]) => {
					if (res.data.signal === '0') {
						uni.setStorageSync('user_info', res)
						setTimeout(function(){
							uni.showToast({
								icon: 'none',
								position: 'bottom',
								title: res.data.message
							});
							uni.switchTab({
								url: '../main/main'
							})
						},1200)
				    } else {
					    setTimeout(function(){
					    	uni.showToast({
					    		icon: 'none',
					    		position: 'bottom',
					    		title: res.data.message
					    	});
					    },1200)
				    }
				})
		    },
			isLogin() {
				if(uni.getStorageSync('user_now_iden')) {
					uni.showToast({
						icon: 'none',
						position: 'bottom',
						title: '您已登录'
					});
					uni.switchTab({
						url: '../main/main'
					})
				}
			}
		},
	}
</script>

<style>
	@import url("../../components/watch-login/css/icon.css");
	@import url("./css/main.css");
	.content {
		padding: 0;
	}
	.main {
		margin-top: 70upx;
	}
</style>
