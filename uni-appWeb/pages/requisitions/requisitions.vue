<template>
	<view class="page">
		
		<!-- <sl-filter :independence="true" :color="titleColor" :themeColor="themeColor" :menuList.sync="menuList" @result="result"></sl-filter> -->
		
		<view v-for="item in materialList" :key="item.id" class="card-set">
			<uni-card
			    :title="item.mso_iden"
			    mode="basic" 
			    :is-shadow="true" 
				:extra="item.mso_date"
			>
				<view>物料编码：{{ item.material_iden }}</view>
				<view>物料名称：{{ item.material_name }}</view>
				<view>规格：{{ item.material_specification }}</view>
				<view>型号：{{ item.material_model }}</view>
				<view>计量单位：{{ item.material_meterage }}</view>
				<view>存货量：{{ item.material_attr }}</view>
				<view>选择数量:  <yp-number-box class="num_select" :max="item.material_attr" index="item.material_iden"></yp-number-box></view>
				<view>选择：<switch color='#d81e06' @change="switchChange" /></view>
				<view>备注：<textarea class="remarks_input" maxlength="200" v-model="remarks" placeholder="请输入,限制200字" auto-height="true"></textarea></view>
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
</template>

<script>
	import uniSegmentedControl from '../../components/uni-segmented-control/uni-segmented-control.vue'
	import uniCard from '../../components/uni-card/uni-card.vue'
	import uniSection from '../../components/uni-section/uni-section.vue'
	// import slFilter from '@/components/sl-filter/sl-filter.vue'
	import materialData from '../../data/materialData.js'
	import dragButton from '../../components/drag-button/anotherButton.vue'
	import ypNumberBox from '@/components/yp-number-box/yp-number-box.vue'
	
	export default {
		components: {
			uniSegmentedControl,
			uniCard,
			uniSection,
			uniSegmentedControl,
			// slFilter,
			dragButton,
			ypNumberBox
		},
		data() {
			return {
				themeColor: '#000000',
				titleColor: '#666666',
				filterResult: '',
				materialList: materialData.data,
				menuList: [{
						'title': '品牌',
						'detailTitle': '请选择职位类型（可多选）',
						'isMutiple': true,
						'key': 'jobType',
						'defaultSelectedIndex': [0],
						'detailList': [{
								'title': '不限',
								'value': ''
							},
							{
								'title': 'uni-app',
								'value': 'uni-app'
							},
							{
								'title': 'java开发',
								'value': 'java'
							},
							{
								'title': 'web开发',
								'value': 'web'
							},
							{
								'title': 'Android开发',
								'value': 'Android'
							},
							{
								'title': 'iOS开发',
								'value': 'iOS'
							},
							{
								'title': '测试工程师',
								'value': '测试'
							},
							{
								'title': 'UI设计',
								'value': 'UI'
							},
							{
								'title': 'Ruby开发',
								'value': 'Ruby'
							},
							{
								'title': 'C#开发',
								'value': 'C#'
							},
							{
								'title': 'PHP开发',
								'value': 'php'
							},
							{
								'title': 'Python开发',
								'value': 'Python'
							}
						]
				
					},
					{
						'title': '型号',
						'key': 'salary',
						'isMutiple': true,
						'detailList': [{
								'title': '不限',
								'value': ''
							},
							{
								'title': '0~2000',
								'value': '0~2000'
							},
							{
								'title': '2000~3000',
								'value': '2000~3000'
							},
							{
								'title': '3000~4000',
								'value': '3000~4000'
							},
							{
								'title': '4000~5000',
								'value': '4000~5000'
							},
							{
								'title': '5000~6000',
								'value': '5000~6000'
							},
							{
								'title': '6000~7000',
								'value': '6000~7000'
							},
							{
								'title': '7000~8000',
								'value': '7000~8000'
							},
							{
								'title': '8000~9000',
								'value': '8000~9000'
							},
							{
								'title': '9000~10000',
								'value': '9000~10000'
							},
							{
								'title': '10000以上',
								'value': '10000~1000000'
							}
						]
				
					},
					{
						'title': '单选',
						'key': 'single',
						'isMutiple': false,
						'detailTitle': '请选择（单选）',
						'reflexTitle': true,
						'defaultSelectedIndex': 2,
						'detailList': [{
								'title': '不限',
								'value': ''
							},
							{
								'title': '条件1',
								'value': 'test_1'
							},
							{
								'title': '条件2',
								'value': 'test_2'
							},
							{
								'title': '条件3',
								'value': 'test_3'
							},
							{
								'title': '条件4',
								'value': 'test_4'
							},
							{
								'title': '条件5',
								'value': 'test_5'
							},
							{
								'title': '条件6',
								'value': 'test_6'
							},
							{
								'title': '条件7',
								'value': 'test_7'
							},
							{
								'title': '条件8',
								'value': 'test_8'
							},
						]
					},
					{
						'title': '排序',
						'key': 'sort',
						'isSort': true,
						'reflexTitle': true,
						'defaultSelectedIndex': 2,
						'detailList': [{
								'title': '默认排序',
								'value': ''
							},
							{
								'title': '发布时间',
								'value': 'add_time'
							},
							{
								'title': '薪资最高',
								'value': 'wages_up'
							},
							{
								'title': '离我最近',
								'value': 'location'
							}
						]
					}
				]
			}	
		},onLoad() {
			
		},
		mounted(){
			
		},
		methods:{
			result(val) {
				console.log('filter_result:' + JSON.stringify(val));
				this.filterResult = JSON.stringify(val, null, 2)
			},
			newOut(){
				uni.navigateTo({
					url: './start',
				});
			}
		}
	}
