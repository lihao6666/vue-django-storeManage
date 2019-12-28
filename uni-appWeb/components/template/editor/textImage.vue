<template>
    <view class="uni-row uni-flex">
        <view class="uni-flex uni-column uni-flex-item" style="">
            <view v-for="(item,idx) in formData" :key="idx" class=" uni-column uni-flex" :class="item.text?'':'red'"
                style="width: 100%;box-sizing: border-box;width: 100%;position: relative;padding:2px 0px;">
                <view class="" style="background: #fff;">
                    <view class="iconfont" style="position: absolute;top: 5px;right: 5px;z-index: 5;font-weight: 600;"
                        @tap="tapContent(item.type,idx)">
                       ✕
                    </view>
                    <view v-if="item.type=='image'" @tap="tapContentImg(idx)" class="uni-flex uni-row" style="padding: 20upx;width: 100%;box-sizing: border-box; background: #FFFFFF;justify-content: center;">

                        <image v-if="item.text" mode="aspectFill" style="height: 200px;width: 100%;" :src="item.text">
                        </image>
                        <view v-else class="uni-flex uni-row" style="text-align: center;font-size:50px ;">
                            +
                        </view>
                    </view>
                    <view v-else-if="item.type=='text'" class="uni-flex uni-row" style="padding: 20upx;width: 100%;box-sizing: border-box; background: #FFFFFF;justify-content: center;">
                        <textarea maxlength="500" auto-height placeholder="请输入内容..." style="background:#f3f3f3;padding: 5px;flex: 1;width: 100%;min-height: 70px;"
                            v-model="item.text"> </textarea>
                    </view>
                </view>

            </view>
        </view>
    </view>
</template>

<script>
    export default {
        props: {
            formData: {
                type: Array,
                default: function() {
                    return []
                }
            }
        },

        data() {
            return {

            }
        },
        methods: {
            tapContentImg(idx) {
                uni.chooseImage({
                    count: 1, //默认9
                    sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
                    sourceType: ['album'], //从相册选择
                    success: (res) => {

                        var formData = this.formData;
                        formData[idx].text = res.tempFilePaths[0]
                        this.$emit('changes', {
                            // type:'add',
                            tap: 'addImage',
                            data: formData,
                            index: idx
                        })
                        // console.log(this.version)
                        // console.log(JSON.stringify(res.tempFilePaths));
                    }
                });
            },

            tapContent(type, idx) {
                this.$emit('changes', {
                    tap: 'button',
                    data: this.formData,
                    index: idx,
                    type
                })

            }
        }
    }
</script>

<style>
</style>
