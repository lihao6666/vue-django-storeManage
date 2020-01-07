<template>
	<view class="content">
		<view class="btn-row">
			<wButton
				text="退 出 登 录"
				@click.native="logout()"
			></wButton>
		</view>
	</view>
</template>

<script>
	import wButton from '../../components/watch-login/watch-button.vue'
	var _this
	export default {
		components:{
			wButton
		},
		mounted() {
			_this = this;
		},
	    methods: {
	        logout() {
				var myinfo = uni.getStorageSync('user_info')
				var user_now_iden = myinfo.data.user.username
				uni.showModal({
				    title: '提示',
				    content: '确认退出登录?',
				    success: function (choose) {
				        if (choose.confirm) {
				            _this.$http.post('/base/loginExit', {user_now_iden}).then(([err,res]) => {
								uni.removeStorageSync('user_info')
				            	uni.reLaunch({
				            	    url: '../login/login',
				            	});
								
								//TODO 提示信息只能在该页面显示，想办法放在下个页面显示
								// if (res.data.signal === '0') {
								// 	uni.showToast({
								// 		icon: 'none',
								// 		position: 'bottom',
								// 		title: res.data.message
								// 	});
								// } else {
								//     uni.showToast({
								//     	icon: 'none',
								//     	position: 'bottom',
								//     	title: '您的账号未登录'
								//     });
								// }
				            })
				        } else if (choose.cancel) {
				            uni.showToast({
							    icon: 'none',
							    position: 'bottom',
							    title: '取消退出'
						    });
				        }
				    }
				});
	        },
		},
	}
</script>

<style>
</style>
