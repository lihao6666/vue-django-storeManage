<template>
	<view class="content">
<!-- 		<view v-for="item in detailList" :key="item.id" class="card-set"> -->
		
		<view class="material">
			<text class="material-title">物料编号</text>
			<text class="material-input">
				{{ material_iden }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">物料名称</text>
			<text class="material-input">
				{{ material_name }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">仓库编号</text>
			<text class="material-input">
				{{ total_iden }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">仓库名称</text>
			<text class="material-input">
				{{ total_name }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">库存组织编号</text>
			<text class="material-input">
				{{ orga_iden }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">库存组织名称</text>
			<text class="material-input">
				{{ orga_name }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">物料规格</text>
			<text class="material-input">
				{{ material_specification }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">物料类型</text>
			<text class="material-input">
				{{ material_model }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">物料单位</text>
			<text class="material-input">
				{{ material_meterage }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">现存量</text>
			<text class="material-input">
				{{ ts_present_num }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">现存单价</text>
			<text class="material-input">
				{{ ts_present_price }}
			</text>
		</view>
		<view class="material">
			<text class="material-title">现存总价</text>
			<text class="material-input">
				{{ ts_present_sum }}
			</text>
		</view>		
		<view class="address-add-btn" @click="apply">前往申领</view>
	</view>
</template>

<script>
	// import detailData from '../../data/English.js'
	var _this;
export default {
	data() {
		return {
			material_iden: '',
			material_name: '',
			total_iden: '',
			total_name: '',
			orga_iden: '',
			orga_name: '',
			material_specification: '',
			material_model: '',
			material_meterage: '',
			ts_present_num: '',
			ts_present_price: '',
			ts_present_sum: ''
		}
	},
	mounted() {
		_this = this
	},
	methods: {
		apply:function(e){
			uni.removeStorageSync('details')
			uni.switchTab({
				url: '../index/index',
			});	
		},
	},
	onLoad: function() {
		var  item= uni.getStorageSync('details')
		this.material_iden = item.material_iden
		this.material_name = item.material_name
		this.total_iden = item.total_iden
		this.total_name = item.total_name
		this.orga_iden = item.orga_iden
		this.orga_name = item.orga_name
		this.material_specification = item.material_specification
		this.material_model = item.material_model
		this.material_meterage = item.material_meterage
		this.ts_present_num = item.ts_present_num
		this.ts_present_price = item.ts_present_price
		this.ts_present_sum = item.ts_present_sum
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
		height: 92upx;
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