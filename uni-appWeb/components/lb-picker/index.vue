<template>
  <view class="lb-picker">
    <view class="lb-picker-mask"
      v-show="visible"
      @tap="visible = false">
    </view>
    <view :class="['lb-picker-container', visible ? 'lb-picker-toggle' : '']"
      :style="{borderRadius: `${radius} ${radius} 0 0`}">
      <view class="lb-picker-header"
        :style="{height: pickerHeaderHeight, 'line-height': pickerHeaderHeight}">
        <view class="lb-picker-action lb-picker-left">
          <view class="lb-picker-action-cancle"
            @tap="handleCancle">
            <slot v-if="$slots['cancle-text']"
              name="cancle-text">
            </slot>
            <view v-else
              class="action-cancle-text"
              :style="{color: cancleColor}">
              {{ cancleText }}
            </view>
          </view>
        </view>

        <view class="lb-picker-action lb-picker-center"
          v-if="$slots['action-center']">
          <slot name="action-center"></slot>
        </view>

        <view class="lb-picker-action lb-picker-right">
          <view class="lb-picker-action-confirm"
            @tap="handleConfirm">
            <slot v-if="$slots['confirm-text']"
              name="confirm-text">
            </slot>
            <view v-else
              class="action-confirm-text"
              :style="{color: confirmColor}">
              {{ confirmText }}
            </view>
          </view>
        </view>
      </view>
      <view class="lb-picker-content"
        :style="{height: pickerContentHeight}">

        <!-- loading -->
        <view v-if="loading"
          class="lb-picker-loading">
          <slot name="loading">
            <view class="lb-picker-loading-img"></view>
          </slot>
        </view>

        <!-- 单选 -->
        <selector-picker v-if="mode === 'selector' && !loading"
          :value="value"
          :list="list"
          :props="pickerProps"
          :height="pickerContentHeight"
          :column-style="columnStyle"
          :active-column-style="activeColumnStyle"
          @change="handleChange">
        </selector-picker>

        <!-- 多列联动 -->
        <multi-selector-picker v-if="mode === 'multiSelector' && !loading"
          :value="value"
          :list="list"
          :level="level"
          :visible="visible"
          :props="pickerProps"
          :height="pickerContentHeight"
          :column-style="columnStyle"
          :active-column-style="activeColumnStyle"
          @change="handleChange">
        </multi-selector-picker>
      </view>
    </view>
  </view>
</template>

<script>
	const defaultProps = {
		label: 'label',
		value: 'value',
		children: 'children'
	}
	import './style/picker.scss'
	import { getIndicatorHeight } from './utils'
	import SelectorPicker from './pickers/selector-picker'
	import MultiSelectorPicker from './pickers/multi-selector-picker'
	const indicatorHeight = getIndicatorHeight()
	export default {
		components: {
			SelectorPicker,
			MultiSelectorPicker
		},
		props: {
			value: [String, Number, Array],
			list: Array,
			mode: {
				type: String,
				default: 'selector'
			},
			level: {
				type: Number,
				default: 2
			},
			props: {
				type: Object
			},
			cancleText: {
				type: String,
				default: '取消'
			},
			cancleColor: String,
			confirmText: {
				type: String,
				default: '确定'
			},
			confirmColor: String,
			canHide: {
				type: Boolean,
				default: true
			},
			columnNum: {
				type: Number,
				default: 5
			},
			radius: String,
			columnStyle: Object,
			activeColumnStyle: Object,
			loading: Boolean
		},
		data(){
			return {
				visible: false,
				myValue: this.value,
				picker: {},
				pickerHeaderHeight: indicatorHeight + 'px',
				pickerContentHeight: indicatorHeight * (this.columnNum) + 'px'
			}
		},
		computed: {
			pickerProps () {
				return Object.assign({}, defaultProps, this.props)
			}
		},
		methods: {
			show () {
				this.visible = true
			},
			hide () {
				this.visible = false
			},
			handleCancle () {
				this.$emit('cancle', this.picker)
				if (this.canHide) {
					this.hide()
				}
			},
			handleConfirm () {
				const picker = JSON.parse(JSON.stringify(this.picker))
				this.myValue = picker.value
				this.$emit('confirm', this.picker)
				if (this.canHide) {
					this.hide()
				}
			},
			handleChange ({ value, item, index, init }) {
				this.picker.value = value
				this.picker.item = item
				this.picker.index = index
				if (!init) {
					this.$emit('change', this.picker)
				}
			}
		},
		watch: {
			value (newVal) {
				this.myValue = newVal
			},
			myValue (newVal) {
				this.$emit('input', newVal)
			},
			visible (newVisible) {
				if (newVisible) {
					this.$emit('show')
				} else {
					this.$emit('hide')
				}
			}
		}
	}
</script>
