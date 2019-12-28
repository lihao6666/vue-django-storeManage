<template>

        <view class="uni-page-body uni-content-info">
            <view class='cropper-content'>
                <view v-if="isShowImg" class="uni-corpper" :style="'width:'+cropperInitW+'px;height:'+cropperInitH+'px;background:#000'">
                    <view class="uni-corpper-content" :style="'width:'+cropperW+'px;height:'+cropperH+'px;left:'+cropperL+'px;top:'+cropperT+'px'">
                        <image :src="imageSrc" :style="'width:'+cropperW+'px;height:'+cropperH+'px'"></image>
                        <view class="uni-corpper-crop-box" @touchstart.stop="contentStartMove" @touchmove.stop="contentMoveing"
                            @touchend.stop="contentTouchEnd" :style="'left:'+cutL+'px;top:'+cutT+'px;right:'+cutR+'px;bottom:'+cutB+'px'">
                            <view class="uni-cropper-view-box">
                                <view class="uni-cropper-point point-rb" data-drag="rightBottom" @touchstart.stop="dragStart"
                                    @touchmove.stop="dragMove"></view>
                            </view>
                        </view>
                    </view>
                </view>
            </view>
            <view class='cropper-config' style="width: 100%;">
                <button type="primary reverse" @click="getImage" style='margin-top: 30upx;width: 100%;'> 选择图片 </button>
                <button type="warn" @click="getImageInfo" style='margin-top: 30upx;width: 100%;'>确认 </button>
            </view>
            <canvas canvas-id="myCanvas" :style="'position:absolute;border: 1px solid red; width:'+imageW+'px;height:'+imageH+'px;top:-9999px;left:-9999px;'"></canvas>
        </view>
</template>

