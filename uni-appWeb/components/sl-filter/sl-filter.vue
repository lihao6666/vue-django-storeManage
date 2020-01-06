<template>
	<view class="content">
		<view :style="{height: tabHeight + 1 +'px'}">
			<view :class="topFixed?'select-tab-fixed-top':'select-tab'" :style="{height: tabHeight+'px'}">
				<view class="select-tab-item" :style="{width: itemWidth}" v-for="(item,index) in titleList" :key="index" @tap="showMenuClick(index)">
					<text :style="{color:color}">{{item.title}}</text>
					<text class="arrows sl-font" :class="statusList[index].isActive?up:down"></text>
				</view>
			</view>
		</view>
		<popup-layer ref="popupRef" :direction="'bottom'" @close="close" :isTransNav="isTransNav" :navHeight="navHeight"
		 :tabHeight="tabHeight">
			<sl-filter-view :ref="'slFilterView'" :independence="independence" :themeColor="themeColor" :menuList.sync="menuListTemp"
			 ref="slFilterView" @confirm="filterResult"></sl-filter-view>
		</popup-layer>
	</view>

</template>

<script>
	import popupLayer from '@/components/sl-filter/popup-layer.vue';
	import slFilterView from '@/components/sl-filter/filter-view.vue';
	export default {
		components: {
			popupLayer,
			slFilterView
		},
		props: {
			menuList: {
				type: Array,
				default () {
					return []
				}
			},
			themeColor: {
				type: String,
				default () {
					return '#000000'
				}
			},
			color: {
				type: String,
				default () {
					return '#666666'
				}
			},
			independence: {
				type: Boolean,
				default: false
			},
			isTransNav: {
				type: Boolean,
				default: false
			},
			navHeight: {
				type: Number,
				default: 0
			},
			topFixed: {
				type: Boolean,
				default: false
			}
		},

		computed: {
			itemWidth() {
				return 'calc(100%/2)'
			},
			menuListTemp: {
				get() {
					return this.getMenuListTemp();
				},
				set(newObj) {
					return newObj;
				}
			}
		},
		// #ifndef H5
		onReady: function() {
			let arr = [];
			let titleArr = [];
			let r = {};
			for (let i = 0; i < this.menuList.length; i++) {
				arr.push({
					'isActive': false
				});
				// titleArr.push({
				// 	'title': this.menuList[i].title,
				// 	'key': this.menuList[i].key
				// })

				r[this.menuList[i].key] = this.menuList[i].title;

				if (this.menuList[i].reflexTitle && this.menuList[i].defaultSelectedIndex > -1) {
					titleArr.push({
						'title': this.menuList[i].detailList[this.menuList[i].defaultSelectedIndex].title,
						'key': this.menuList[i].key
					})
				} else {
					titleArr.push({
						'title': this.menuList[i].title,
						'key': this.menuList[i].key
					})
				}

			}
			this.statusList = arr;
			this.titleList = titleArr;
			this.tempTitleObj = r;
		},
		// #endif

		// #ifdef H5
		created: function() {
			let arr = [];
			let titleArr = [];
			let r = {};
			for (let i = 0; i < this.menuList.length; i++) {
				arr.push({
					'isActive': false
				});
				// titleArr.push({
				// 	'title': this.menuList[i].title,
				// 	'key': this.menuList[i].key
				// });
				r[this.menuList[i].key] = this.menuList[i].title;

				if (this.menuList[i].reflexTitle && this.menuList[i].defaultSelectedIndex > -1) {
					titleArr.push({
						'title': this.menuList[i].detailList[this.menuList[i].defaultSelectedIndex].title,
						'key': this.menuList[i].key
					})
				} else {
					titleArr.push({
						'title': this.menuList[i].title,
						'key': this.menuList[i].key
					})
				}

			}
			this.statusList = arr;
			this.titleList = titleArr;
			this.tempTitleObj = r;
		},
		// #endif
		data() {
			return {
				down: 'sl-down',
				up: 'sl-up',
				tabHeight: 50,
				statusList: [],
				selectedIndex: '',
				titleList: [],
				tempTitleObj: {}
			};
		},
		methods: {
			getMenuListTemp() {
				let arr = this.menuList;
				for (let i = 0; i < arr.length; i++) {
					let item = arr[i];
					for (let j = 0; j < item.detailList.length; j++) {
						let d_item = item.detailList[j];
						if (j == 0) {
							d_item.isSelected = true
						} else {
							d_item.isSelected = false
						}
					}
				}
				return arr;
			},
			// 重置所有选项，包括默认选项，并更新result
			resetAllSelect(callback) {
				this.$refs.slFilterView.resetAllSelect(function(e){
					callback(e);
				});
			},
			// 重置选项为设置的默认值，并更新result
			resetSelectToDefault(callback) {
				this.$refs.slFilterView.resetSelectToDefault(function(e){
					callback(e);
				});
			},
			resetMenuList(val) {
				this.menuList = val;
				this.$emit('update:menuList', val)
				this.$forceUpdate();
				this.$refs.slFilterView.resetMenuList(val)
			},
			showMenuClick(index) {
				this.selectedIndex = index;
				if (this.statusList[index].isActive == true) {
					this.$refs.popupRef.close();
					this.statusList[index].isActive = false
				} else {
					this.menuTabClick(index);
					this.$refs.popupRef.show()
				}
			},
			menuTabClick(index) {
				this.$refs.slFilterView.menuTabClick(index);
				for (let i = 0; i < this.statusList.length; i++) {
					if (index == i) {
						this.statusList[i].isActive = true;
					} else {
						this.statusList[i].isActive = false;
					}
				}
			},
			filterResult(obj) {
				let val = obj.result;
				let titlesObj = obj.titles;
				// 处理选项映射到菜单title
				if (this.independence) {
					if (!this.menuList[this.selectedIndex].isMutiple || this.menuList[this.selectedIndex].isSort) {
						let tempTitle = '';
						for (let i = 0; i < this.menuList[this.selectedIndex].detailList.length; i++) {
							let item = this.menuList[this.selectedIndex].detailList[i];
							if (item.value == val[this.menuList[this.selectedIndex].key]) {
								tempTitle = item.title;
							}
						}
						if (this.menuList[this.selectedIndex].reflexTitle) {
							this.titleList[this.selectedIndex].title = tempTitle;
						}
					}
				} else {
					for (let key in titlesObj) {
						if (!Array.isArray(titlesObj[key])) {
							this.tempTitleObj[key] = titlesObj[key];
						}

					}
					for (let key in this.tempTitleObj) {
						for (let i = 0; i < this.titleList.length; i++) {
							if (this.titleList[i].key == key) {
								this.titleList[i].title = this.tempTitleObj[key];
							}
						}
					}
				}

				this.$refs.popupRef.close()
				if (obj.isReset) {
					
				} else{
					this.$emit("result", val)
				}
				

			},
			close() {
				for (let i = 0; i < this.statusList.length; i++) {
					this.statusList[i].isActive = false;
				}
			}
		}
	}
</script>

<style>
	@import 'iconfont/iconfont.css';

	.select-tab {
		border-bottom: #F7F7F7 1px solid;
		background-color: #FFFFFF;
		display: flex;
		width: 100%;
	}

	.select-tab-fixed-top {
		border-bottom: #F7F7F7 1px solid;
		background-color: #FFFFFF;
		display: flex;
		width: 100%;
		position: fixed;
		/* #ifdef H5 */
		top: 44px;
		/* #endif */
		/* #ifndef H5 */
		top: 0;
		/* #endif */
	}

	.arrows {
		margin-left: 5px;
	}

	.select-tab .select-tab-item,
	.select-tab-fixed-top .select-tab-item {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.select-tab .select-tab-item text,
	.select-tab-fixed-top .select-tab-item text {
		color: #666666;
		font-size: 14px;
	}
</style>
