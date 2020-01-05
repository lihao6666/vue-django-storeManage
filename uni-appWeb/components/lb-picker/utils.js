export function isArray(val) {
	return Object.prototype.toString.call(val) === '[object Array]'
}

export function getIndicatorHeight() {
	return Math.round(uni.getSystemInfoSync().screenWidth / (750 / 100))
}