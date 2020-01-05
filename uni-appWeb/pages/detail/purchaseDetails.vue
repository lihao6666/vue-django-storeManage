<template>
	<view class="content">
		<view class="content-content">
			<view v-for="item in detailList" :key="item.id" class="card-set">
				<uni-card
					:title="item.prd_name"
					mode="basic" 
					:is-shadow="true" 
					:extra="item.prd_iden"
				>
					<view>
						<view>请购数量：{{ item.prd_num }}</view>
						<view>现存量：{{ item.prd_present_num }}</view>
						<view>规格：{{ item.prd_specification }}</view>
						<view>型号：{{ item.prd_model }}</view>
						<view>单位：{{ item.prd_meterage }}</view>
						<view>备注：{{ item.prd_remarks }}</view>
					</view>
				</uni-card>
			</view>
		</view>
	</view>
</template>

<script>
import uniCard from '../../components/uni-card/uni-card.vue'
import detailData from '../../data/purchaseDetails.js'


export default {
	components: {
		uniCard
	},
	data() {
		return {
			//将data文件夹中的数据读入
			order_iden: '',
			detailList: detailData.data
		}
	},
	methods: {
		
	},
	onLoad: function() {
		var myinfo = uni.getStorageSync('viewpurchase');
		this.order_iden = myinfo;
	}
}
</script>

<style>
	page {
		display: flex;
		flex-direction: column;
		box-sizing: border-box;
		background-color: #efeff4;
		min-height: 100%;
		height: auto;
	}
	
	view {
		font-size: 28upx;
		line-height: inherit;
	}
	.content {
		padding: 0;
	}
	.content-content {
		justify-content: center;
		align-items: center;
		text-align: left;
	}
</style>
