<template>
	<view class="content">
		<view class="content-content">
			<view v-for="item in detailList" :key="item.id" class="card-set">
				<uni-card
					:title="item.msod_name"
					mode="basic" 
					:is-shadow="true" 
					:extra="item.msod_iden"
				>
					<view>
						<view>出库数量：{{ item.msod_num }}</view>
						<view>现存量：{{ item.msod_present_num }}</view>
						<view>规格：{{ item.msod_specification }}</view>
						<view>型号：{{ item.msod_model }}</view>
						<view>单位：{{ item.msod_meterage }}</view>
						<view>备注：{{ item.msod_remarks }}</view>
					</view>
				</uni-card>
			</view>
		</view>
	</view>
</template>

<script>
import uniCard from '../../components/uni-card/uni-card.vue'
import detailData from '../../data/outDetails.js'


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
