<template>
	<view class="content">
		<view class="person-head">
			<cmd-avatar src="https://avatar.bbs.miui.com/images/noavatar_small.gif" size="md" :make="{'background-color': '#fff', 'margin-right': '10upx'}"></cmd-avatar>
		</view>
		<view class="person-list">
			<cmd-cell-item title="姓名" slot-right>{{ user_name }}</cmd-cell-item>
			<cmd-cell-item title="工号" slot-right>{{ user_id }}</cmd-cell-item>
			<cmd-cell-item title="手机号" slot-right arrow>{{ user_phone_number }}</cmd-cell-item>
			<cmd-cell-item title="邮箱" slot-right arrow>{{ user_mailbox }}</cmd-cell-item>
			<cmd-cell-item title="区域" slot-right>{{ user_area }}</cmd-cell-item>
			<cmd-cell-item title="部门" slot-right>{{ user_departments }}</cmd-cell-item>
			<cmd-cell-item title="角色" slot-right>{{ user_roles }}</cmd-cell-item>
		</view>
	</view>
</template>

<script>
	import cmdAvatar from "../../components/cmd-avatar/cmd-avatar.vue"
	import cmdCellItem from "../../components/cmd-cell-item/cmd-cell-item.vue"
	var _this;
	
	export default {
		components: {
			cmdAvatar,
			cmdCellItem
		},
		data() {
			return {
				//将data文件夹中的数据读入
				user_name: '',
				user_id: '',
				user_phone_number: '',
				user_mailbox: '',
				user_area: '',
				user_departments: '',
				user_roles: ''
			}
		},
		methods: {
			
		},
		mounted() {
			_this = this
		},
		onLoad: function() {
			var myinfo = uni.getStorageSync('user_info')
			this.user_name = myinfo.data.user.user_name
			this.user_id = myinfo.data.user.username
			this.user_phone_number = myinfo.data.user.user_phone_number
			this.user_mailbox = myinfo.data.user.email
			this.user_area = myinfo.data.user.area_name
			this.user_departments = myinfo.data.user.user_departments
			for(var i=0; i<myinfo.data.roles.length; i++){
				if(i < myinfo.data.roles.length-1) {
					this.user_roles += myinfo.data.roles[i][0] + '、'
				} else {
					this.user_roles += myinfo.data.roles[i][0]
				}
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
		background: linear-gradient(to top, #365fff, #20a0ff);
		border-top: 0;
	}
	.person-list {
		background: #FFFFFF;
	}
</style>
