<template>
	<view class="content">
		<uni-nav-bar :fixed="true" background-color="#20a0ff" :border="false">
			<view class="input-view">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="detailFilterText" confirm-type="search" class="input" type="text" placeholder="输入销售订单信息">
				<uni-icons :color="'#999999'" v-if="detailFilterText!==''" type="clear" size="22" @click="clear" />
			</view>
		</uni-nav-bar>
		<view class="content-content">
			<view v-for="(item,index) in detailFilterList" :key="index" class="card-set">
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
			detailFilterText: ''
		}
	},
	computed: {
		detailFilterList () {
			let arr = []
			this.detailList.forEach((item) => arr.push(item))
			if (this.detailFilterText) {
				arr = this.detailList.filter(item => item.msod_name.includes(this.detailFilterText)||
					item.msod_iden.includes(this.detailFilterText)||
					item.msod_remarks.includes(this.detailFilterText)||
					item.msod_specification.includes(this.detailFilterText)||
					item.msod_model.includes(this.detailFilterText)
				)
			}
			return arr
		}
	},
	methods: {
		clear() {
			this.detailFilterText = ''
		},
	},
	onLoad: function() {
		// let _this = this
		// let myinfo = uni.getStorageSync('user_info')
		// let mso_info = uni.getStorageSync('order_info')
		// uni.removeStorageSync('order_info')
		// let msg = {}
		// msg.mso_iden = mso_info.iden
		// msg.orga_name = mso_info.orga
		// msg.user_now_iden = myinfo.data.user.username
		// this.$http.post('/out/msoNew', msg).then(([err,res]) => {
		// 	if (res.data.signal === 1) {
		// 		_this.detailList = res.data.prds
		//     } else {
				
		//     }
		// })
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
