<template>
	<view class="page">
		
		<!-- <qsTab
		ref="tabs" 
		:tabs="tabs" 
		animationMode="line1" 
		:current="current"
		 @change="tabChange"
		swiperWidth="750">
		</qsTab> -->
		
<!-- 		<view class="swiper" :current="current"  
		@transition="transition"
		@animationfinish="animationfinish">
			<swiper-item class="swiper-item" @transition="transition" v-for="(item, index) in tabs" :key="index" @change="swiperChange" @tap.stop="swichNav(index)">
				<indexList :i="index" :type="current"></indexList>
			</swiper-item>
		</view> -->
		
				<view class="list_box">
					<view class="left">
						<scroll-view scroll-y="true" :style="{ 'height':scrollHeight }">
							<view class="item" 
								v-for="(item,index) in leftArray"
								:key="index" 
								:class="{ 'active':index==leftIndex }" 
								:data-index="index"
								@tap="leftTap"
							>{{item}}</view>
				        </scroll-view>
						<navigator url="./start" hover-class="navigator-hover">
						<button class='start' type="default"> 新建</button>
						</navigator>
					</view>
					<view class="main">
						<scroll-view  scroll-y="true" :style="{ 'height':scrollHeight }" @scroll="mainScroll" :scroll-into-view="scrollInto" scroll-with-animation="true">
							<view class="item" v-for="(item,index) in mainArray" :key="index" :id="'item-'+index">
								<view class="title">
									<view>{{item.title}}</view>
								</view>
								<view class="goods" v-for="(item2,index2) in item.list" :key="index2">
									<image src="/static/logo.png" mode=""></image>
									<view>
										<view>第{{index2+1}}个商品标题</view>
										<view class="describe">第{{index2+1}}个商品的描述内容</view>
										<view class="money">第{{index2+1}}个商品的价格</view>
									</view>
								</view>
							</view>
						</scroll-view>
					</view>
				</view>
				
	</view>
</template>

<script>
	// import indexList from './list.vue'
	// import qsTab from '../../components/QS-tabs/QS-tabs.vue'
	
	
	
	// export default {
	// 	// components: {
	// 	// 	qsTab,
	// 	// },
	import uniSegmentedControl from '../../components/uni-section/uni-section.vue'
	import uniSection from '../../components/uni-section/uni-section.vue'
	export default {
		components: {
			uniSection,
			uniSegmentedControl
		},
		data() {
			return {
				// items: ['选项卡1', '选项卡2'],
				// styles: [{
				// 		value: 'button',
				// 		text: '按钮',
				// 		checked: true
				// 	}
				// ],
				// colors: ['#007aff', '#4cd964', '#dd524d'],
				current: 0,
				colorIndex: 0,
				activeColor: '#007aff',
				styleType: 'button',
				// tabs: [
				// 	{
				// 		name: '查看',
				// 		 state: 0,
				// 		 orderList: []
				// 	},
				// 	{
				// 		name: '新建',
				// 		 state: 1,
				// 		orderList: []
				// 	}
				// ],
				scrollHeight:'500px',
				leftArray:[],
				mainArray:[],
				topArr:[],
				leftIndex:0,
				scrollInto:'',
			}	
		},onLoad() {
			uni.getSystemInfo({
				success:(res)=>{
					/* 设置当前滚动容器的高，若非窗口的高度，请自行修改 */
					this.scrollHeight=`${res.windowHeight}px`;
				}
			});
		},
		mounted(){
			this.getListData();
		},
		methods:{
			// onClickItem(e) {
			// 		if (this.current !== e.currentIndex) {
			// 			this.current = e.currentIndex
			// 		}
			// 	},
			// 	styleChange(e) {
			// 		if (this.styleType !== e.detail.value) {
			// 			this.styleType = e.detail.value
			// 		}
			// 	},
			// 	colorChange(e) {
			// 		if (this.styleType !== e.detail.value) {
			// 			console.log(e.detail.value);
			// 			this.activeColor = e.detail.value
			// 		}
			// 	},
			
			// swiperChange(e) {
			// 	this.current = e.detail.current
			// },
			
			// // changeTab(e) {
			// // 	this.current = e.target.current;
			// // },
			
			// transition({ detail: { dx } }) {
			// 	this.$refs.tabs.setDx(dx);
			// },
			
			// animationfinish({detail: { current }}) {
			// 	this.$refs.tabs.setFinishCurrent(current);
			// 	// this.swiperCurrent = current;
			// 	this.current = current;
			// },
			
			// /**
			//  * 选显卡切换
			//  * */
			// tabChange(index) {
			// 	this.current = index
				
			// },
			
			// swichNav(index) {
			// 	let item = this.tabs[index]
			// 	if (item && item.disabled) return
			// 	if (this.currentTab == index) {
			// 		return false
			// 	} else {
			// 		this.currentTab = Number(index)
			// 	}
			// },
			
			
			/* 获取列表数据 */
			getListData(){
				/* 因无真实数据，当前方法模拟数据 */
				let [left,main]=[[],[]];
				
				
			
				for(let i=0;i<3;i++){
					left.push(`${i+1}类`);
					
					let list=[];
					for(let j=0;j<10;j++){
						list.push(j);
					}
					main.push({
						title:`第${i+1}表单`,
						list
					})
				}
				this.leftArray=left;
				this.mainArray=main;
				
				this.$nextTick(()=>{
					this.getElementTop();
				});
			},
			/* 获取元素顶部信息 */
			getElementTop(){
				/* Promise 对象数组 */
				let p_arr=[];
				
				/* 新建 Promise 方法 */
				let new_p=(selector)=>{
					return new Promise((resolve,reject)=>{
						let view = uni.createSelectorQuery().select(selector);
						view.boundingClientRect(data => {
							resolve(data.top);
						}).exec();
					})
				}
				
				/* 遍历数据，创建相应的 Promise 数组数据 */
				this.mainArray.forEach((item,index)=>{
					p_arr.push(new_p(`#item-${index}`));
				});
				
				/* 所有节点信息返回后调用该方法 */
				Promise.all(p_arr).then((data)=>{
					this.topArr=data;					
				});
			},
			/* 主区域滚动监听 */
			mainScroll(e){
				let top =e.detail.scrollTop;
				let index=0;
				/* 查找当前滚动距离 */
				for(let i = (this.topArr.length-1);i>=0;i--){
					/* 在部分安卓设备上，因手机逻辑分辨率与rpx单位计算不是整数，滚动距离与有误差，增加2px来完善该问题 */
					if((top+2)>=this.topArr[i]){
						index = i;
						break;
					}
				}
				this.leftIndex=(index < 0 ? 0: index);
			},
			/* 左侧导航点击 */
			leftTap(e){
				let index=e.currentTarget.dataset.index;
				this.scrollInto=`item-${index}`;
			}
		}
	}
