<template>
	<view class="container999" @click="conClick" @touchstart="refreshStart" @touchmove="refreshMove" @touchend="refreshEnd">
		<!-- 刷新组件需搭配scroll-view使用，并在pages.json中添加 "disableScroll":true-->
		<refresh ref="refresh" @isRefresh='isRefresh'></refresh>
				<!-- 点击反馈组件 -->
		<clickCircle ref="clickCircle"></clickCircle>
		<view class='nav'>
			<!-- #ifdef H5 -->
				<view style="height: 44px;width: 100%;">边距盒子</view>
			<!-- #endif -->
			<!-- 搜索 -->
			<view class='searchInput999'>
				<view class='searchBox999'>
					<image src='/static/icon-search.png' class='search999'></image>
				</view>
				<input class='input999' placeholder="输入关键词"></input>
			</view>
			<!-- 导航栏 agents导航栏标题 -->
			<navTab ref="navTab" :tabTitle="tabTitle" @changeTab='changeTab'></navTab>
		</view>
		<!-- 回到顶部悬浮按钮 -->
		<movable-area style="height: 100vh; width: 100vw;position: absolute;bottom: 0;">
		    <movable-view class="addBtnBox" style="padding-top:120upx;padding-bottom:120upx;"  @touchmove.stop="" :x="isX" :y="isY" direction="all">
				<view class="addBtn" @click="toTop">TOP</view>
		    </movable-view>
		</movable-area>
		<!-- swiper切换 swiper-item表示一页 scroll-view表示滚动视窗 -->
		<swiper style="min-height: 100vh;" :current="currentTab" @change="swiperTab">
			<swiper-item v-for="(listItem,listIndex) in list" :key="listIndex">
				<scroll-view style="height: 100%;" scroll-y="true" @scrolltolower="lower1" scroll-with-animation :scroll-into-view="toView">
				<view :id="'top'+listIndex" style="width: 100%;height: 180upx;">边距盒子</view>
				<view class='content'>
					<view v-if="listIndex == 0">我是第一页特有的内容我是第一页特有的内容我是第一页特有的内容我是第一页特有的内容我是第一页特有的内容我是第一页特有的内容我是第一页特有的内容</view>
					<view v-if="listIndex == 1">
						我是轮播图
						<swiper style="height: 30vh;width: 100vw;">
							<swiper-item v-for="(item,inde) in 3" :key="inde">
								<image style="height: 100%;width:100%;" src="../../static/logo.png"></image>
							</swiper-item>
						</swiper>
					</view>
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
		<tabBar4 :currentPage="currentPage"></tabBar4>
	</view>
</template>

<script>
const util = require('../../util/util.js');
import refresh from '../../components/refresh.vue';
import navTab from '../../components/navTab.vue';
import clickCircle from '../../components/clickCircle.vue';
import tabBar4 from '../../components/tabBar4.vue';
export default {
	components: {refresh,navTab,clickCircle,tabBar4},
	data() {
		return {
			currentPage:'user',
			toView:'',//回到顶部id
			isX:0,//放在store统一管理
			isY:999,//放在store统一管理
			tabTitle:['英语','科技','艺术'], //导航栏格式 --导航栏组件
			currentTab: 0, //sweiper所在页
			pages:[1,1,1], //第几个swiper的第几页
			list: [[1, 2, 3, 4, 5, 6],['a', 'b', 'c', 'd', 'e', 'f'],[]] //数据格式
		};
	},
	onLoad(e) {
		
	},
	onShow() {},
	onHide() {},
	methods: {
		toTop(){
			this.toView = ''
			setTimeout(()=>{
				this.toView = 'top' + this.currentTab
			},10)
		},
		changeTab(index){
			this.currentTab = index
		},
		// 点击反馈事件
		conClick(e) {
		    this.$refs.clickCircle.conClick(e);
		},
		// 其他请求事件 当然刷新和其他请求可以写一起 多一层判断。
		isRequest(pages) {
			return new Promise((resolve, reject) => {
				this.pages[this.currentTab]++
				var that = this
				setTimeout(() => {
					uni.hideLoading()
					uni.showToast({
						icon: 'none',
						title: `请求第${that.currentTab + 1 }个导航栏的第${that.pages[that.currentTab]}页数据成功`
					})
					let newData = ['新数据1','新数据2','新数据3']
					resolve(newData)
				}, 1000)
			})
		},
		// swiper 滑动
		swiperTab: function(e) {
			var index = e.detail.current //获取索引
			this.$refs.navTab.longClick(index);
		},
		// 加载更多 util.throttle为防抖函数
		lower1: util.throttle(function(e) {
		console.log(`加载${this.currentTab}`)//currentTab表示当前所在页数 根据当前所在页数发起请求并带上page页数
		uni.showLoading({
			title: '加载中',
			mask:true
		})
			this.isRequest().then((res)=>{
				let tempList = this.list
				tempList[this.currentTab] = tempList[this.currentTab].concat(res)
				console.log(tempList)
				this.list = tempList
				this.$forceUpdate() //二维数组，开启强制渲染
			})
		}, 300),
		// 刷新touch监听
		refreshStart(e) {
			this.$refs.refresh.refreshStart(e);
		},
		refreshMove(e){
			this.$refs.refresh.refreshMove(e);
		},
		refreshEnd(e) {
			this.$refs.refresh.refreshEnd(e);
		},
		isRefresh(){
				setTimeout(() => {
					uni.showToast({
						icon: 'success',
						title: '刷新成功'
					})
					this.$refs.refresh.endAfter() //刷新结束调用
				}, 1000)
		}
	}
};
</script>

<style lang="scss">
	.addBtnBox{
		position: fixed;
		z-index:900;
		width: 140upx;
		align-items: flex-end;
		justify-content: center;
		height: 140upx;
		display:flex;
		.addBtn{
			width: 100upx;
			height: 100upx;
			border-radius: 50%;
			color: white;
			font-size: 10px;
			font-weight: bold;
			background: #444857;
			line-height: 100upx;
			text-align: center;
			box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
		}
	}
		.container999 {
	  width: 100vw;
	  font-size: 28upx;
	  min-height: 100vh;
	  overflow: hidden;
	  color: #6B8082;
	  position: relative;
	  background-color: #f6f6f6;
	}
	.content {
		width: 100%;
	}
	
	.card {
		width: 90%;
		height: 368upx;
		background-color: white;
		margin: 0 auto 42upx auto;
		background: #FFFFFF;
		box-shadow: 0 0 5px 0 rgba(0, 0, 0, 0.10);
		border-radius: 5px;
		position: relative;
	}
	
	.noCard {
		width: 90%;
		height: 200upx;
		margin: auto;
		background-color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #999999;
		box-shadow: 0 0 10upx 0 rgba(0, 0, 0, 0.10);
		border-radius: 10upx;
	}
	
	
	.nav {
		position: fixed;
		left: 0;
		top: 0;
		color: white;
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		justify-content: flex-start;
		font-size: 24upx;
		background-color: #50B7EA;
		z-index: 996;
	}
	
	.searchInput999 {
		width: 90%;
		margin: 0 auto;
		background: white;
		border-radius: 30upx;
		display: flex;
		align-items: center;
		justify-content: center;
		height: 56upx;
	}
	
	.search999 {
		width: 32upx;
		height: 32upx;
	}
	
	.searchBox999 {
		width: 56upx;
		height: 56upx;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	
	.input999 {
		color: #999;
		width: 80%;
	}
</style>
