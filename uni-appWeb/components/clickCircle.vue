<template>
	<view class="circle" v-if="circleShow == 1" :style="isCricle" :class="circleShow==1?ainimaChoose:''"></view>
</template>

<script>
	export default {
		name: 'clickCircle',
		data() {
			return {
				isReady:1,
				isCricle:'',
				circleShow:0,
				ainimaChoose:''
			};
		},
		created() {
			if(Math.random() >= 0.5) {
				this.ainimaChoose = 'animation0'
			} else{
				this.ainimaChoose = 'animation1'
			}
		},
		methods:{
			conClick(e){
				var isReady = this.isReady
				if (isReady === 1) {
					// #ifdef H5
					var isTop = Math.round(e.changedTouches[0].clientY) + 15 + 'px'
					var isLeft = Math.round(e.changedTouches[0].clientX) - 25 + 'px'
					// #endif
					// #ifndef H5
					  var isTop = Math.round(e.changedTouches[0].clientY) - 25 + 'px'
					  var isLeft = Math.round(e.changedTouches[0].clientX) - 25 + 'px'
					// #endif
					this.isCricle = `top:${isTop};left:${isLeft};`
					this.circleShow = 1
					this.isReady = 0
					var that = this
				  setTimeout(() => {
					  that.circleShow = 0
					  that.isReady = 1
				  }, 300)
				}
			}
		}
	}
</script>

<style lang="scss">
	.circle{
	width: 100upx;
	height: 100upx;
	border-radius: 100%;
	position: fixed;
	z-index: 999;
	}
	
	
	// 动画0
	.animation0::before, .animation0::after {
  position: absolute;
  content: '';
  display: block;
  width: 140%;
  height: 100%;
  left: -20%;
  z-index: -1000;
  transition: all ease-in-out 0.5s;
  background-repeat: no-repeat;
}
	
	.animation0::before{
		  display: none;
		  top: -55%;
		  background-image: radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, transparent 20%, #ff0081 20%, transparent 30%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, transparent 10%, #ff0081 15%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%);
		  background-size: 10% 10%, 20% 20%, 15% 15%, 20% 20%, 18% 18%, 10% 10%, 15% 15%, 10% 10%, 18% 18%;
	}
	.animation0::after{
		  display: none;
		  bottom: -55%;
		  background-image: radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, transparent 10%, #ff0081 15%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%), radial-gradient(circle, #ff0081 20%, transparent 20%);
		  background-size: 15% 15%, 20% 20%, 18% 18%, 20% 20%, 15% 15%, 10% 10%, 20% 20%;
	}
	
	
	.animation0::before{
	display: block;
	animation: topBubbles ease-in-out 0.75s forwards;
	}
	.animation0::after{
		display: block;
	animation: bottomBubbles ease-in-out 0.75s forwards;
	}
	
	@keyframes topBubbles {
  0% {
    background-position: 5% 90%, 10% 90%, 10% 90%, 15% 90%, 25% 90%, 25% 90%, 40% 90%, 55% 90%, 70% 90%;
  }
  50% {
    background-position: 0% 80%, 0% 20%, 10% 40%, 20% 0%, 30% 30%, 22% 50%, 50% 50%, 65% 20%, 90% 30%;
  }
  100% {
    background-position: 0% 70%, 0% 10%, 10% 30%, 20% -10%, 30% 20%, 22% 40%, 50% 40%, 65% 10%, 90% 20%;
    background-size: 0% 0%, 0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%;
  }
}
@keyframes bottomBubbles {
  0% {
    background-position: 10% -10%, 30% 10%, 55% -10%, 70% -10%, 85% -10%, 70% -10%, 70% 0%;
  }
  50% {
    background-position: 0% 80%, 20% 80%, 45% 60%, 60% 100%, 75% 70%, 95% 60%, 105% 0%;
  }
  100% {
    background-position: 0% 90%, 20% 90%, 45% 70%, 60% 110%, 75% 80%, 95% 70%, 110% 10%;
    background-size: 0% 0%, 0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%;
  }
}

	// 动画1
	.animation1{
	animation: shockwave 0.3s 0s linear;
	}
	@keyframes shockwave {
	  0% {
	    transform: scale(1);
	    box-shadow: 0 0 2px rgba(0, 0, 0, 0.15), inset 0 0 1px rgba(0, 0, 0, 0.15);
	  }
	  95% {
	    box-shadow: 0 0 50px rgba(0, 0, 0, 0), inset 0 0 30px rgba(0, 0, 0, 0);
	  }
	  100% {
	    transform: scale(2.25);
	  }
	}
	
	
</style>