</script>

<style lang="scss" scoped>
	.page {
		width: 100%;
		height: 100%;
	}
	.swiper {
		width: 100%;
		height: 30%;
		.swiper-item {
			width: 100%;
			height: 100%;
		}
	}
	
	.list_box{
		display: flex;
	    flex-direction: row;
	    flex-wrap: nowrap;
	    justify-content: flex-start;
	    align-items: flex-start;
	    align-content: flex-start;
		font-size: 28rpx;
		
		.left{
			width: 200rpx;
			background-color: #f6f6f6;
			line-height: 80rpx;
			box-sizing: border-box;
			font-size: 32rpx;
			
			.item{
				padding-left: 20rpx;
				position: relative;
				&:not(:first-child) {
					margin-top: 1px;
				
					&::after {
						content: '';
						display: block;
						height: 0;
						border-top: #d6d6d6 solid 1px;
						width: 620upx;
						position: absolute;
						top: -1px;
						right: 0;
						transform:scaleY(0.5);	/* 1px像素 */
					}
				}
				
				&.active{
					color: #42b983;
					background-color: #fff;
				}
			}
			
				
			.start{
				position: absolute;
				bottom:8px;
				width: 200rpx;
			}
		}
		.main{
			background-color: #fff;
			padding-left: 20rpx;
			width: 0;
			flex-grow: 1;
			box-sizing: border-box;
			
			
			
			.title{
				line-height: 64rpx;
				font-size: 24rpx;
				font-weight: bold;
				color: #666;
				background-color: #fff;
				position: sticky;
				top: 0;
				z-index: 19;
			}
			
			.item{
				padding-bottom: 10rpx;
				border-bottom: #eee solid 1px;
			}
			
			.goods{
				display: flex;
				flex-direction: row;
				flex-wrap: nowrap;
				justify-content: flex-start;
				align-items: center;
				align-content: center;
				margin-bottom: 10rpx;
				
				&>image{
					width: 120rpx;
					height: 120rpx;
					margin-right: 16rpx;
				}
				
				.describe{
					font-size: 24rpx;
					color: #999;
				}
				
				.money{
					font-size: 24rpx;
					color: #efba21;
				}
				
			}
		}
	}
</style>