import Vue from 'vue'
import SellSod from '@/components/basic_data/Brand'
describe('Brand', () => {
  // 检查原始组件选项
  it('has a created hook', () => {
    expect(typeof SellSod.created).toBe('function')
  })

  // 评估原始组件选项中的函数的结果
  it('sets the correct default data', () => {
    expect(typeof SellSod.data).toBe('function')
    const defaultData = SellSod.data()
    expect(defaultData.addVisible).toBe(false)
    expect(defaultData.ifhasorga).toBe(false)
  })
})

// 挂载元素并返回已渲染的文本的工具函数
function getRenderedText (Component, propsData) {
  const Constructor = Vue.extend(Component)
  const vm = new Constructor({ propsData: propsData }).$mount()
  return vm.$el.textContent
}

describe('MyComponent', () => {
  it('renders correctly with different props', () => {
    expect(getRenderedText(SellSod, {
      ifchange: true
    })).toBe(true)

    expect(getRenderedText(SellSod, {
      ifchange: false
    })).toBe(false)
  })
})

// 在状态更新后检查生成的 HTML
it('updates the rendered message when vm.message updates', done => {
  const vm = new Vue(SellSod).$mount()
  vm.addVisible = true

  // 在状态改变后和断言 DOM 更新前等待一刻
  Vue.nextTick(() => {
    expect(vm.$el.textContent).toBe(true)
    done()
  })
})
