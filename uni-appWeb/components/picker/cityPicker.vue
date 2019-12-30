<template>
    <div class="mpvue-picker">
        <div :class="{'pickerMask':showPicker}" @click="maskClick" catchtouchmove="true"></div>
        <div class="mpvue-picker-content " :class="{'mpvue-picker-view-show':showPicker}">
            <div class="mpvue-picker__hd" catchtouchmove="true">
                <div class="mpvue-picker__action" @click="pickerCancel">取消</div>
                <div class="mpvue-picker__action" :style="{color:themeColor}" @click="pickerConfirm">确定</div>
            </div>
            <view class="" v-if="dataList && column">
                <picker-view indicator-style="height: 40px;" class="mpvue-picker-view" :value="pickerValue" @change="pickerChange">

                    <picker-view-column v-if="column>0 && dataList[0]">
                        <div class="picker-item" v-for="(item,index) in dataList[0]" :key="index">{{item[label]}}</div>
                    </picker-view-column>
                    <picker-view-column v-if="column>1 && dataList[1]">
                        <div class="picker-item" v-for="(item,index) in dataList[1][pickerValue[0]]" :key="index">{{item[label]}}</div>
                    </picker-view-column>
                    <picker-view-column v-if="column>2 && dataList[2] ">
                        <div class="picker-item" v-for="(item,index) in dataList[2][pickerValue[0]][pickerValue[1]]"
                            :key="index">{{item[label]}}</div>
                    </picker-view-column>

                </picker-view>
            </view>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                column: 0,
                pickerValue: [0],
                /* 是否显示控件 */
                showPicker: false,
            };
        },
        props: {
            value: {
                default () {
                    return 'value'
                }
            },
            label: {
                default () {
                    return 'label'
                }
            },
            dataList: {
                default () {
                    return null;
                }
            },
            col: {
                default () {
                    return 0
                    // return this.dataList.length || 0;
                }
            },
            /* 默认值 */
            pickerValueDefault: {
                type: Array,
                default () {
                    return null
                }
            },
            /* 主题色 */
            themeColor: String
        },
        watch: {
            showPicker(val) {
                if (val) {
                    this.init();
                }
            }
        },
        methods: {
            init() {
                if (!this.col && this.dataList && !isNaN(this.dataList.length)) {
                    // console.log(this.dataList.length)
                    this.column = this.dataList.length;
                } else {
                    this.column = this.col || 1;
                }

                // this.handPickValueDefault(); // 对 pickerValueDefault 做兼容处理
                if (this.pickerValueDefault) {
                    this.pickerValue = this.pickerValueDefault;
                } else if (this.column) {
                    var pickerValue = [];
                    for (var i = 0; i < this.column; i++) {
                        pickerValue.push(0)
                    }
                    this.pickerValue = pickerValue;
                }
            },
            show(state) {
                var state = state || false;

                setTimeout(() => {
                    this.showPicker = state;
                }, 10);
            },
            maskClick() {
                this.pickerCancel();
            },
            pickerCancel() {
                this.showPicker = false;
                this._$emit('onCancel');
            },
            pickerConfirm(e) {
                this.showPicker = false;
                this._$emit('onConfirm');
            },
            showPickerView(state) {
                this.showPicker = state || false;
            },
            pickerChange(e) {

                let changePickerValue = e.mp.detail.value;

                if (this.pickerValue[0] !== changePickerValue[0] && this.column > 1) {

                    // 第一级发生滚动
                    changePickerValue[1] = 0;

                } else if (this.column > 2 && (typeof this.pickerValue[1] != 'number' || this.pickerValue[1] !==
                        changePickerValue[1])) {
                    // 第二级滚动
                    changePickerValue[2] = 0;
                }
                this.pickerValue = changePickerValue;

                this._$emit('onChange');
            },
            _$emit(emitName) {
                let pickObj = {
                    label: this._getLabel(),
                    pickerValue: this.pickerValue,
                    data: this._getAll(),
                };
                this.$emit(emitName, pickObj);
            },
            _getAll() {

                var pickerValue = this.pickerValue
                var All = []
                for (var i = 0; i < pickerValue.length; i++) {
                    switch (i) {
                        case 0:
                            All.push(this.dataList[0][pickerValue[0]])
                            break;
                        case 1:
                            All.push(this.dataList[1][pickerValue[0]][pickerValue[1]])
                            break;
                        case 2:
                            All.push(this.dataList[2][pickerValue[0]][pickerValue[1]][pickerValue[2]])
                            break;
                        default:
                            break;
                    }

                }

                return All
            },
            _getLabel() {
                var label = this.label
                var all = this._getAll();
                var num = all.length - 1;
                var pcikerLabel = '';
                for (var i = 0; i < all.length; i++) {
                    if (i != num) {
                        pcikerLabel = pcikerLabel + all[i][label] + "-";
                    } else {
                        pcikerLabel = pcikerLabel + all[i][label]
                    }
                }
                return pcikerLabel;
            },
            _getValue() {
                var all = this._getAll();
                return all[all.length - 1][this.value];
            }
        }
    };
</script>

<style>
    .pickerMask {
        position: fixed;
        z-index: 1000;
        top: 0;
        right: 0;
        left: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.6);
    }

    .mpvue-picker-content {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        transition: all 0.3s ease;
        transform: translateY(100%);
        z-index: 3000;
    }

    .mpvue-picker-view-show {
        transform: translateY(0);
    }

    .mpvue-picker__hd {
        display: flex;
        padding: 9px 15px;
        background-color: #fff;
        position: relative;
        text-align: center;
        font-size: 17px;
    }

    .mpvue-picker__hd:after {
        content: ' ';
        position: absolute;
        left: 0;
        bottom: 0;
        right: 0;
        height: 1px;
        border-bottom: 1px solid #e5e5e5;
        color: #e5e5e5;
        transform-origin: 0 100%;
        transform: scaleY(0.5);
    }

    .mpvue-picker__action {
        display: block;
        flex: 1;
        color: #1aad19;
    }

    .mpvue-picker__action:first-child {
        text-align: left;
        color: #888;
    }

    .mpvue-picker__action:last-child {
        text-align: right;
    }

    .picker-item {
        text-align: center;
        line-height: 40px;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-size: 16px;
    }

    .mpvue-picker-view {
        position: relative;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 238px;
        background-color: rgba(255, 255, 255, 1);
    }
</style>
