<template>
  <view class="content">
	<view class="order" >
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
			<text class="address-item-title">申请时间</text>	
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
			<text class="remarks_text" >备注</text>	
			<textarea class="remarks_input" maxlength="200" v-model="remarks" placeholder="请输入,限制200字"></textarea>
		</view> 
	</view>  	
	<view class = "card">
		<view v-for="(item,index) in materialsDisplay" :key="index" class="card-item">
			<uni-card class="card_style"
				:title="item.material_name"
				mode="basic" 
				:is-shadow="true" 
				:extra="item.material_iden"
			>
				<view>物料编码：{{ item.material_iden }}</view>
				<view>物料名称：{{ item.material_name }}</view>
				<view>规格：{{ item.material_specification }}</view>
				<view>型号：{{ item.material_model }}</view>
				<view>计量单位：{{ item.material_meterage }}</view>
				<view>存货量：{{ item.material_attr }}</view>
				<view>选择数量：{{ item.material_num }}</view>
				<view>备注：{{item.material_remarks}}</view>
			</uni-card>
		</view>
	</view>
	<view class="shop">
		<view class="cart">
			<text class="address-add-btn4" >到底了</text>
		</view>
	</view>
	
	<view class="shopcart">
		<!-- @click="toggleList" -->
		<view class="cartBottom">
			<view class="carIcon">
				<button class="address-add-btn1" @click="cancel">取消</button>
			</view>
			<view class="middle">
				<button class="address-add-btn2" @click="hold">保存</button>
			</view>
			<view class="BtnRight">
				<button class="address-add-btn3" @click="confirm">提交</button>
			</view>
		</view>
	</view>
</view>
</template>

<script>
	import {formateDate} from "../../common/catUtil.js"
	import uniCard from "../../components/uni-card/uni-card.vue"
	import wPicker from "@/components/w-picker/w-picker.vue";
	import lbPicker from "@/components/lb-picker"
	export default {
		components:{
			wPicker,
			lbPicker,
			uniCard
		},
		computed:{
			materialsDisplay (){
				let arr = []
				
				arr = uni.getStorageSync('purchase_select')
				
				console.log(arr)
				
				return arr
			}
			
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
					},{
						label: '杭州',
						value: 'C'
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
			},
			cancel(){
				uni.switchTab({url:'../main/main'})
			},
			hold(){
				uni.switchTab({url:'../main/main'})
			},
			confirm(){
				uni.switchTab({url:'../main/main'})
			},
			select(){
				uni.navigateTo({
					url:'purchaseMaterials'
				})
			},
			
		}
	}
</script>

<style lang="scss">
	page {
		background-color: #F8F8F8;
		width: 100%
	}
	
	.order {
		height:50vh;
		box-sizing: border-box;
		margin-bottom:10rpx ;
		flex-direction: column;
		flex: 1;
		display: flex;
		
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
	
	.card{
		font-size: 25upx;
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
			font-size: 32upx;
			color: black;
			// align-items: center;
		}
		
		.remarks-input{
			flex: 1;
			font-size: 32upx;
			color: black;
		}
	}
	
	// .card-item{
	// 	display: flex;
	// 	align-items: center;
	// 	padding: 0 30upx;
	// 	height: 100rpx;
	// 	background: #fff;
	// 	border-bottom:1upx solid #F8F8F8;
		
	// 	.card-style{
	// 		font-size: 16px;
			
	// 	}
	// }

	.default-item {
		.address-item-title {
			flex: 1;
		}
	
		switch {
			transform: scale(.7);
		}
	}
	
	
	
	// .shop .cart{
	// 	position: fixed;
	// 	bottom: 50px;
	// 	left: 0;
	// 	right: 0;
	// 	height: 50px;
	// 	z-index: 99;
	// 	display: flex;
	// 	background-color: #141d27;
	// }
	
	
	
	.shopcart .cartBottom {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		height: 50px;
		z-index: 99;
		display: flex;
		background-color: #141d27;
	}

	.address-add-btn1 {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 125px;
		height: 80upx;
		margin: 10upx auto;
		font-size: 32upx;
		color: #fff;
		background-color: #DD524D;
		border-radius: 10upx;
	}
	
	.address-add-btn2 {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 125px;
		height: 80upx;
		margin: 10upx auto;
		font-size: 32upx;
		color: #fff;
		background-color: #20a0ff;
		border-radius: 10upx;
		
	}
	
	.address-add-btn3 {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 125px;
		height: 80upx;
		margin: 10upx auto;
		font-size: 32upx;
		color: #fff;
		background-color: #1aa034;
		border-radius: 10upx;
		
	}
	
	.address-add-btn4 {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 690upx;
		height: 80upx;
		margin: 60upx auto;
		font-size: 32upx;
		color: #fff;
		background-color: #f9cc9d;
		border-radius: 10upx;
		position: relative;
		bottom: 22px;
	}
</style>