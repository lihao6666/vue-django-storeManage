<template>
	<view class="tabBar">
		<view
		 v-for="(item,index) in tabBar" 
		 :key="item.url" 
		 class="tabbar_item" 
		 :class="{'active':item.url == currentPage}"
		 @click="navTo(item)"
		 >
			<image v-if="item.url == currentPage" :src="item.imgClick" mode=""></image>
			<image v-else :src="item.imgNormal" mode=""></image>
			<view class="text">{{item.text}}</view>
		</view>
	</view>
</template>

<script>
	export default {
		props:{
			currentPage:{
				type:String,
				default:'index'
			}
		},
		data() {
			return {
				tabBar:[{
						url:'index',
						text:'首页',
						imgNormal:'../static/tab-index.png',
						imgClick:'../static/tab-index-current.png'
					},
					{
					    url: 'requisitions',
					    text: '请购',
					    imgNormal: "../static/img/home.png",
					    imgClick: "../static/img/homeHL.png"
					},{
						url:'user',
						text:'我的',
						imgNormal:'../static/tab-my.png',
						imgClick:'../static/tab-my-current.png'
					}]
			};
		},
		created() {
			uni.hideTabBar({})
		},
		computed:{
			
		},
		methods:{
			navTo(item){
				if(item.url !== this.currentPage){
					var isUrl = `/pages/${item.url}/${item.url}`
					const that = this
					uni.switchTab({
						url: isUrl
					})
				} else{
					this.$parent.toTop()
				}
			}
		}
	}
</script>

<style lang="scss" scoped>
	//导航栏设置
		$isRadius:0upx; //左上右上圆角
		$isWidth:100vw; //导航栏宽度
		$isBorder:0px solid white; //边框 不需要则设为0px
		$isBg:white; //背景
	
	// 选中设置
		$chooseTextColor:#50B7EA; //选中时字体颜色
		$chooseBgColor:transparent; //选中时背景颜色 transparent为透明
	
	//未选中设置
		$normalTextColor:#999; //未选中颜色
	.tabBar{
		width: $isWidth;
		height: 100upx;
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		box-shadow: 0upx -2upx 10upx rgba(89,125,172,.4);
		margin:0 auto;
		z-index: 998;
		background-color: $isBg;
		color: $normalTextColor;
		border-left: $isBorder;
		border-top: $isBorder;
		border-right: $isBorder;
		display: flex;
		justify-content: space-around;
		border-top-right-radius: $isRadius;
		border-top-left-radius: $isRadius;
		box-sizing: border-box;
		overflow: hidden;
		.tabbar_item{
			width: 25%;
			font-size: 12px;
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
			&.active{
				border-left: $isBorder;
				border-top: $isBorder;
				background: $chooseBgColor;
				color: $chooseTextColor;
			}
		}
		image{
			width: 48upx;
			height:48upx;
			margin-left: 5upx;
		}
	}
</style>
