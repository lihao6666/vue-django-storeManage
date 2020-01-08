// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

// require('./mock/mock')

Vue.config.productionTip = false
Vue.use(ElementUI)

/* eslint-disable no-new */
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} | 仓储管理系统`
  const username = localStorage.getItem('user_now_iden')
  const power = localStorage.getItem('user_power')
  if (!username && to.path !== '/login') {
    next('/login')
  } else if (to.path === '/login' || to.path === '/404') {
    next()
  } else if (username && power) {
    if (!to.meta.key) {
      next()
    } else if (power.charAt(to.meta.key) === '0') {
      next('/404')
    } else {
      next()
    }
  } else {
    next('/login')
  }
  // const role = localStorage.getItem('user_now_iden')
  // if (!role && to.path !== '/login') {
  //   next('/login')
  // } else {
  //   next()
  // }
})

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
