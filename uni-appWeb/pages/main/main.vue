<template>
    <view>
		<view class="contentControl">
			<uni-segmented-control :current="current" :values="items" @clickItem="onClickItem" style-type="button" active-color="#0faeff"></uni-segmented-control>
		</view>
		<view class="currentContent">
			<view v-if="current === 0"><text class="content-text">选项卡1的内容</text></view>
			<view v-if="current === 1"><text class="content-text">选项卡2的内容</text></view>
			<view v-if="current === 2"><text class="content-text">选项卡3的内容</text></view>
			<view v-if="current === 3"><text class="content-text">选项卡4的内容</text></view>
		</view>
    </view>
</template>

<script>
import uniSegmentedControl from '../../components/uni-segmented-control/uni-segmented-control.vue'
export default {
	components: {
		uniSegmentedControl
	},
	data() {
		return {
			items: ['请购','出库','销售','转库'],
			current: 0
		}
	},
	methods: {
		onClickItem(e) {
			if (this.current !== e.currentIndex) {
				this.current = e.currentIndex;
			}
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
	
	.tabs {
		padding: 0;
	}
	.contentControl {
		padding: 5upx;
		width: auto;
	}
	.currentContent {
		justify-content: center;
		align-items: center;
		height: 150px;
		text-align: center;
	}
	
</style>
