<template>
	<view class="content">
		<view class="content-content">
			<view v-for="item in computeMoney" :key="item.id" class="card-set">
				<uni-card
					:title="item.sod_name"
					mode="basic" 
					:is-shadow="true" 
					:extra="item.sod_iden"
				>
					<view>
						<view>请购数量：{{ item.sod_num }}</view>
						<view>规格：{{ item.sod_specification }}</view>
						<view>型号：{{ item.sod_model }}</view>
						<view>单位：{{ item.sod_meterage }}</view>
						<view>税率：{{ item.sod_taxRate }}</view>
						<view>含税单价：{{ item.sod_tax_unitPrice }}</view>
						<view>无税单价：{{ item.sod_unitPrice }}</view>
						<view>含税金额：{{ item.sod_tax_sum }}</view>
						<view>无税金额：{{ item.sod_sum }}</view>
						<view>税额：{{ item.sod_tax_price }}</view>
						<view>备注：{{ item.sod_remarks }}</view>
					</view>
				</uni-card>
			</view>
		</view>
	</view>
</template>

<script>
import uniCard from '../../components/uni-card/uni-card.vue'
import detailData from '../../data/sellDetails.js'


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
	computed: {
		computeMoney () {
			var arr = []
			this.detailList.forEach((item) => {
				var unitPrice = item.sod_tax_unitPrice/(1+item.sod_taxRate/100)
				var tax_sum = item.sod_tax_unitPrice*item.sod_num
				var sum = item.sod_tax_unitPrice*item.sod_num/(1+item.sod_taxRate/100)
				var tax_price = item.sod_tax_unitPrice*item.sod_num*(item.sod_taxRate/100)/(1+item.sod_taxRate/100)
				item.sod_unitPrice = unitPrice.toFixed(2)
				item.sod_tax_sum = tax_sum.toFixed(2)
				item.sod_sum = sum.toFixed(2)
				item.sod_tax_price = tax_price.toFixed(2)
				arr.push(item)
			})
			
			return arr
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
