<template>
    <view>
		<view class="tabs">
            <maintabs :tabTitle="tabTitle" @changeTab='changeTab'></maintabs>
		</view>
		<!-- <view class="info">
			<swiper style="min-height: 100vh;" :current="currentTab" @change="swiperTab">
				<swiper-item v-for="(listItem,listIndex) in list" :key="listIndex">
					<scroll-view style="height: 100%;" scroll-y="true" @scrolltolower="lower1" scroll-with-animation :scroll-into-view="toView">
						<view style="width: 100%;height: 153upx;"></view> --> <!-- 边距盒子 -->
						<!-- <view class='content'>
							<view class='card' v-for="(item,index) in listItem" v-if="listItem.length > 0" :key="index">
								{{item}}
							</view>
						</view>
						<view class='noCard' v-if="listItem.length===0">
							暂无信息
						</view>
						<view style="width: 100%;height: 100upx;opacity:0;">底部占位盒子</view>
					</scroll-view>
				</swiper-item>
			</swiper>
		</view> -->
    </view>
</template>

<script>
import maintabs from '../../components/mainpage/Maintabs.vue';
export default {
	components: {maintabs},
	data() {
		return {
			tabTitle:['请购','出库','销售','转库']
		};
	},
	methods: {
		changeTab(index) {
			
		}
	},
	// onLoad: function() {   //登录检查函数
	// 	loginMsg = this.checkLogin('../pages/main/main', 'switchTab');
	// 	if(!loginMsg){
	// 		return;
	// 	}
	// }
}

</script>

<style>
	.tabs {
		padding: 0;
	}
</style>
