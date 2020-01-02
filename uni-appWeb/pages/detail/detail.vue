<template>
	<view class="content">
		<view class="material">
			<text class="material-title">物料名称</text>
			<text class="material-input">
				1
			</text>
		</view>
		<view class="material">
			<text class="material-title">物料编码</text>
			<text class="material-input">
				2
			</text>
		</view>
		<view class="material">
			<text class="material-title">规格</text>
			<text class="material-input">
				3
			</text>
		</view>
		<view class="material">
			<text class="material-title">型号</text>
			<text class="material-input">
				4
			</text>
		</view>
		<view class="material">
			<text class="material-title">计量单位</text>
			<text class="material-input">
				5
			</text>
		</view>
		<view class="material">
			<text class="material-title">存货属性</text>
			<text class="material-input">
				6
			</text>
		</view>
		<view class="material">
			<text class="material-title">物料状态</text>
			<text class="material-input">
				7
			</text>
		</view>
		<view class="address-add-btn" @tap="apply">前往申领</view>
    </view>
</template>

<script>
export default {
	methods: {
		apply:function(e){
			uni.navigateTo({
				url: '../reg/reg',
				success: res => {},
				fail: () => {},
				complete: () => {}
			});	
		}
	},
}
</script>

<style lang="scss">
	page {
		background-color: #F8F8F8;
	}
	.material {
		display: flex;
		align-items: center;
		position: relative;
		padding: 0 30upx;
		height: 100upx;
		background: #fff;
		border-bottom:1upx solid #F8F8F8;
	
		.material-title {
			flex-shrink: 0;
			width: 200upx;
			font-size: 32upx;
			color: black;
		}
		.material-input {
			flex: 1;
			font-size: 32upx;
			color: black;
		}	
	}
	.address-add-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 690upx;
		height: 80upx;
		margin: 10rpx;
		font-size: 32upx;
		color: #fff;
		background-color: #DD524D;
		border-radius: 10upx;
	}
</style>
