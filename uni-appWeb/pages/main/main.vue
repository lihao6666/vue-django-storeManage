<template>
    <view class="content">
		<view class="content-control">
			<uni-segmented-control :current="current" :values="items" @clickItem="onClickItem" style-type="button" active-color="#0faeff"></uni-segmented-control>
		</view>
		<view class="current-content">
			<view v-if="current === 0">
				<!-- <input v-model="filterText" type="text" placeholder="设备编号,设备名称" ></input> -->
				<view v-for="item in outList" :key="item.id" class="card-set">
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
				<view v-for="item in purchaseList" :key="item.id" class="card-set">
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
				<view v-for="item in sellList" :key="item.id" class="card-set">
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
				<view v-for="item in exchangeList" :key="item.id" class="card-set">
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
							<view>备注：{{ item.str_remarks }}</view>
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
import dragButton from '../../components/drag-button/drag-button.vue'
import cmdIcon from "../../components/cmd-icon/cmd-icon.vue"
import outData from '../../data/outStore.js'
import purchaseData from '../../data/purchase.js'
import sellData from '../../data/sell.js'
import exchangeData from '../../data/exchange.js'

export default {
	components: {
		uniSegmentedControl,
		uniCard,
		dragButton,
		cmdIcon
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
			// filterText: ''
		}
	},
	// computed:{
	// 	filterList () {
	// 		var arr = []
	// 		this.outList.forEach((item) => arr.push(item))
	// 		if (this.filterText) {
	// 			arr = this.outList.filter(item => item.mso_status.includes(this.filterText))
	// 		}
	// 		return arr
	// 	}
	// },
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
		//新增单据
		newOrder(page) {
			if(page === 0) {
				uni.navigateTo({
				    url: '../user/phoneus',
				});
			} else if(page === 1) {
				uni.navigateTo({
				    url: '../user/myinfo',
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
				            uni.navigateTo({
				                url: '../user/myinfo',
				            });
				        } else if (res.cancel) {
				            console.log('用户点击取消');
				        }
				    }
				});
			} else if(diff === "PR") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
							uni.navigateTo({
								url: '../user/myinfo',
							});
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
							uni.navigateTo({
								url: '../user/myinfo',
							});
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
							uni.navigateTo({
								url: '../user/myinfo',
							});
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
				            uni.navigateTo({
				                url: '../user/myinfo',
				            });
				        } else if (res.cancel) {
				            console.log('用户点击取消');
				        }
				    }
				});
			} else if(diff === "PR") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (res) {
				        if (res.confirm) {
							uni.navigateTo({
								url: '../user/myinfo',
							});
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
							uni.navigateTo({
								url: '../user/myinfo',
							});
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
							uni.navigateTo({
								url: '../user/myinfo',
							});
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
			            uni.navigateTo({
			                url: '../user/myinfo',
			            });
			        } else if (res.cancel) {
			            console.log('用户点击取消');
			        }
			    }
			});
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
