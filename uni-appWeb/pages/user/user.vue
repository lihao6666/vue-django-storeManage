<template>
    <view class="content">
		<view class="personHead">
			<cmd-avatar src="https://avatar.bbs.miui.com/images/noavatar_small.gif" @click="mydetail" size="md" :make="{'background-color': '#fff', 'margin-right': '10upx'}"></cmd-avatar>
			<view class="personHeadBox">
				<view class="userName">俞浩然</view>
				<view class="userId">ID：123456789</view>
			</view>
		</view>
		<view class="personList">
			<cmd-cell-item title="联系我们" slot-left arrow @click="phone">
			  <cmd-icon type="phone" size="24" color="#368dff"></cmd-icon>
			</cmd-cell-item>
			<cmd-cell-item title="系统设置" slot-left arrow @click="setting">
			  <cmd-icon type="settings" size="24" color="#368dff"></cmd-icon>
			</cmd-cell-item>
		</view>
    </view>
</template>

<script>
	import cmdAvatar from "../../components/cmd-avatar/cmd-avatar.vue"
	import cmdIcon from "../../components/cmd-icon/cmd-icon.vue"
	import cmdCellItem from "../../components/cmd-cell-item/cmd-cell-item.vue"

    export default {
		components: {
			cmdAvatar,
			cmdIcon,
			cmdCellItem
		},
        methods: {
			mydetail() {
				uni.navigateTo({
				    url: 'myinfo',
				});
			},
			phone() {
				uni.navigateTo({
				    url: 'phoneus',
				});
			},
			setting() {
				uni.navigateTo({
				    url: 'setting',
				});
			}
        }
    }
</script>

<style>
	.content {
		padding: 0;
	}
	.personHead {
		display: flex;
		flex-direction: row;
		align-items: center;
		height: 170upx;
		padding-left: 20px;
		background: linear-gradient(to top, #365fff, #0faeff);
		border-top: 0;
	}
	.personHeadBox {
		border-radius: 10upx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: flex-start;
	}
	.userName {
		font-size: 18px;
		font-weight: 1000;
		color: #000000;
		font-family: '楷体';
	}
	.userId {
		font-size: 14px;
		font-weight: 1000;
		color: #000000;
	}
	.personList {
		background: #FFFFFF;
	}
</style>
