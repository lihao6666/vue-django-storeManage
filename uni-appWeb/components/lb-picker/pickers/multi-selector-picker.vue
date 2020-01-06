<template>
  <view class="multi-selector picker-item"
    :style="{height: height}">
    <picker-view :value="pickerValue"
      :indicator-style="indicatorStyle"
      :style="{height: height}"
      @change="handleChange">
      <picker-view-column v-for="(column, index) in pickerColumns"
        :key="index">
        <view v-for="(item, i) in column"
          :class="['lb-picker-column', item[props.value] === selectValue[index] ? 'lb-picker-column-active' : '']"
          :key="setColumnKey(item, i)"
          :style="{height: columnHeight, 'line-height': columnHeight}">
          <view class="lb-picker-column-label"
            :style="[item[props.value] === selectValue[index] ? activeColumnStyle : columnStyle]">
            {{ item[props.label] }}
          </view>
        </view>
      </picker-view-column>
    </picker-view>
  </view>
</template>

<script>
import '../style/picker-item.scss'
import { isArray, getIndicatorHeight } from '../utils.js'
const indicatorHeight = getIndicatorHeight()
export default {
	props: {
		value: Array,
		list: Array,
		props: Object,
		columnKey: String,
		level: Number,
		keep: {
			type: Boolean,
			default: true
		},
		visible: Boolean,
		height: String,
		columnStyle: Object,
		activeColumnStyle: Object
	},
	data() {
		return {
			pickerValue: [],
			pickerColumns: [],
			selectValue: [],
			selectItem: [],
			columnHeight: indicatorHeight + 'px',
			indicatorStyle: `height: ${indicatorHeight}px`
		}
	},
	created () {
		this.init()
	},
	methods: {
		init () {
			const defaultValue = this.value || []
			this.setPickerItems(this.list)
			this.$emit('change', {
				value: this.selectValue,
				item: this.selectItem,
				index: this.pickerValue,
				init: true
			})
		},
		handleChange (item) {
			const pickerValue = item.detail.value
			const columnIndex = pickerValue.findIndex((item, i) => item !== this.pickerValue[i] )
			const valueIndex = pickerValue[columnIndex]
			this.setPickerChange(pickerValue, valueIndex, columnIndex)
		},
		setPickerChange (pickerValue, valueIndex, columnIndex) {
			for (let i = 0; i < pickerValue.length; i++) {
				if (i > columnIndex) {
					pickerValue[i] = 0
					const column = this.pickerColumns[i-1][valueIndex] || this.pickerColumns[i-1][0]
					this.$set(this.pickerColumns, i, column[this.props.children] || [])
				}
				this.selectItem[i] = this.pickerColumns[i][pickerValue[i]]
				this.selectValue[i] = this.selectItem[i][this.props.value]
			}
			this.pickerValue = pickerValue
			this.$emit('change', {
				value: this.selectValue,
				item: this.selectItem,
				index: this.pickerValue
			})
		},
		setPickerItems (list = [], index = 0) {
			const defaultValue = this.value || []
			if (index < this.level && list.length) {
				const value = defaultValue[index] || ''
				let i = list.findIndex(item => item[this.props.value] === value)
				i = i > -1 ? i : 0
				this.$set(this.pickerValue, index, i)
				this.$set(this.pickerColumns, index, list)
				this.$set(this.selectValue, index, list[i][this.props.value])
				this.$set(this.selectItem, index, list[i])
				this.setPickerItems(list[i][this.props.children] || [], index + 1)
			}
		},
		setColumnKey (column, i) {
			return this.columnKey ? column[this.columnKey] : i
		}
	},
	watch: {
		visible (newVisible) {
			if (newVisible && !this.keep) {
				this.init()	
			}
		},
		list () {
			this.init()
		}	
	}
}
</script>
