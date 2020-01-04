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
	export default {
		components:{
			wButton
		},
	    methods: {
	        logout() {
				uni.showModal({
				    title: '提示',
				    content: '确认退出登录?',
				    success: function (res) {
				        if (res.confirm) {
				            uni.reLaunch({
				                url: '../login/login',
				            });
				        } else if (res.cancel) {
				            console.log('取消');
				        }
				    }
				});
	        },
		},
	}
</script>

<style>
</style>
