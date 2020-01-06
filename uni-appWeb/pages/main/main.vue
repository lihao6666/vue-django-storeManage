<template>
    <view class="content">
		<uni-nav-bar :fixed="true" background-color="#0faeff" :border="false">
			<view class="input-view"  v-if="current === 0">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="outFilterText" confirm-type="search" class="input" type="text" placeholder="输入出库单信息">
				<uni-icons :color="'#999999'" v-if="outFilterText!==''" class="icon-clear" type="clear" size="22" @click="clear1" />
			</view>
			<view class="input-view"  v-if="current === 1">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="purchaseFilterText" confirm-type="search" class="input" type="text" placeholder="输入请购单信息">
				<uni-icons :color="'#999999'" v-if="purchaseFilterText!==''" class="icon-clear" type="clear" size="22" @click="clear2" />
			</view>
			<view class="input-view"  v-if="current === 2">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="sellFilterText" confirm-type="search" class="input" type="text" placeholder="输入销售订单信息">
				<uni-icons :color="'#999999'" v-if="sellFilterText!==''" class="icon-clear" type="clear" size="22" @click="clear3" />
			</view>
			<view class="input-view"  v-if="current === 3">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="exchangeFilterText" confirm-type="search" class="input" type="text" placeholder="输入转库申请单信息">
				<uni-icons :color="'#999999'" v-if="exchangeFilterText!==''" class="icon-clear" type="clear" size="22" @click="clear4" />
			</view>
		</uni-nav-bar>
		<view class="content-control">
			<uni-segmented-control :current="current" :values="items" @clickItem="onClickItem" style-type="button" active-color="#0faeff"></uni-segmented-control>
		</view>
		<view class="current-content">
			<view v-if="current === 0">
				<view v-for="item in outFilterList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.mso_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.mso_date"
					>
					    <view @click="viewDetail(item.mso_iden)">
							<view>库存组织：{{ item.mso_orga }}</view>
							<view>出库仓库：{{ item.mso_warehouse }}</view>
							<view>出库分类：{{ item.mso_type }}</view>
							<view>出库部门：{{ item.mso_req_department }}</view>
							<view>备注：{{ item.mso_remarks }}</view>
							<view>创建人：{{ item.mso_creator }}</view>
							<view>创建日期：{{ item.mso_createDate }}</view>
						</view>
						<view v-if="judgeStatus(item.mso_status) === 0" class="button-box">
							<view class="delete" @click="deleteOrder(item.mso_iden)">删除</view>
							<view class="edit" @click="editOrder(item.mso_iden)">编辑</view>
							<view class="commit" @click="commitOrder(item.mso_iden)">提交</view>
						</view>
						<view v-if="judgeStatus(item.mso_status) === 1" class="button-box">
							<view class="detail" @click="viewDetail(item.mso_iden)">详情</view>
						</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOrder(current)">
					</drag-button>
				</view>
			</view>
			<view v-if="current === 1">
				<view v-for="item in purchaseFilterList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.rp_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.rp_date"
					>
					    <view @click="viewDetail(item.rp_iden)">
							<view>库存组织：{{ item.rp_orga }}</view>
							<view>需求类型：{{ item.rp_type }}</view>
							<view>申请部门：{{ item.rp_req_department }}</view>
							<view>备注：{{ item.rp_remarks }}</view>
							<view>创建人：{{ item.rp_creator }}</view>
							<view>创建日期：{{ item.rp_createDate }}</view>
						</view>
						<view v-if="judgeStatus(item.rp_status) === 0" class="button-box">
							<view class="delete" @click="deleteOrder(item.rp_iden)">删除</view>
							<view class="edit" @click="editOrder(item.rp_iden)">编辑</view>
							<view class="commit" @click="commitOrder(item.rp_iden)">提交</view>
						</view>
						<view v-if="judgeStatus(item.rp_status) === 1" class="button-box">
							<view class="detail" @click="viewDetail(item.rp_iden)">详情</view>
							<view class="delete" @click="closeOrder(item.rp_iden)">关闭</view>
						</view>
						<view v-if="judgeStatus(item.rp_status) === 2" class="button-box">
							<view class="detail" @click="viewDetail(item.rp_iden)">详情</view>
						</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOrder(current)">
					</drag-button>
				</view>
			</view>
			<view v-if="current === 2">
				<view v-for="item in sellFilterList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.so_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.so_date"
					>
					    <view @click="viewDetail(item.so_iden)">
							<view>库存组织：{{ item.so_orga }}</view>
							<view>出库分类：{{ item.so_type }}</view>
							<view>客户：{{ item.so_custom }}</view>
							<view>发货仓库：{{ item.so_warehouse }}</view>
							<view>备注：{{ item.so_remarks }}</view>
							<view>创建人：{{ item.so_creator }}</view>
							<view>创建日期：{{ item.so_createDate }}</view>
						</view>
						<view v-if="judgeStatus(item.so_status) === 0" class="button-box">
							<view class="delete" @click="deleteOrder(item.so_iden)">删除</view>
							<view class="edit" @click="editOrder(item.so_iden)">编辑</view>
							<view class="commit" @click="commitOrder(item.so_iden)">提交</view>
						</view>
						<view v-if="judgeStatus(item.so_status) === 1" class="button-box">
							<view class="detail" @click="viewDetail(item.so_iden)">详情</view>
						</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOrder(current)">
					</drag-button>
				</view>
			</view>
			<view v-if="current === 3">
				<view v-for="item in exchangeFilterList" :key="item.id" class="card-set">
					<uni-card
					    :title="item.str_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.str_date"
					>
					    <view @click="viewDetail(item.str_iden)">
							<view>库存组织：{{ item.str_orga }}</view>
							<view>转入仓库：{{ item.str_to }}</view>
							<view>转出仓库：{{ item.str_from }}</view>
							<view>申请部门：{{ item.str_req_department }}</view>
							<view>创建人：{{ item.str_creator }}</view>
							<view>创建日期：{{ item.str_createDate }}</view>
						</view>
						<view v-if="judgeStatus(item.str_status) === 0" class="button-box">
							<view class="delete" @click="deleteOrder(item.str_iden)">删除</view>
							<view class="edit" @click="editOrder(item.str_iden)">编辑</view>
							<view class="commit" @click="commitOrder(item.str_iden)">提交</view>
						</view>
						<view v-if="judgeStatus(item.str_status) === 1" class="button-box">
							<view class="detail" @click="viewDetail(item.str_iden)">详情</view>
						</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOrder(current)">
					</drag-button>
				</view>
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
import outData from '../../data/outStore.js'
import purchaseData from '../../data/purchase.js'
import sellData from '../../data/sell.js'
import exchangeData from '../../data/exchange.js'

