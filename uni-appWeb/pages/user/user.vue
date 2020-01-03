<template>
    <view class="content">
		<view class="person-head">
			<cmd-avatar src="https://avatar.bbs.miui.com/images/noavatar_small.gif" @click="mydetail" size="md" :make="{'background-color': '#fff', 'margin-right': '10upx'}"></cmd-avatar>
			<view class="person-head-box" @click="mydetail" v-for="info in myInfo" :key="info.id">
				<view class="user-name">{{ info.user_name }}</view>
				<view class="user-id">ID：{{ info.user_id }}</view>
			</view>
		</view>
		<view class="person-list">
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
	import myData from '../../data/userinfo.js'

    export default {
		components: {
			cmdAvatar,
			cmdIcon,
			cmdCellItem
		},
		data() {
			return {
				//将data文件夹中的数据读入
				myInfo: myData.data
			}
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
	.person-head {
		display: flex;
		flex-direction: row;
		align-items: center;
		height: 170upx;
		padding-left: 20px;
		background: linear-gradient(to top, #365fff, #0faeff);
		border-top: 0;
	}
	.person-head-box {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: flex-start;
	}
	.user-name {
		font-size: 18px;
		font-weight: 1000;
		color: #000000;
		font-family: '楷体';
	}
	.user-id {
		font-size: 14px;
		font-weight: 1000;
		color: #000000;
	}
	.person-list {
		background: #FFFFFF;
	}
</style>
