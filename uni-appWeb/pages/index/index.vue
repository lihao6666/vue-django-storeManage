<template>
    <view class="content">
		<uni-nav-bar :fixed="true" background-color="#20a0ff" :border="false">
			<view class="input-view">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="FilterText" confirm-type="search" class="input" type="text" placeholder="输入查询信息">
				<uni-icons :color="'#999999'" v-if="FilterText!==''" class="icon-clear" type="clear" size="22" @click="clear1" />
			</view>
		</uni-nav-bar>
		<!-- <view class="content-control">
			<uni-segmented-control :current="current" :values="items" @clickItem="onClickItem" style-type="button" active-color="#20a0ff"></uni-segmented-control>
		</view> -->
		<view class="current-content">
				<view v-for="(item,index) in EnglishList" :key="index" class="card-set">
					<uni-card
					    :title="item.material_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra=none
					>
					    <view>
							<view>物料名称：{{item.material_name}}</view>
							<view>库存组织编号：{{ item.orga_iden }}</view>
							<view>库存组织：{{ item.orga_name }}</view>
							<view>仓库编号：{{ item.total_iden }}</view>
							<view>仓库：{{ item.total_name }}</view>
						</view>
						<view class="button-box">
							<view class="detail" @click="viewDetail(item)"><evan-icons type="reorder" size="15"></evan-icons>详情</view>
						</view>
					</uni-card>
				</view>
		</view>
    </view> 
</template>
 
<script>
import uniSegmentedControl from '../../components/uni-segmented-control/uni-segmented-control.vue'
import uniCard from '../../components/uni-card/uni-card.vue'
import uniIcons from '@/components/uni-icons/uni-icons.vue'
import dragButton from '../../components/drag-button/drag-button.vue'
import cmdIcon from "../../components/cmd-icon/cmd-icon.vue"
import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue'
import EvanIcons from '../../components/evan-icons/evan-icons.vue'
import EnglishData from '../../data/English.js'
var _this;
export default {
	
	components: {
		uniSegmentedControl,
		uniCard,
		dragButton,
		cmdIcon,
		uniNavBar,
		uniIcons,
		EvanIcons
	},
	data() {
		return {	
			//将data文件夹中的数据读入
			// EnglishList: EnglishData.data,
			// technologyList: technologyData.data,
			// artList: artData.data,
			// sportsList: sportsData.data,
			FilterText: '',
			area_name: '',
		}
	},
	mounted() {
		_this = this;
	},
	
	methods: {
		EnglishFilterList () {
			var arr = []
			this.EnglishList.forEach((item) => arr.push(item))
			if (this.FilterText) {
				arr = this.EnglishList.filter(item => item.total_iden.includes(this.FilterText)||
					item.total_name.includes(this.FilterText)||
					item.orga_iden.includes(this.FilterText)||
					item.orga_name.includes(this.FilterText)||
					item.material_iden.includes(this.FilterText)||
					item.material_name.includes(this.FilterText)
				)
			}
			return arr
		},
		//切换tab
		onClickItem(e) {
			if (this.current !== e.currentIndex) {
				this.current = e.currentIndex;
			}
		},
		//查看详情
		viewDetail(item) {
						// uni.setStorageSync('viewdetail', material_iden , total_iden);
						uni.setStorageSync('details', item)
						uni.navigateTo({
						    url: '../detail/detail'
						});
	    } ,
		clear1() {
			this.FilterText = ''
		}
	},
	
	onLoad: function() {   
		//登录检查
		// loginMsg = this.checkLogin('../pages/main/main', 'switchTab');
		// if(!loginMsg){
		// 	return;
		// }
		let myinfo = uni.getStorageSync('user_info')
		this.area_name  = myinfo.data.user.area_name
		this.$http.post('/storeManage/totalStock', _this.area_name).then((res) => {
			uni.setStorageSync('EnglishList', res)
		})
		
		// uni.removeStorageSync('viewdetail');
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
		font-size: 28rpx;
		line-height: inherit;
	}
	.content {
		padding: 0;
	}
	.content-control {
		padding: 5upx;
		padding-bottom: 0;
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
		padding-top: 1vw;
	}
	.delete {
		width: 90upx;
		color: red;
	}
	.edit {
		padding-top: 3rpx;
		color: blue;
		width: 90upx;
	}
	.detail {
		width: 90upx;
	}
	.commit {
		width: 90upx;
		color: green;
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