<script>
    // import Storage from "../../common/yc_js/Storage.js";
    let sysInfo = uni.getSystemInfoSync();
    let SCREEN_WIDTH = sysInfo.screenWidth
    let PAGE_X, // 手按下的x位置
        PAGE_Y, // 手按下y的位置 
        PR = sysInfo.pixelRatio, // dpi
        T_PAGE_X, // 手移动的时候x的位置
        T_PAGE_Y, // 手移动的时候Y的位置
        CUT_L, // 初始化拖拽元素的left值
        CUT_T, // 初始化拖拽元素的top值
        CUT_R, // 初始化拖拽元素的
        CUT_B, // 初始化拖拽元素的
        CUT_W, // 初始化拖拽元素的宽度
        CUT_H, //  初始化拖拽元素的高度
        IMG_RATIO, // 图片比例
        IMG_REAL_W, // 图片实际的宽度
        IMG_REAL_H, // 图片实际的高度
        DRAFG_MOVE_RATIO = 1, //移动时候的比例,
        INIT_DRAG_POSITION = 100, // 初始化屏幕宽度和裁剪区域的宽度之差，用于设置初始化裁剪的宽度
        DRAW_IMAGE_W = sysInfo.screenWidth // 设置生成的图片宽度
    // var  ctx = uni.createCanvasContext('myCanvas');
    export default {
        props: {
            num: {
                type: Number,
                default: 1
            },
            imgSrc: {
                type: String,
                default: 'https://img-cdn-qiniu.dcloud.net.cn/demo_crop.jpg'
            },
            // 宽高比
            W_H_ratio: {
                type: Number,
                default: 1
            },
            // 宽边长度像素
            maxW: {
                type: Number,
                default: 1280
            }
        },
        mounted(e) {
            this.$nextTick(() => {
                // console.log(this.imgSrc)
                // this.imageSrc=this.imgSrc
                this.loadImage();
            })

        },
        /**
         * 页面的初始数据
         */
        data() {
            return {
                imageSrc: this.imgSrc,
                isShowImg: false,
                // minW:100,//图片的宽高短边像素
                // 初始化的宽高
                cropperInitW: SCREEN_WIDTH,
                cropperInitH: SCREEN_WIDTH,
                // 动态的宽高
                cropperW: SCREEN_WIDTH,
                cropperH: SCREEN_WIDTH,
                // 动态的left top值
                cropperL: 0,
                cropperT: 0,

                transL: 0,
                transT: 0,

                // 图片缩放值
                scaleP: 0,
                imageW: 0,
                imageH: 0,

                // 裁剪框 宽高
                cutL: 0, //裁剪框移动位置left
                cutT: 0, //top
                cutB: SCREEN_WIDTH, //bottom
                cutR: 0, //right
                qualityWidth: DRAW_IMAGE_W,
                innerAspectRadio: DRAFG_MOVE_RATIO,

                // W_H_ratio:0.8,//宽高比
            }
        },
        watch: {
            imageSrc(e) {

            }
        },
        methods: {
            setData: function(obj) {
                let that = this;
                Object.keys(obj).forEach(function(key) {
                    that.$set(that.$data, key, obj[key])
                });
            },
            getImage: function() {
                var count = this.num;
                uni.chooseImage({
                    count: count,
                    success: (res) =>{
                        this.imageSrc = res.tempFilePaths[0];
                        this.loadImage();
                    },
                })
            },
            loadImage: function() {
                var _this = this;
                // console.log( _this.imageSrc)
                if(this.imageSrc){
                     uni.showLoading({
                        title: '图片加载中...',
                    })
                    setTimeout(function() {
                        uni.hideLoading();
                    }, 2000);
                    uni.getImageInfo({
                        src: this.imageSrc,
                        success: (res)=> {
                            IMG_RATIO = res.width / res.height; //获得图片实际的宽高比
                            // 裁剪区域上下左右边距
                            let cutT = 0;
                            let cutL = 0;
                            let surplus = 0;
                            // let duanbian=SCREEN_WIDTH;//短边长度
                            // 保持屏幕能完全显示图片 ，以图片短边为基准铺满屏幕宽度
                            if (IMG_RATIO >= 1) {
                                // duanbian=SCREEN_WIDTH;
                                var cropperW = SCREEN_WIDTH;
                                var cropperH = SCREEN_WIDTH / IMG_RATIO;
                                // 								// 初始化left right
                                var cropperL = Math.ceil((SCREEN_WIDTH - SCREEN_WIDTH) / 2);
                                var cropperT = Math.ceil((SCREEN_WIDTH - SCREEN_WIDTH / IMG_RATIO) / 2);
                    
                                IMG_REAL_W = SCREEN_WIDTH;
                                IMG_REAL_H = SCREEN_WIDTH / IMG_RATIO;
                    
                                if (this.W_H_ratio > 1) {
                                    cutT = (IMG_REAL_H - (IMG_REAL_W / this.W_H_ratio)) / 2;
                                } else {
                                    cutL = (IMG_REAL_W - (IMG_REAL_H * this.W_H_ratio)) / 2;
                                }
                            } else {
                                var cropperW = SCREEN_WIDTH * IMG_RATIO; //屏幕可视区域图片底片宽度
                                var cropperH = SCREEN_WIDTH; //屏幕可视区域图片底片高度
                                // 初始化left right
                                var cropperL = Math.ceil((SCREEN_WIDTH - SCREEN_WIDTH * IMG_RATIO) / 2);
                                var cropperT = Math.ceil((SCREEN_WIDTH - SCREEN_WIDTH) / 2);
                    
                                IMG_REAL_W = SCREEN_WIDTH * IMG_RATIO; //裁剪区域图片的宽度
                                IMG_REAL_H = SCREEN_WIDTH; //裁剪区域图片的高度
                    
                                //以最长边为基准计算另一边
                                if (this.W_H_ratio > 1) {
                                    cutT = (IMG_REAL_H - (IMG_REAL_W / this.W_H_ratio)) / 2;
                                } else {
                                    cutT = (IMG_REAL_H - (IMG_REAL_W / this.W_H_ratio)) / 2;
                                    // cutL =(IMG_REAL_H-(IMG_REAL_W/_this.W_H_ratio))/2; 
                                }
                    
                            }
                            // console.log({IMG_REAL_W,IMG_REAL_H,cutT,cutL,surplus})
                            let minRange = IMG_REAL_W > IMG_REAL_H ? IMG_REAL_W : IMG_REAL_H;
                            INIT_DRAG_POSITION = minRange > INIT_DRAG_POSITION ? INIT_DRAG_POSITION :
                                minRange;
                    
                            let cutB = cutT;
                            let cutR = cutL;
                            // console.log({cropperW,cropperH})
                            this.setData({
                                cropperW: cropperW,
                                cropperH: cropperH,
                                // 初始化left right
                                cropperL: cropperL,
                                cropperT: cropperT,
                    
                                cutL: cutL,
                                cutT: cutT,
                                cutR: cutR,
                                cutB: cutB,
                                // 图片缩放值
                                imageW: IMG_REAL_W,
                                imageH: IMG_REAL_H,
                                scaleP: IMG_REAL_W / SCREEN_WIDTH,
                                qualityWidth: DRAW_IMAGE_W,
                                innerAspectRadio: IMG_RATIO
                            })
                            this.setData({
                                isShowImg: true
                            })
                            uni.hideLoading()
                        }
                    })
                    
                }
               
            },
            // 拖动时候触发的touchStart事件
            contentStartMove(e) {
                PAGE_X = e.touches[0].pageX
                PAGE_Y = e.touches[0].pageY
            },

            // 拖动时候触发的touchMove事件
            contentMoveing(e) {

                var dragLengthX = (PAGE_X - e.touches[0].pageX) * DRAFG_MOVE_RATIO
                var dragLengthY = (PAGE_Y - e.touches[0].pageY) * DRAFG_MOVE_RATIO
                // 左移
                if (dragLengthX > 0) {
                    if (this.cutL - dragLengthX < 0) dragLengthX = this.cutL
                } else {
                    if (this.cutR + dragLengthX < 0) dragLengthX = -this.cutR
                }

                if (dragLengthY > 0) {
                    if (this.cutT - dragLengthY < 0) dragLengthY = this.cutT
                } else {
                    if (this.cutB + dragLengthY < 0) dragLengthY = -this.cutB
                }
                this.setData({
                    cutL: this.cutL - dragLengthX,
                    cutT: this.cutT - dragLengthY,
                    cutR: this.cutR + dragLengthX,
                    cutB: this.cutB + dragLengthY
                })

                PAGE_X = e.touches[0].pageX
                PAGE_Y = e.touches[0].pageY
            },

            contentTouchEnd() {

            },

            // 获取图片
            getImageInfo() {
                var _this = this;
                uni.showLoading({
                    title: '图片生成中...',
                });
                setTimeout(function() {
                    uni.hideLoading();

                }, 10000);
                // 将图片写入画布
                var ctx = uni.createCanvasContext('myCanvas', this);

                ctx.drawImage(this.imageSrc, 0, 0, IMG_REAL_W, IMG_REAL_H);
                // console.log(ctx)
                ctx.draw(true, (e) => {
                    // 获取画布要裁剪的位置和宽度   均为百分比 * 画布中图片的宽度    保证了在微信小程序中裁剪的图片模糊  位置不对的问题 canvasT = (_this.cutT / _this.cropperH) * (_this.imageH / pixelRatio)
                    var canvasW = ((_this.cropperW - _this.cutL - _this.cutR) / _this.cropperW) * IMG_REAL_W;
                    var canvasH = ((_this.cropperH - _this.cutT - _this.cutB) / _this.cropperH) * IMG_REAL_H;
                    var canvasL = (_this.cutL / _this.cropperW) * IMG_REAL_W;
                    var canvasT = (_this.cutT / _this.cropperH) * IMG_REAL_H;
                    var fileType = _this.imageSrc.replace(/^.+\./, '');
                    if (fileType == 'png') {
                        fileType = 'png';
                    } else {
                        fileType = 'jpg';
                    }
                    // console.log(fileType)
                    uni.canvasToTempFilePath({
                        x: canvasL,
                        y: canvasT,
                        width: canvasW,
                        height: canvasH,
                        destWidth: canvasW,
                        destHeight: canvasH,
                        quality: 0.5,
                        canvasId: 'myCanvas',
                        fileType: fileType,
                        success: (res) => {
                            res.fileType = fileType;
                            uni.hideLoading()
                            _this.$emit("changes", res);
                        }
                    }, this);
                });
            },

            // 设置大小的时候触发的touchStart事件
            dragStart(e) {
                T_PAGE_X = e.touches[0].pageX
                T_PAGE_Y = e.touches[0].pageY
                CUT_L = this.cutL
                CUT_R = this.cutR
                CUT_B = this.cutB
                CUT_T = this.cutT
            },

            // 设置大小的时候触发的touchMove事件
            dragMove(e) {

                var _this = this
                var dragType = e.target.dataset.drag
                switch (dragType) {
                    case 'rightBottom':
                        var dragLengthX = (T_PAGE_X - e.touches[0].pageX) * DRAFG_MOVE_RATIO
                        var dragLengthY = (T_PAGE_Y - e.touches[0].pageY) * DRAFG_MOVE_RATIO

                        if (CUT_B + dragLengthY < 0) dragLengthY = -CUT_B
                        if (CUT_R + dragLengthX < 0) dragLengthX = -CUT_R
                        let cutB = CUT_B + dragLengthY;
                        let cutR = CUT_R + dragLengthX;
                        // console.log({cutB,cutR,CUT_B,CUT_R,dragLengthY,dragLengthX})

                        //计算画布被选中区域宽-高
                        var canvasW = ((this.cropperW - this.cutL - cutR) / this.cropperW) * IMG_REAL_W;
                        var canvasH = ((this.cropperH - this.cutT - cutB) / this.cropperH) * IMG_REAL_H;
                        var W_H_ratio = this.W_H_ratio;
                        //以最长边为基准计算另一边
                        if (this.W_H_ratio > 1) {
                            canvasH = canvasW / W_H_ratio
                        } else {
                            canvasW = canvasH * W_H_ratio;
                        }

                        cutR = IMG_REAL_W - this.cutL - canvasW;
                        cutB = IMG_REAL_H - canvasH - this.cutT;
                        // 超出边框就不取值了
                        if (cutR >= 0 && cutB >= 0) {
                            this.setData({
                                cutB: cutB,
                                cutR: cutR
                            })
                        }

                        break;
                    default:
                        break;
                }
            }
        }
    }
