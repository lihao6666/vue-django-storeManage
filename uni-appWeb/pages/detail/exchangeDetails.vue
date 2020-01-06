<template>
	<view class="content">
		<view class="content-content">
			<view v-for="item in detailList" :key="item.id" class="card-set">
				<uni-card
					:title="item.trd_name"
					mode="basic" 
					:is-shadow="true" 
					:extra="item.trd_iden"
				>
					<view>
						<view>申请数量：{{ item.trd_num }}</view>
						<view>现存量：{{ item.trd_present_num }}</view>
						<view>规格：{{ item.trd_specification }}</view>
						<view>型号：{{ item.trd_model }}</view>
						<view>单位：{{ item.trd_meterage }}</view>
						<view>备注：{{ item.trd_remarks }}</view>
					</view>
				</uni-card>
			</view>
		</view>
	</view>
</template>

<script>
import uniCard from '../../components/uni-card/uni-card.vue'
import detailData from '../../data/exchangeDetails.js'


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
		var myinfo = uni.getStorageSync('viewexchange');
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
