<template>
    <view>
        <view class="feedback-body feedback-uploader">
            <view class="uni-uploader">
                <view class="uni-uploader-head" style="text-align: right;">
                    <view class=""></view>
                    <view class="uni-uploader-info">{{imgList.length}}/{{count}}</view>
                </view>
                <view class="uni-uploader-body">
                    <view class="uni-uploader__files" >
                        <block v-for="(image,index) in imgList" :key="index">
                            <view class="uni-uploader__file" style="position: relative;">
                                <image mode="aspectFill" class="uni-uploader__img" :src="image"></image>
                                <view v-if="index" class="set-capital" style="background: #0A98D5;" @tap="setCapital(index)">设为主图</view>
                                <view v-else class="set-capital">主图</view>
                                <view class="close-view" @click="close(index)">x</view>
                            </view>
                        </block>
                        <view class="uni-uploader__input-box" v-show="imgList.length < count">
                            <view class="uni-uploader__input" @tap="chooseImg"></view>
                        </view>
                    </view>
                </view>
            </view>
        </view>

    </view>
</template>
<script type="text/javascript">
    export default {
        name: 'image-choose',
        props: {

            imgList: {
                //接收的图片列表[{src:12.jpg}]
                type: Array,
                default: function() {
                    return []
                }
            },
            quality: {
                //质量
                type: Number,
                default: 1
            },
            count: {
                //最多数量
                type: Number,
                default: 5
            },
            changes: {
                //监听变化
                type: Function,
                default: null
            }
        },

        data() {
            return {

            }
        },
        watch: {

        },

        methods: {

            chooseImg() { //选择图片
                // console.log('选择图片')
                var count = this.count - this.imgList.length;
                uni.chooseImage({
                    count: count,
                    success: (res) => {
                        var imgs = res.tempFilePaths || [];
                        var count = imgs.length + this.imgList.length;
                        var imgList = this.imgList;
                        if (count <= this.count) {
                            imgList = this.imgList.concat(res.tempFilePaths);
                            this.$emit("changes", imgList);
                        } else {
                            var len = this.count - this.imgList.length;
                            // console.log(len)
                            for (var i = 0; i < len; i++) {
                                imgList.push(res.tempFilePaths[i])
                            }
                            this.$emit("changes", imgList);
                            uni.showToast({
                                title: '最多只能添加' + this.count + '张图片',
                                icon: 'none'
                            })

                        }


                    },
                })
            },
            close(e) {
                var imgList = this.imgList;
                imgList.splice(e, 1);
                this.$emit("changes", imgList);

            },
            setCapital(i, name) {
                var imgList=this.imgList;
                imgList[0]= imgList.splice(i,1,imgList[0])[0];
                this.$emit("changes", imgList);
            },

        }
    }
</script>
<style scoped>
    .set-capital {
        text-align: center;
        line-height: 30px;
        height: 30px;
        padding: 0 5px;
        right: 0;
        /* width: 30px; */
        background: #1AAD19;
        color: #FFFFFF;
        position: absolute;
        bottom: 0px;
        font-size: 12px;
    }

    .close-view {
        text-align: center;
        line-height: 14px;
        height: 16px;
        width: 16px;
        border-radius: 50%;
        background: #FF5053;
        color: #FFFFFF;
        position: absolute;
        top: -6px;
        right: -4px;
        font-size: 12px;
    }
</style>
