<template>
	
	<view class="content">
		<view class="address-item " @click="showCityPicker">
			<text class="address-item-title">库存组织</text>
			<text class="address-item-input">
				{{addressData.organization}}
			</text>
		</view>
		<view class="address-item " >
			<text class="address-item-title">需求类型</text>
			
		</view>
		<view class="address-item " @click="showCityPicker">
			<text class="address-item-title">申请部门</text>
			<text class="address-item-input">
				{{addressData.department}}
			</text>
		</view>
		<view class="address-item ">
			<text class="address-item-title">电话</text>
			<input class="address-item-input" type="number" v-model="addressData.mobile" placeholder="收货人手机号"  />
		</view>
		<view class="address-item " @click="showCityPicker">
			<text class="address-item-title">地区</text>
			<text class="address-item-input">
				{{addressData.label}}
			</text>
		</view>
		
		<view class="address-item ">
			<text class="address-item-title">邮政编码</text>
			<input class="address-item-input" type="text" v-model="addressData.postcode" placeholder="邮政编码"  />
		</view>

		<view class="address-item default-item">
			<text class="address-item-title">设为默认</text>
			<switch :checked="addressData.default==1" color='#d81e06' @change="switchChange" />
		</view>
		
		<button class="address-add-btn" @click="confirm">保存</button>
		<button class="address-add-btn" @click="cancel">取消</button>
		<mpvue-city-picker :themeColor="themeColor" ref="mpvueCityPicker" :pickerValueDefault="cityPickerValueDefault"
		 @onCancel="onCancel" @onConfirm="onConfirm"></mpvue-city-picker>
	</view>
</template>

<script>
	import mpvueCityPicker from '../../components/mpvue-citypicker/mpvueCityPicker.vue'
	
	
	export default {
		components: {
			mpvueCityPicker
		},
		data() {
			return {
				addressData: {
					name: '',
					mobile: '',
					organization:'请选择库存组织',
					type:'选择需求类型',
					label: '选择省/市/区',
					department:'选择部门',
					address: '',
					default: false,
					remarks:'不超过200字'
				}
		}
		},onLoad(option){
			
		},
		methods: {
			switchChange(e) {
				this.addressData.default = e.detail.value?1:0;
			},

			//提交
			confirm() {
				let data = this.addressData;
				if (!data.name) {
					this.$msg('请填写收货人姓名');
					return;
				}
				if (!/(^1[0-9]{10}$)/.test(data.mobile)) {
					this.$msg('请输入正确的手机号');
					return;
				}
				if (!data.label) {
					this.$msg('请选择地区信息');
					return;
				}
				if (!data.address) {
					this.$msg('请输入详细地址');
					return;
				}
				this.$msg('保存成功')
			},
			// 三级联动选择
			showCityPicker() {
				this.$refs.mpvueCityPicker.show()
				console.log('showpicker')
			},
			onConfirm(e) {
				console.log(e)
				this.addressData.label=e.label

			},
			onCancel(){
				
			},
			showTypePicker(){
				this.$refs.mpvuetypepicker.show()
				console.log('showpicker')
			},
			onTypePickerConfirm(e){
				console.log(e)
				this.addressData.type=e.type
			}
			
		},
		onBackPress() {
			if (this.$refs.mpvueCityPicker.showPicker) {
				this.$refs.mpvueCityPicker.pickerCancel();
				return true;
			}
		},
		onUnload() {
			if (this.$refs.mpvueCityPicker.showPicker) {
				this.$refs.mpvueCityPicker.pickerCancel()
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
		height: 100upx;
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
		margin: 10rpx;
		font-size: 32upx;
		color: #fff;
		background-color: #DD524D;
		border-radius: 10upx;
	}
</style>
