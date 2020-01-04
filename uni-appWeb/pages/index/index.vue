<template>
    <view class="content">
		<view class="learning-center">
							<text class="learning-center-title">学习中心</text>
								<view style="width: 80%; margin: auto; margin-bottom: 20px;">
								        <xfl-select 
								            :list="list1"
								            :clearable="false"
								            :showItemNum="5" 
								            :listShow="true"
								            :isCanInput="true"  
								            :style_Container="'height: 50px; font-size: 16px;'"
								            :placeholder = "'请选择学习中心'"
								            :initValue="''"
								            :selectHideType="'hideAll'"
								        >
								        </xfl-select>
								</view>
							</text>
		</view>
		<view class="content-control">
			<uni-segmented-control :current="current" :values="items" @clickItem="onClickItem" style-type="button" active-color="#0faeff"></uni-segmented-control>
		</view>
		<view class="current-content">
			<view v-if="current === 0">
				<view v-for="item in engList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.total_iden" 
					    mode="basic" 
					    :is-shadow="true" 
					>
							<view>仓库编号：{{ item.stock_iden}}</view>
							<view>物料名称：{{ item.total_name}}</view>
							<view>规格：{{ item.total_specification }}</view>
							<view>类型：{{ item.total_model }}</view>
							<view>单位：{{ item.total_meterage }}</view>
							<view>存货属性：{{ item.total_attr }}</view>
						    <view>现存量：{{ item.total_present_num }}</view>
					</uni-card>
				</view>
			</view>
			<view v-if="current === 1">
				<view v-for="item in tecList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.total_iden" 
					    mode="basic" 
					    :is-shadow="true" 
					>
							<view>仓库编号：{{ item.stock_iden}}</view>
							<view>物料名称：{{ item.total_name}}</view>
							<view>规格：{{ item.total_specification }}</view>
							<view>类型：{{ item.total_model }}</view>
							<view>单位：{{ item.total_meterage }}</view>
							<view>存货属性：{{ item.total_attr }}</view>
						    <view>现存量：{{ item.total_present_num }}</view>
					</uni-card>
				</view>
			</view>
			<view v-if="current === 2">
				<view v-for="item in artList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.total_iden" 
					    mode="basic" 
					    :is-shadow="true" 
					>
							<view>仓库编号：{{ item.stock_iden}}</view>
							<view>物料名称：{{ item.total_name}}</view>
							<view>规格：{{ item.total_specification }}</view>
							<view>类型：{{ item.total_model }}</view>
							<view>单位：{{ item.total_meterage }}</view>
							<view>存货属性：{{ item.total_attr }}</view>
						    <view>现存量：{{ item.total_present_num }}</view>
					</uni-card>
				</view>
			</view>
			<view v-if="current === 3">
				<view v-for="item in spoList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.total_iden" 
					    mode="basic" 
					    :is-shadow="true" 
					>
							<view>仓库编号：{{ item.stock_iden}}</view>
							<view>物料名称：{{ item.total_name}}</view>
							<view>规格：{{ item.total_specification }}</view>
							<view>类型：{{ item.total_model }}</view>
							<view>单位：{{ item.total_meterage }}</view>
							<view>存货属性：{{ item.total_attr }}</view>
						    <view>现存量：{{ item.total_present_num }}</view>
					</uni-card>
				</view>>

			</view>
		</view>
    </view>
</template>

<script>
import xflSelect from '../../components/xfl-select/xfl-select.vue';
import uniSegmentedControl from '../../components/uni-segmented-control/uni-segmented-control.vue'
import uniCard from '../../components/uni-card/uni-card.vue'
import cmdIcon from "../../components/cmd-icon/cmd-icon.vue"
import engData from '../../data/English.js'
import tecData from '../../data/technology.js'
import artData from '../../data/art.js'
import spoData from '../../data/sports.js'

export default {
	components: {
		xflSelect,
		uniSegmentedControl,
		uniCard,
		cmdIcon
	},
	data() {
		return {
			items: ['英语','科技','艺术','体育'],
			list1: [
					'安高中心',
					'财富中心',
					'稻香路中心',
					'习友路中心'
					],
			current: 0,
			//将data文件夹中的数据读入
			engList: engData.data,
			tecList: tecData.data,
			artList: artData.data,
			spoList: spoData.data,
		}
	},
	methods: {
		//切换tab
		onClickItem(e) {
			if (this.current !== e.currentIndex) {
				this.current = e.currentIndex;
			}
		},
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
	.learning-center {
				display: flex;
				align-items: center;
				position: relative;
				padding: 0 30upx;
				height: 100upx;
				background: #fff;
				border-bottom:1upx solid #F8F8F8;
			}
			.learning-center-title {
				flex-shrink: 0;
				width: 200rpx;
				font-size: 16px;
				color:#606266;
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
	.button-box {
		display: flex;
		justify-content: space-between;
		padding-top: 40upx;
	}
	.delete {
		width: 60upx;
		color: red;
	}
	.edit {
		width: 60upx;
	}
	.detail {
		width: 60upx;
	}
	.commit {
		width: 60upx;
		color: green;
	}
</style>
