# uni-app picker选择器

插件市场里面的picker选择器不满足自己的需求，所以自己写了一个简单的picker选择器，可扩展、可自定义，一般满足日常需要。

## 功能

1、单选  
2、多级联动，理论支持任意级数  
3、省市区选择，基于多级联动  
4、自定义选择器头部确定取消按钮颜色及插槽支持  
5、选择器可视区自定义滚动个数  
6、自定义数据字段，满足不同人的需求  
7、自定义选择器样式  

## 引入插件

单独引入，在需要使用的页面上import引入即可

```html
<template>
  <view>
    <lb-picker></lb-picker>
  </view>
</template>

<script>
import LbPicker from '@/components/lb-picker'
export default {
  components: {
    LbPicker
  }
}
</script>
```

全局引入，`main.js`中import引入并注册即可全局使用

```jsvascript
import LbPicker from '@/components/lb-picker'
Vue.component("lb-picker", LbPicker)
```

## 调用显示选择器

通过`ref`形式手动调用`show`方法显示，隐藏同理调用`hide`

```javascript
<lb-picker ref="picker"></lb-picker>

this.$refs.picker.show() // 显示
this.$refs.picker.hide() // 隐藏
```

## 绑定值及设置默认值

支持vue中`v-model`写法绑定值

```javascript
<lb-picker v-model="value1"></lb-picker>
<lb-picker v-model="value2"></lb-picker>

data () {
  return {
    value1: '' // 单选
    value2: [] // 多列联动选择
  }
}
```

## 多个选择器

通过设置不同的`ref`，然后调用即可

```javascript
<lb-picker ref="picker1"></lb-picker>
<lb-picker ref="picker2"></lb-picker>

this.$refs.picker1.show() // picker1显示
this.$refs.picker2.show() // picker2显示
```

## 省市区选择

省市区选择是基于多列联动选择，数据来源：[https://github.com/modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China)，  
省市区文件位于`/pages/demos/area-data-min.js`，自行引入即可，可参考`demo3省市区选择`，  
也可使用自己已有的省市区数据，如果数据字段不一样，也可以自定义，参考下方自定义数据字段。

## 自定义数据字段

为了满足不同人的需求，插件支持自定义数据字段名称， 插件默认的数据字段如下形式：

```javascript
[
  {
    label: '选择1',
    value: 1,
    children: []
  },
  {
    label: '选择1',
    value: 1,
    children: []
  }
]
```

如果你的数据字段和上面不一样，如下形式：

```javascript
[
  {
    text: '选择1',
    id: 1,
    child: []
  },
  {
    text: '选择1',
    id: 1,
    child: []
  }
]
```

通过设置参数中的`props`即可，如下所示：

```javascript
<lb-picker :props="myProps"></lb-picker>

data () {
  return {
    myProps: {
      label: 'text',
      value: 'id',
      children: 'child'
    }
  }
}
```

## 插槽使用

选择器支持一些可自定义化的插槽，如选择器的取消和确定文字按钮，如果需要对其自定义处理的话，比如加个icon图标之类的，可使用插槽，使用方法如下：  

```html
<lb-picker>
  <view slot="cancle-text">我是自定义确定</view>
  <view slot="confirm-text">我是自定义取消</view>
</lb-picker>

```

其他插槽见下。

## 其他

其他功能参考示例Demo代码。

## 参数及事件

### Props

| 参数                | 说明                                                  | 类型                | 可选值                 | 默认值                                            |
| :------------------ | :---------------------------------------------------- | :------------------ | :--------------------- | :------------------------------------------------ |
| value/v-model       | 绑定值，联动选择为Array类型                           | String/Number/Array | -                      | -                                                 |
| mode                | 选择器类型，支持单列，多列联动                        | String              | selector/multiSelector | selector                                          |
| list                | 选择器数据                                            | Array               | -                      | -                                                 |
| level               | 多列联动层级，仅mode为multiSelector有效               | Number              | -                      | 2                                                 |
| props               | 自定义数据字段                                        | Object              | -                      | {label:'label',value:'value',children:'children'} |
| cancle-text         | 取消文字                                              | String              | -                      | 取消                                              |
| cancle-color        | 取消文字颜色                                          | String              | -                      | #999999                                           |
| confirm-text        | 确定文字                                              | String              | -                      | 确定                                              |
| confirm-color       | 确定文字颜色                                          | String              | -                      | #007aff                                           |
| column-num          | 可视滚动区域内滚动个数，最好设置奇数值                | Number              | -                      | 5                                                 |
| radius              | 选择器顶部圆角，支持rpx，如radius="10rpx"             | String              | -                      | -                                                 |
| column-style        | 选择器默认样式                                        | Object              | -                      | -                                                 |
| active-column-style | 选择器选中样式                                        | Object              | -                      | -                                                 |
| loading             | 选择器是否显示加载中，可使用loading插槽自定义加载效果 | Boolean             | -                      | -                                                 |

### 方法

| 方法名 | 说明       | 参数 |
| :----- | :--------- | :--- |
| show   | 打开选择器 | -    |
| hide   | 关闭选择器 | -    |

### Events

| 事件名称 | 说明                                     | 回调参数                                                                                                                                                                                                                                                             |
| :------- | :--------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| show     | 选择器打开时触发                         | -                                                                                                                                                                                                                                                                    |
| hide     | 选择器隐藏时触发                         | -                                                                                                                                                                                                                                                                    |
| change   | 选择器滚动时触发，此时不会改变绑定的值   | `{ index, item, value }`   `index`触发滚动后新的索引，单选时是具体的索引值，多列联动选择时为数组。`item`触发滚动后新的的完整内容，包裹`label`、`value`等，单选时为对象，多列选择时为数组对象。`value`触发滚动后新的value值，单列选择时为具体值，多列联动选择时为数组 |
| confirm  | 点击选择器确定时触发，此时会改变绑定的值 | 同上`change`事件说明                                                                                                                                                                                                                                                 |
| cancle   | 点击选择器取消时触发                     | 同上`change`事件说明                                                                                                                                                                                                                                                 |

### 插槽

| 插槽名        | 说明               |
| :------------ | :----------------- |
| cancle-text   | 选择器取消文字插槽 |
| action-center | 选择器顶部中间插槽 |
| confirm-text  | 选择器确定文字插槽 |
| loading       | 选择器loading插槽  |

## Tips

微信小程序端，滚动时在iOS自带振动反馈，可在系统设置 -> 声音与触感 -> 系统触感反馈中关闭  
