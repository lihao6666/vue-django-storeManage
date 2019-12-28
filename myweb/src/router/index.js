import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/requisition'
    },
    {
      path: '/',
      component: () => import(/* webpackChunkName: "home" */ '../components/Home.vue'),
      meta: {title: 'home'},
      children: [
        {
          path: '/requisition',
          component: () => import(/* webpackChunkName: "请购" */ '../components/req_pur/req_pur_check.vue'),
          meta: {title: '请购'}
        },
        {
          path: '/sell',
          component: () => import(/* webpackChunkName: "销售订单" */ '../components/sell/sell_check.vue'),
          meta: {title: '销售订单'}
        },
        {
          path: '/organizationmanage',
          component: () => import(/* webpackChunkName: "donate" */ '../components/System/OrganizationManage.vue'),
          meta: {title: '库存组织管理'}
        },
        {
          path: '/rolemanage',
          component: () => import(/* webpackChunkName: "donate" */ '../components/System/RoleManage.vue'),
          meta: {title: '角色管理'}
        },
        {
          path: '/usermanage',
          component: () => import(/* webpackChunkName: "donate" */ '../components/System/UserManage.vue'),
          meta: {title: '用户管理'}
        }
      ]
    },
    {
      path: '/login',
      component: () => import(/* webpackChunkName: "login" */ '../components/Login.vue'),
      meta: {title: '登录'}
    },
    {
      path: '*',
      component: () => import(/* webpackChunkName: "404" */ '../components/404.vue'),
      meta: {title: '404'}
    }
  ]
})
