<template>
    <view class="content">
		<view class="content-control">
			<uni-segmented-control :current="current" :values="items" @clickItem="onClickItem" style-type="button" active-color="#0faeff"></uni-segmented-control>
		</view>
		<view class="current-content">
			<view v-if="current === 0">
				<view v-for="item in outList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.mso_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.mso_date"
					>
						<view>库存组织：{{ item.mso_orga }}</view>
						<view>出库仓库：{{ item.mso_warehouse }}</view>
						<view>出库分类：{{ item.mso_type }}</view>
						<view>出库部门：{{ item.mso_req_department }}</view>
						<view>备注：{{ item.mso_remarks }}</view>
						<view>创建人：{{ item.mso_creator }}</view>
						<view>创建日期：{{ item.mso_createDate }}</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOut">
					</drag-button>
				</view>
			</view>
			<view v-if="current === 1">选项卡2的内容</view>
			<view v-if="current === 2">选项卡3的内容</view>
			<view v-if="current === 3">选项卡4的内容</view>
		</view>
    </view>
</template>

<script>
import uniSegmentedControl from '../../components/uni-segmented-control/uni-segmented-control.vue'
import uniCard from '../../components/uni-card/uni-card.vue'
import dragButton from '../../components/drag-button/drag-button.vue'
import outData from '../../data/outStore.js'

export default {
	components: {
		uniSegmentedControl,
		uniCard,
		dragButton
	},
	data() {
		return {
			items: ['出库','请购','销售','转库'],
			current: 0,
			pattern: {
				color: '#7A7E83',
				backgroundColor: '#fff',
				selectedColor: '#007AFF',
				buttonColor: '#007AFF'
			},
			outList: outData.data,
			purchaseList: [
				
			],
			sellList: [
				
			],
			exchangeList: [
				
			]
		}
	},
	methods: {
		onClickItem(e) {
			if (this.current !== e.currentIndex) {
				this.current = e.currentIndex;
			}
		},
		newOut() {
			uni.navigateTo({
			    url: '../user/phoneus',
			});
		}
	}
	// onLoad: function() {   //登录检查函数
	// 	loginMsg = this.checkLogin('../pages/main/main', 'switchTab');
	// 	if(!loginMsg){
	// 		return;
	// 	}
	// }
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
		font-size: 28rpx;
		line-height: inherit;
	}
	.content {
		padding: 0;
	}
	.tabs {
		padding: 0;
	}
	.content-control {
		padding: 5upx;
		width: auto;
	}
	.current-content {
		justify-content: center;
		align-items: center;
		text-align: left;
	}
	
</style>