export default {
	components: {
		uniSegmentedControl,
		uniCard,
		dragButton,
		cmdIcon,
		uniNavBar,
		uniIcons
	},
	data() {
		return {
			items: ['出库','请购','销售','转库'],
			current: 0,
			//将data文件夹中的数据读入
			outList: outData.data,
			purchaseList: purchaseData.data,
			sellList: sellData.data,
			exchangeList: exchangeData.data,
			outFilterText: '',
			purchaseFilterText: '',
			sellFilterText: '',
			exchangeFilterText: ''
		}
	},
	computed: {
		// 单据列表
		outFilterList () {
			var arr = []
			this.outList.forEach((item) => arr.push(item))
			if (this.outFilterText) {
				arr = this.outList.filter(item => item.mso_orga.includes(this.outFilterText))
				if(arr.length === 0) {
					arr = this.outList.filter(item => item.mso_iden.includes(this.outFilterText))
				} 
				if(arr.length === 0) {
					arr = this.outList.filter(item => item.mso_remarks.includes(this.outFilterText))
				} 
				if(arr.length === 0) {
					arr = this.outList.filter(item => item.mso_warehouse.includes(this.outFilterText))
				} 
				if(arr.length === 0) {
					arr = this.outList.filter(item => item.mso_req_department.includes(this.outFilterText))
				}
				if(arr.length === 0) {
					arr = this.outList.filter(item => item.mso_creator.includes(this.outFilterText))
				}
			}
			return arr
		},
		purchaseFilterList () {
			var arr = []
			this.purchaseList.forEach((item) => arr.push(item))
			if (this.purchaseFilterText) {
				arr = this.purchaseList.filter(item => item.rp_orga.includes(this.purchaseFilterText))
				if(arr.length === 0) {
					arr = this.purchaseList.filter(item => item.rp_iden.includes(this.purchaseFilterText))
				} 
				if(arr.length === 0) {
					arr = this.purchaseList.filter(item => item.rp_remarks.includes(this.purchaseFilterText))
				} 
				if(arr.length === 0) {
					arr = this.purchaseList.filter(item => item.rp_type.includes(this.purchaseFilterText))
				} 
				if(arr.length === 0) {
					arr = this.purchaseList.filter(item => item.rp_req_department.includes(this.purchaseFilterText))
				}
				if(arr.length === 0) {
					arr = this.purchaseList.filter(item => item.rp_creator.includes(this.purchaseFilterText))
				}
			}
			return arr
		},
		sellFilterList () {
			var arr = []
			this.sellList.forEach((item) => arr.push(item))
			if (this.sellFilterText) {
				arr = this.sellList.filter(item => item.so_orga.includes(this.sellFilterText))
				if(arr.length === 0) {
					arr = this.sellList.filter(item => item.so_remarks.includes(this.sellFilterText))
				} 
				if(arr.length === 0) {
					arr = this.sellList.filter(item => item.so_iden.includes(this.sellFilterText))
				} 
				if(arr.length === 0) {
					arr = this.sellList.filter(item => item.so_warehouse.includes(this.sellFilterText))
				} 
				if(arr.length === 0) {
					arr = this.sellList.filter(item => item.so_type.includes(this.selFilterText))
				}
				if(arr.length === 0) {
					arr = this.sellList.filter(item => item.so_creator.includes(this.sellFilterText))
				}
				if(arr.length === 0) {
					arr = this.sellList.filter(item => item.so_custom.includes(this.sellFilterText))
				}
			}
			return arr
		},
		exchangeFilterList () {
			var arr = []
			this.exchangeList.forEach((item) => arr.push(item))
			if (this.exchangeFilterText) {
				arr = this.exchangeList.filter(item => item.str_orga.includes(this.exchangeFilterText))
				if(arr.length === 0) {
					arr = this.exchangeList.filter(item => item.str_iden.includes(this.exchangeFilterText))
				} 
				if(arr.length === 0) {
					arr = this.exchangeList.filter(item => item.str_to.includes(this.exchangeFilterText))
				} 
				if(arr.length === 0) {
					arr = this.exchangeList.filter(item => item.str_from.includes(this.exchangeFilterText))
				} 
				if(arr.length === 0) {
					arr = this.exchangeList.filter(item => item.str_req_department.includes(this.exchangeFilterText))
				}
				if(arr.length === 0) {
					arr = this.exchangeList.filter(item => item.str_creator.includes(this.exchangeFilterText))
				}
			}
			return arr
		}
	},
	methods: {
		//切换tab
		onClickItem(e) {
			if (this.current !== e.currentIndex) {
				this.current = e.currentIndex;
			}
		},
		//判断订单状态
		judgeStatus(status) {
			if (status === "草稿") {
				return 0;
			}
			else if(status === "已审批") {
				return 1;
			}
			else if(status === "已关闭") {
				return 2;
			}
		},
		//查看订单详情
		viewDetail(iden) {
			var diff = iden[0]+iden[1]
			if(diff === "MS") {
				try {
				    uni.setStorageSync('viewout', iden);
				} catch (e) {
				    console.log("传出库单单号失败")
				}
				uni.navigateTo({
				    url: '../detail/outDetails',
				});
			} else if(diff === "PR") {
				try {
				    uni.setStorageSync('viewpurchase', iden);
				} catch (e) {
				    console.log("传请购单单号失败")
				}
				uni.navigateTo({
				    url: '../detail/purchaseDetails',
				});
			} else if(diff === "SO") {
				try {
				    uni.setStorageSync('viewsell', iden);
				} catch (e) {
				    console.log("传销售单单号失败")
				}
				uni.navigateTo({
				    url: '../detail/sellDetails',
				});
			} else if(diff === "ST") {
				try {
				    uni.setStorageSync('viewexchange', iden);
				} catch (e) {
				    console.log("传转库申请单单号失败")
				}
				uni.navigateTo({
				    url: '../detail/exchangeDetails',
				});
			}
		},
		//新增单据
		newOrder(page) {
			if(page === 0) {
				uni.navigateTo({
				    url: '../user/phoneus',
				});
			} else if(page === 1) {
				uni.navigateTo({
				    url: '../requisitions/requisitions',
				});
			} else if(page === 2) {
				uni.navigateTo({
				    url: '../user/setting',
				});
			} else if(page === 3) {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			}
		},
		//删除单据
		deleteOrder(iden) {
			var diff = iden[0]+iden[1]
			if(diff === "MS") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
				            
				        } else if (res.cancel) {
				           
				        }
				    }
				});
			} else if(diff === "PR") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
							
				        } else if (res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "SO") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
							
				        } else if (res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "ST") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
							
				        } else if (res.cancel) {
				            
				        }
				    }
				});
			}
		},
		//提交草稿
		commitOrder(iden) {
			var diff = iden[0]+iden[1]
			if(diff === "MS") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
				            
				        } else if (res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "PR") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
							
				        } else if (res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "SO") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
							
				        } else if (res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "ST") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
							
				        } else if (res.cancel) {
				            
				        }
				    }
				});
			}
		},
		//编辑草稿
		editOrder(iden) {
			var diff = iden[0]+iden[1]
			if(diff === "MS") {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			} else if(diff === "PR") {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			} else if(diff === "SO") {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			} else if(diff === "ST") {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			}
		},
		//关闭订单
		closeOrder(iden) {
			uni.showModal({
			    title: '提示',
			    content: '确认关闭请购单：'+iden+" ?",
			    success: function (res) {
			        if (res.confirm) {
			            
			        } else if (res.cancel) {
			            console.log('用户点击取消');
			        }
			    }
			});
		},
		clear1() {
			this.outFilterText = ''
		},
		clear2() {
			this.purchaseFilterText = ''
		},
		clear3() {
			this.sellFilterText = ''
		},
		clear4() {
			this.exchangeFilterText = ''
		}

	},
	
	onLoad: function() {   
		//登录检查
		// loginMsg = this.checkLogin('../pages/main/main', 'switchTab');
		// if(!loginMsg){
		// 	return;
		// }
		uni.removeStorageSync('viewout');
		uni.removeStorageSync('viewpurchase');
		uni.removeStorageSync('viewsell');
		uni.removeStorageSync('viewexchange');
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