</script>

<style lang="scss" scoped>
	.page {
		width: 100%;
		height: 100%;
		background: #F1F0F3;
	}
	
	.num_select{
		
	}
	// .swiper {
	// 	width: 100%;
	// 	height: 30%;
	// 	.swiper-item {
	// 		width: 100%;
	// 		height: 100%;
	// 	}
	// }
	
	// .list_box{
	// 	display: flex;
	//     flex-direction: row;
	//     flex-wrap: nowrap;
	//     justify-content: flex-start;
	//     align-items: flex-start;
	//     align-content: flex-start;
	// 	font-size: 28rpx;
		
	// 	.left{
	// 		width: 200rpx;
	// 		background-color: #f6f6f6;
	// 		line-height: 80rpx;
	// 		box-sizing: border-box;
	// 		font-size: 32rpx;
			
	// 		.item{
	// 			padding-left: 20rpx;
	// 			position: relative;
	// 			&:not(:first-child) {
	// 				margin-top: 1px;
				
	// 				&::after {
	// 					content: '';
	// 					display: block;
	// 					height: 0;
	// 					border-top: #d6d6d6 solid 1px;
	// 					width: 620upx;
	// 					position: absolute;
	// 					top: -1px;
	// 					right: 0;
	// 					transform:scaleY(0.5);	/* 1px像素 */
	// 				}
	// 			}
				
	// 			&.active{
	// 				color: #42b983;
	// 				background-color: #fff;
	// 			}
	// 		}
			
				
	// 		.start{
	// 			position: absolute;
	// 			bottom:8px;
	// 			width: 200rpx;
	// 		}
	// 	}
	// 	.main{
	// 		background-color: #fff;
	// 		padding-left: 20rpx;
	// 		width: 0;
	// 		flex-grow: 1;
	// 		box-sizing: border-box;
			
			
			
	// 		.title{
	// 			line-height: 64rpx;
	// 			font-size: 24rpx;
	// 			font-weight: bold;
	// 			color: #666;
	// 			background-color: #fff;
	// 			position: sticky;
	// 			top: 0;
	// 			z-index: 19;
	// 		}
			
	// 		.item{
	// 			padding-bottom: 10rpx;
	// 			border-bottom: #eee solid 1px;
	// 		}
			
	// 		.goods{
	// 			display: flex;
	// 			flex-direction: row;
	// 			flex-wrap: nowrap;
	// 			justify-content: flex-start;
	// 			align-items: center;
	// 			align-content: center;
	// 			margin-bottom: 10rpx;
				
	// 			&>image{
	// 				width: 120rpx;
	// 				height: 120rpx;
	// 				margin-right: 16rpx;
	// 			}
				
	// 			.describe{
	// 				font-size: 24rpx;
	// 				color: #999;
	// 			}
				
	// 			.money{
	// 				font-size: 24rpx;
	// 				color: #efba21;
	// 			}
				
	// 		}
	// 	}
		
	// }
</style>