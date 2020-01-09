<template>
	<view class="content">
		<uni-nav-bar :fixed="true" background-color="#20a0ff" :border="false">
			<view class="input-view">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="detailFilterText" confirm-type="search" class="input" type="text" placeholder="输入物料信息">
				<uni-icons :color="'#999999'" v-if="detailFilterText!==''" type="clear" size="22" @click="clear" />
			</view>
		</uni-nav-bar>
		<view class="content-content">
			<view v-for="(item,index) in detailFilterList" :key="index" class="card-set">
				<uni-card
					:title="item.sod_name"
					mode="basic" 
					:is-shadow="true" 
					:extra="item.sod_iden"
				>
					<view>
						<view>数量：{{ item.sod_num }}</view>
						<view>现存量: {{ item.present_num }}</view>
						<view>规格：{{ item.sod_specification }}</view>
						<view>型号：{{ item.sod_model }}</view>
						<view>单位：{{ item.sod_meterage }}</view>
						<view>税率：{{ item.sod_taxRate }}%</view>
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
import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue'
import uniIcons from '@/components/uni-icons/uni-icons.vue'


export default {
	components: {
		uniCard,
		uniNavBar,
		uniIcons
	},
	data() {
		return {
			//将data文件夹中的数据读入
			order_iden: '',
			detailList: detailData.data,
			// detailList: [],
			detailFilterText: ''
		}
	},
	computed: {
		detailFilterList () {
			let arr = []
			this.detailList.forEach((item) => arr.push(item))
			if (this.detailFilterText) {
				arr = this.detailList.filter(item => item.sod_name.includes(this.detailFilterText)||
					item.sod_iden.includes(this.detailFilterText)||
					item.sod_remarks.includes(this.detailFilterText)||
					item.sod_specification.includes(this.detailFilterText)||
					item.sod_model.includes(this.detailFilterText)
				)
			}
			return arr
		}
	},
	methods: {
		clear() {
			this.detailFilterText = ''
		},
		computeMoney() {
			let arr = []
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
			this.detailList = arr
			return
		}
	},
	onLoad: function() {
		let _this = this
		let myinfo = uni.getStorageSync('user_info')
		let so_info = uni.getStorageSync('order_info')
		uni.removeStorageSync('order_info')
		let msg = {}
		msg.so_iden = so_info.iden
		msg.orga_name = so_info.orga
		msg.user_now_iden = myinfo.data.user.username
		this.$http.post('/sell/sellOrderNew', msg).then(([err,res]) => {
			if (res.data.signal === 1) {
				_this.detailList = res.data.sods
				for(let i=0; i<_this.detailList.length; i++) {
					_this.detailList[i].present_num = res.data.sods_present_num[i]
				}
		    } else {
				
		    }
		})
		this.computeMoney()
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
	.input-view {
		align-items: center;
		justify-content: center;
		width: 100%;
		display: flex;
		background-color: #e7e7e7;
		height: 30px;
		border-radius: 15px;
		padding: 0 4%;
		flex-wrap: nowrap;
		margin: 7px 10rpx;
		line-height: 30px;
		background: #f5f5f5;
	}
	.input-view .input {
		height: 30px;
		line-height: 30px;
		width: 94%;
		padding: 0 3%;
	}
</style>
