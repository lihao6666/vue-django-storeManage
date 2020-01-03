<template>
	<view class="content">
		<view class="person-head">
			<cmd-avatar src="https://avatar.bbs.miui.com/images/noavatar_small.gif" @click="mydetail" size="md" :make="{'background-color': '#fff', 'margin-right': '10upx'}"></cmd-avatar>
		</view>
		<view class="person-list" v-for="info in myInfo" :key="info.id">
			<cmd-cell-item title="姓名" slot-right>{{ info.user_name }}</cmd-cell-item>
			<cmd-cell-item title="工号" slot-right>{{ info.user_id }}</cmd-cell-item>
			<cmd-cell-item title="手机号" slot-right arrow>{{ info.user_phone_number }}</cmd-cell-item>
			<cmd-cell-item title="邮箱" slot-right arrow>{{ info.user_mailbox }}</cmd-cell-item>
			<cmd-cell-item title="区域" slot-right arrow>{{ info.user_area }}</cmd-cell-item>
			<cmd-cell-item title="部门" slot-right arrow>{{ info.user_departments }}</cmd-cell-item>
		</view>
	</view>
</template>

<script>
	import cmdAvatar from "../../components/cmd-avatar/cmd-avatar.vue"
	import cmdCellItem from "../../components/cmd-cell-item/cmd-cell-item.vue"
	import myData from '../../data/userinfo.js'
	
	export default {
		components: {
			cmdAvatar,
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
		padding-left: 44%;
		background: linear-gradient(to top, #365fff, #0faeff);
		border-top: 0;
	}
	.person-list {
		background: #FFFFFF;
	}
</style>
