<template>
	<view></view>
</template>

<script>
	export default {
		components: {
			
		},
		data() {
			return {
				//将data文件夹中的数据读入
				order_iden: '',
			}
		},
		methods: {
			
		},
		onLoad: function() {
			var myinfo = uni.getStorageSync('viewsell');
			this.order_iden = myinfo;
		}
	}
</script>

<style>
</style>
