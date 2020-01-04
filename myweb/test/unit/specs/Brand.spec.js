import Vue from 'vue'
import Brand from '@/components/basic_data/Brand'
describe('Brand', () => {
  // 检查原始组件选项
  it('has a created hook', () => {
    expect(typeof Brand.created).toBe('function')
  })

  // 评估原始组件选项中的函数的结果
  it('sets the correct default data', () => {
    expect(typeof Brand.data).toBe('function')
    const defaultData = Brand.data()
    expect(defaultData.alterVisible).toBe(false)
  })

  // 检查 mount 中的组件实例
  it('correctly sets the message when created', () => {
    const vm = new Vue(Brand).$mount()
    expect(vm.message).toBe('bye!')
  })

  // 创建一个实例并检查渲染输出
  it('renders the correct message', () => {
    const Constructor = Vue.extend(MyComponent)
    const vm = new Constructor().$mount()
    expect(vm.$el.textContent).toBe('bye!')
  })
})
