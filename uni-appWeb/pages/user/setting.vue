<template>
	<view class="content">
		<view class="btn-row">
			<button class="exit" type="default" @tap="bindLogout">退出登录</button>
		</view>
	</view>
</template>

<script>
	import {
	    mapState,
	    mapMutations
	} from 'vuex'
	export default {
	    computed: {
	        ...mapState(['hasLogin', 'forcedLogin'])
	    },
	    methods: {
	        ...mapMutations(['logout']),
	        bindLogout() {
				uni.showModal({
				    title: '提示',
				    content: '确认退出登录?',
				    success: function (res) {
				        if (res.confirm) {
				            uni.reLaunch({
				                url: '../login/login',
				            });
				        } else if (res.cancel) {
				            console.log('用户点击取消');
				        }
				    }
				});
	        },
		},
	}
</script>

<style>
	.exit {
		background-color: rgb(255,60,60);
		font-weight: 500;
	}
</style>
