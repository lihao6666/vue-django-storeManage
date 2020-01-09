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
			detailList: [],
			detailFilterText: ''
		}
	},
	computed: {
		detailFilterList () {
			let arr = []
			this.detailList.forEach((item) => arr.push(item))
			if (this.detailFilterText) {
				arr = this.detailList.filter(item => item.prd_name.includes(this.detailFilterText)||
					item.prd_iden.includes(this.detailFilterText)||
					item.prd_remarks.includes(this.detailFilterText)||
					item.prd_specification.includes(this.detailFilterText)||
					item.prd_model.includes(this.detailFilterText)
				)
			}
			return arr
		}
	},
	methods: {
		
	},
	onLoad: function() {
		let _this = this
		let myinfo = uni.getStorageSync('user_info')
		let pr_info = uni.getStorageSync('order_info')
		uni.removeStorageSync('order_info')
		let msg = {}
		msg.pr_iden = pr_info.iden
	    msg.orga_name = pr_info.orga
		msg.user_now_iden = myinfo.data.user.username
		this.$http.post('/purchaseRequest/prNew', msg).then(([err,res]) => {
			if (res.data.signal === 1) {
				_this.detailList = res.data.prds
		    } else {
				
		    }
		})
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
