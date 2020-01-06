<template>
  <view class="content">
	<view class="address-item ">
		<text class="address-item-title">库存组织</text>	
		<text class="address-item-input" @tap="handleTap('picker1')">{{label1}}</text>
		  <lb-picker ref="picker1"
		    v-model="label1"
		   mode="selector"
		   :list="list1"
		    @change="handleChange"
		    @confirm="handleConfirmWithAdd"
		    @cancle="handleCancle">
			</lb-picker>
	</view> 
	 
	<view class="address-item ">
		<text class="address-item-title">需求类型</text>	
		<text class="address-item-input" @tap="handleTap('picker2')">{{label2}}</text>
		  <lb-picker ref="picker2"
		    v-model="label2"
		    mode="selector"
		    :list="list2"
		    @change="handleChange"
		    @confirm="handleConfirmWithType"
		    @cancle="handleCancle">
		</lb-picker>
	</view> 
	
	<view class="address-item ">
		<text class="address-item-title">申请部门</text>	
		<text class="address-item-input" @tap="handleTap('picker3')">{{label3}}</text>
		  <lb-picker ref="picker3"
		    v-model="label3"
		    mode="selector"
		    :list="list3"
		    @change="handleChange"
		    @confirm="handelConfirmWithDepartment"
		    @cancle="handleCancle">
		</lb-picker>
	</view> 
	
	<view class="address-item ">
		<text class="address-item-title">创建时间</text>	
		<text class="address-item-input" @tap="toggleTab('date')">{{label4}}</text>
		 <w-picker
		  	mode="date" 
		  	startYear="2000" 
		  	endYear="2030"
		  	defaultVal="2020-01-01"
		  	:current="false" 
		  	@confirm="handleConfirmWithDate"
		  	:disabledAfter="false"
		  	ref="date" 
		  	themeColor="#f00"
		  ></w-picker>
	</view> 
	
	
	
	<view class="remarks">
		<text class="remarks_text">备注</text>	
		<textarea class="remarks_input" maxlength="200" v-model="remarks" placeholder="请输入,限制200字" auto-height="true"></textarea>
	</view> 
	
	<button class="address-add-btn" @click="confirm">保存</button>
</view>
</template>

<script>
	import {formateDate} from "../../common/catUtil.js"
	import wPicker from "@/components/w-picker/w-picker.vue";
	import lbPicker from "@/components/lb-picker"
	export default {
		components:{
			wPicker,
			lbPicker
		},
		data(){
			return {
				value: '',
				label1: '点击选择',
				label2: '点击选择',
				label3: '点击选择',
				label4: formateDate(new Date(),"Y-M-D"),
				remarks: '',
				list1: [
					{
						label: '合肥',
						value: 'A'
					},
					{
						label: '南京',
						value: 'B'
					}
				],list2:[
					{
						label: '礼品',
						
					},
					{
						label: '教学用品',
						
					},
					{
						label:'销售商品',
						
					},
					{
						label:'办公用品',
						
					},
					{
						label:'市场物资',
						
					}
				],list3:[
					{
						label: '学习中心',
						
					},
					{
						label: '其他部门',
						
					}
				]
			}
		},
		
		methods: {
			toggleTab(str){
				this.$refs[str].show();
			},
			handleTap (picker) {
				this.$refs[picker].show()
			},
			handleChange (item) {
				console.log('change::', item)
			},
			handleConfirmWithAdd(item) {
				this.label1 = item.item.label
				console.log(item)
				console.log('confirm::', item)
			},
			handleConfirmWithType(item) {
				this.label2 = item.item.label
				console.log(item.item.label)
				console.log('confirm::', item)
			},
			handelConfirmWithDepartment(item){
				this.label3 = item.item.label
				console.log(item.item.label)
				console.log('confirm::', item)
			},handleConfirmWithDate(item){
				console.log(item);
				this.label4 = item.result
			},
			handleCancle (item) {
				console.log('cancle::', item)
			}
		}
	}
</script>

<style lang="scss">
	page {
		background-color: #F8F8F8;
	}

	.address-item {
		display: flex;
		align-items: center;
		position: relative;
		padding: 0 30upx;
		height: 100rpx;
		background: #fff;
		border-bottom:1upx solid #F8F8F8;

		.address-item-title {
			flex-shrink: 0;
			width: 200upx;
			font-size: 32upx;
			color: black;
		}

		.address-item-input {
			flex: 1;
			font-size: 32upx;
			color: black;
		}

		
	}
	
	.remarks{
		display: flex;
		align-items: center;
		position: relative;
		padding: 0 30upx;
		background: #fff;
		border-bottom:1upx solid #F8F8F8;
		
		.remarks-text{
			flex-shrink: 0;
			width: 200upx;
			font-size: 32upx;
			color: black;
			align-items: center;
		}
		
		.remarks-input{
			flex: 1;
			font-size: 32upx;
			color: black;
		}
	}

	.default-item {
		.address-item-title {
			flex: 1;
		}
	
		switch {
			transform: scale(.7);
		}
	}

	.address-add-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 690upx;
		height: 80upx;
		margin: 60upx auto;
		font-size: 32upx;
		color: #fff;
		background-color: #DD524D;
		border-radius: 10upx;
	}
</style>