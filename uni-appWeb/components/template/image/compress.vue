<template>
    <view>
        <view style="position:fixed;top:9999px;">
            <canvas :style="'width:'+imageW+'px;height:'+imageH+'px;'" canvas-id="myCanvas"></canvas>
        </view>
    </view>
</template>

<script>
    // 图片批量压缩使用说明  返回值h5=base64 字符串，微信小程序/h5+ 返回=图片地址链接
    // 父页面<compress ref="compress" :maxwh="maxwh=720" :quality="quality=0.8" @changes="callback =function(e){}"> </compress>
    // 两种使用方式 
    // 1监听changes函数获得处理完成返回执
    // 2 使用 this.$refs.compress.yasuoImg(['bold:eqweew.jpg','bold:'fdsfdsf,jpg']).then(e=>{
    //                        console.log(e) //返回值
    //                    })
    export default {
        name: 'image-compress',
        props: {
            quality: {
                //质量
                type: Number,
                default: 1
            },
            maxwh: {
                //最大宽高尺寸像素
                type: Number,
                default: 1920
            },
            changes: {
                //监听变化
                type: Function,
                default: null
            }
        },

        data() {
            return {
                imageW: this.maxwh,
                imageH: this.maxwh,
                redio: 1,
            }
        },
        methods: {
            yasuo(img) {
                return new Promise((resolve, reject) => {
                    uni.getImageInfo({
                        src: img,
                        success: (res) => {
                            var ratio = parseFloat(res.width / res.height); //获得图片实际的宽高比
                            var width = res.width;
                            var height = res.height;
                            // console.log(this.maxwh)
                            var maxwh = this.maxwh;
                            if (width > maxwh || height > maxwh) {
                                if (width > height) {
                                    width = maxwh;
                                    height = parseInt(width / ratio);
                                } else {
                                    height = maxwh;
                                    width = parseInt(height * ratio);
                                }
                            }

                            this.imageW = width;
                            this.imageH = height;
                            // 将图片写入画布
                            var ctx = uni.createCanvasContext('myCanvas', this);
                            ctx.drawImage(res.path, 0, 0, width, height);
                            // console.log(ctx)
                            ctx.draw(true, (e) => {
                                // console.log(e)
                                // 获取画布要裁剪的位置和宽度   均为百分比 * 画布中图片的宽度  
                                var fileType = res.path.replace(/^.+\./, '');
                                if (fileType == 'png') {
                                    fileType = 'png';
                                } else {
                                    fileType = 'jpg';
                                }
                                // console.log(fileType)
                                uni.canvasToTempFilePath({
                                    x: 0,
                                    y: 0,
                                    width: width,
                                    height: height,
                                    destWidth: width,
                                    destHeight: height,
                                    quality: this.quality,
                                    canvasId: 'myCanvas',
                                    fileType: fileType,
                                    success: (res2) => {
                                        // console.log(res)
                                        res2.oldWidth = res.width;
                                        res2.oldHeight = res.height;
                                        res2.width = width;
                                        res2.height = height;
                                        res2.path = res.path;
                                        res2.fileType = fileType;
                                        resolve(res2)


                                    }
                                }, this);
                            });

                        }
                    })
                })
            },
            yasuoImg(imgs, val) {

                var val = val || [];
                var imgs = imgs;

                // 批量压缩逻辑部分
                if (typeof imgs == 'object') {

                    if (imgs.length) {
                      return  this.yasuo(imgs[0]).then(e => {
                            val.push(e)
                            var imgs2 = [];
                            for (var i = 0; i < imgs.length; i++) {
                                if (i != 0) {
                                    imgs2.push(imgs[i])
                                }
                            }
                            return this.yasuoImg(imgs2, val)
                            // this.yasuoImg(imgs2, val).then(e => {
                            //     // 压缩完成一张图，进行下一次
                            //     resolve(e)
                            // })

                        })

                    } else {
                        return new Promise((resolve, reject) => {
                            // var resolves = resolves || resolve;
                            // 全部处理完 验收返回压缩后的内容
                            resolve(val)
                            this.$emit("changes", val);
                        })
                    }
                } else {
                    // 单图压缩逻辑部分
                    return new Promise((resolve, reject) => {
                        this.yasuoImg(imgs).then(e => {
                            resolve(val)
                            this.$emit("changes", val);
                        })
                    })
                }

            }
        }

    }
</script>

<style>
</style>
