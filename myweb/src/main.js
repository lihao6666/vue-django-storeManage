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
  const role = localStorage.getItem('ms_username')
  if (!role && to.path !== '/login') {
    next('/login')
  } else {
    next()
  }
})

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