</script>

<style>
    /* pages/uni-cropper/index.wxss */

    .uni-content-info {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: block;
        align-items: center;
        flex-direction: column;
    }

    .cropper-config {
        padding: 20upx 0upx;
    }

    .cropper-content {
        min-height: 750upx;
        width: 100%;
    }

    .uni-corpper {
        position: relative;
        overflow: hidden;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        -webkit-tap-highlight-color: transparent;
        -webkit-touch-callout: none;
        box-sizing: border-box;
    }

    .uni-corpper-content {
        position: relative;
    }

    .uni-corpper-content image {
        display: block;
        width: 100%;
        min-width: 0 !important;
        max-width: none !important;
        height: 100%;
        min-height: 0 !important;
        max-height: none !important;
        image-orientation: 0deg !important;
        margin: 0 auto;
    }

    /* 移动图片效果 */

    .uni-cropper-drag-box {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        cursor: move;
        background: rgba(0, 0, 0, 0.6);
        z-index: 1;
    }

    /* 内部的信息 */

    .uni-corpper-crop-box {
        position: absolute;
        background: rgba(255, 255, 255, 0.3);
        z-index: 2;
    }

    .uni-corpper-crop-box .uni-cropper-view-box {
        position: relative;
        display: block;
        width: 100%;
        height: 100%;
        overflow: visible;
        outline: 1upx solid #69f;
        outline-color: rgba(102, 153, 255, .75)
    }

    /* 横向虚线 */

    .uni-cropper-dashed-h {
        position: absolute;
        top: 33.33333333%;
        left: 0;
        width: 100%;
        height: 33.33333333%;
        border-top: 1upx dashed rgba(255, 255, 255, 0.5);
        border-bottom: 1upx dashed rgba(255, 255, 255, 0.5);
    }

    /* 纵向虚线 */

    .uni-cropper-dashed-v {
        position: absolute;
        left: 33.33333333%;
        top: 0;
        width: 33.33333333%;
        height: 100%;
        border-left: 1upx dashed rgba(255, 255, 255, 0.5);
        border-right: 1upx dashed rgba(255, 255, 255, 0.5);
    }

    /* 四个方向的线  为了之后的拖动事件*/

    .uni-cropper-line-t {
        position: absolute;
        display: block;
        width: 100%;
        background-color: #69f;
        top: 0;
        left: 0;
        height: 1upx;
        opacity: 0.1;
        cursor: n-resize;
    }

    .uni-cropper-line-t::before {
        content: '';
        position: absolute;
        top: 50%;
        right: 0upx;
        width: 100%;
        -webkit-transform: translate3d(0, -50%, 0);
        transform: translate3d(0, -50%, 0);
        bottom: 0;
        height: 41upx;
        background: transparent;
        z-index: 11;
    }

    .uni-cropper-line-r {
        position: absolute;
        display: block;
        background-color: #69f;
        top: 0;
        right: 0upx;
        width: 1upx;
        opacity: 0.1;
        height: 100%;
        cursor: e-resize;
    }

    .uni-cropper-line-r::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        width: 41upx;
        -webkit-transform: translate3d(-50%, 0, 0);
        transform: translate3d(-50%, 0, 0);
        bottom: 0;
        height: 100%;
        background: transparent;
        z-index: 11;
    }

    .uni-cropper-line-b {
        position: absolute;
        display: block;
        width: 100%;
        background-color: #69f;
        bottom: 0;
        left: 0;
        height: 1upx;
        opacity: 0.1;
        cursor: s-resize;
    }

    .uni-cropper-line-b::before {
        content: '';
        position: absolute;
        top: 50%;
        right: 0upx;
        width: 100%;
        -webkit-transform: translate3d(0, -50%, 0);
        transform: translate3d(0, -50%, 0);
        bottom: 0;
        height: 41upx;
        background: transparent;
        z-index: 11;
    }

    .uni-cropper-line-l {
        position: absolute;
        display: block;
        background-color: #69f;
        top: 0;
        left: 0;
        width: 1upx;
        opacity: 0.1;
        height: 100%;
        cursor: w-resize;
    }

    .uni-cropper-line-l::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        width: 41upx;
        -webkit-transform: translate3d(-50%, 0, 0);
        transform: translate3d(-50%, 0, 0);
        bottom: 0;
        height: 100%;
        background: transparent;
        z-index: 11;
    }

    .uni-cropper-point {
        width: 5upx;
        height: 5upx;
        background-color: #69f;
        opacity: .75;
        position: absolute;
        z-index: 3;
    }

    .point-t {
        top: -3upx;
        left: 50%;
        margin-left: -3upx;
        cursor: n-resize;
    }

    .point-tr {
        top: -3upx;
        left: 100%;
        margin-left: -3upx;
        cursor: n-resize;
    }

    .point-r {
        top: 50%;
        left: 100%;
        margin-left: -3upx;
        margin-top: -3upx;
        cursor: n-resize;
    }

    .point-rb {
        padding: 10px;
        border-radius: 50%;
        bottom: 0;
        right: 0;
        -webkit-transform: translate3d(-50%, -50%, 0);
        transform: translate3d(-50%, -50%, 0);
        cursor: n-resize;
        background-color: #69f;
        position: absolute;
        z-index: 1112;
        opacity: 1;
    }

    .point-b {
        left: 50%;
        top: 100%;
        margin-left: -3upx;
        margin-top: -3upx;
        cursor: n-resize;
    }

    .point-bl {
        left: 0%;
        top: 100%;
        margin-left: -3upx;
        margin-top: -3upx;
        cursor: n-resize;
    }

    .point-l {
        left: 0%;
        top: 50%;
        margin-left: -3upx;
        margin-top: -3upx;
        cursor: n-resize;
    }

    .point-lt {
        left: 0%;
        top: 0%;
        margin-left: -3upx;
        margin-top: -3upx;
        cursor: n-resize;
    }

    /* 裁剪框预览内容 */

    .uni-cropper-viewer {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }

    .uni-cropper-viewer image {
        position: absolute;
        z-index: 2;
    }
</style>
