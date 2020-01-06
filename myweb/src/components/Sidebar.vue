<template>
  <div class="sidebar">
    <el-menu
      class="sidebar-el-menu"
      :default-active="onRoutes"
      :collapse="collapse"
      background-color="#324157"
      text-color="#bfcbd9"
      active-text-color="#20a0ff"
      unique-opened
      router
    >
      <template v-for="item in items" v-if="item.ifshow">
        <template v-if="item.subs">
          <el-submenu :index="item.index" :key="item.index">
            <template slot="title">
              <i :class="item.icon"></i>
              <span slot="title">{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs" v-if="subItem.ifshow">
              <el-submenu
                v-if="subItem.subs"
                :index="subItem.index"
                :key="subItem.index"
              >
                <template slot="title">{{ subItem.title }}</template>
                <el-menu-item
                  v-for="(threeItem,i) in subItem.subs"
                  :key="i"
                  :index="threeItem.index"
                  v-if="threeItem.ifshow"
                >{{ threeItem.title }}
                </el-menu-item>
              </el-submenu>
              <el-menu-item
                v-else
                :index="subItem.index"
                :key="subItem.index"
              >{{ subItem.title }}
              </el-menu-item>
            </template>
          </el-submenu>
        </template>
        <template v-else>
          <el-menu-item :index="item.index" :key="item.index">
            <i :class="item.icon"></i>
            <span slot="title">{{ item.title }}</span>
          </el-menu-item>
        </template>
      </template>
    </el-menu>
  </div>
</template>

<script>
import bus from './bus'

export default {
  data () {
    return {
      collapse: false,
      power: '',
      items: [
        {
          icon: 'el-icon-s-home',
          index: 'home',
          title: '首页',
          ifshow: true
        },
        {
          icon: 'el-icon-shopping-bag-1',
          index: '1',
          title: '销售业务',
          subs: [
            {
              index: 'sell',
              title: '销售订单',
              ifshow: true,
              key: 0
            }
          ],
          ifshow: true
        },
        {
          icon: 'el-icon-shopping-cart-full',
          index: '2',
          title: '采购管理',
          subs: [
            {
              index: 'requisition',
              title: '请购单',
              ifshow: true,
              key: 1
            },
            {
              index: 'constract',
              title: '采购合同',
              ifshow: true,
              key: 2
            },
            {
              index: 'purchase',
              title: '采购订单',
              ifshow: true,
              key: 3
            }
          ],
          ifshow: true
        },
        {
          icon: 'el-icon-box',
          index: '4',
          title: '库存管理',
          subs: [
            {
              index: '4-2',
              title: '入库管理',
              subs: [
                {
                  index: 'buyinstore',
                  title: '采购入库',
                  ifshow: true,
                  key: 4
                },
                {
                  index: 'otherinstore',
                  title: '其他入库',
                  ifshow: true,
                  key: 5
                }
              ],
              ifshow: true
            },
            {
              index: '4-3',
              title: '出库管理',
              subs: [
                {
                  index: 'materialsoutstore',
                  title: '材料出库',
                  ifshow: true,
                  key: 6
                },
                {
                  index: 'selloutstore',
                  title: '销售出库',
                  ifshow: true,
                  key: 7
                },
                {
                  index: 'otheroutstore',
                  title: '其他出库',
                  ifshow: true,
                  key: 8
                }
              ],
              ifshow: true
            },
            {
              index: '4-4',
              title: '库存调整',
              subs: [
                {
                  index: 'stockrequisition',
                  title: '转库申请',
                  ifshow: true,
                  key: 9
                },
                {
                  index: 'stockchange',
                  title: '转库单',
                  ifshow: true,
                  key: 10
                },
                {
                  index: 'stockconfirm',
                  title: '库存盘点',
                  ifshow: true,
                  key: 11
                },
                {
                  index: 'stockbegin',
                  title: '期初库存',
                  ifshow: true,
                  key: 12
                }
              ],
              ifshow: true
            },
            {
              index: '4-1',
              title: '库存查询',
              subs: [
                {
                  index: 'stockcheck',
                  title: '现存量查询',
                  ifshow: true,
                  key: 13
                }
              ],
              ifshow: true
            }
          ],
          ifshow: true
        },
        {
          icon: 'el-icon-data-line',
          index: '3',
          title: '系统管理',
          subs: [
            {
              index: 'organizationmanage',
              title: '组织架构管理',
              ifshow: true,
              key: 14
            },
            {
              index: 'rolemanage',
              title: '角色管理',
              ifshow: true,
              key: 15
            },
            {
              index: 'usermanage',
              title: '用户管理',
              ifshow: true,
              key: 16
            }
          ],
          ifshow: true
        },
        {
          icon: 'el-icon-document',
          index: '9',
          title: '基础数据管理',
          subs: [
            {
              index: 'organization',
              title: '库存组织管理',
              ifshow: true,
              key: 17
            },
            {
              index: 'center',
              title: '中心管理',
              ifshow: true,
              key: 18
            },
            {
              index: 'brand',
              title: '品牌管理',
              ifshow: true,
              key: 19
            },
            {
              index: 'warehouse',
              title: '仓库维护',
              ifshow: true,
              key: 20
            },
            {
              index: 'supplier',
              title: '供应商维护',
              ifshow: true,
              key: 21
            },
            {
              index: 'customer',
              title: '客户维护',
              ifshow: true,
              key: 22
            },
            {
              index: 'meterage',
              title: '计量单位维护',
              ifshow: true,
              key: 23
            },
            {
              index: 'materialtype',
              title: '物料类别维护',
              ifshow: true,
              key: 24
            },
            {
              index: 'material',
              title: '物料维护',
              ifshow: true,
              key: 25
            }
          ],
          ifshow: true
        }
      ]
    }
  },
  computed: {
    onRoutes () {
      return this.$route.path.replace('/', '')
    }
  },
  created () {
    // 通过 Event Bus 进行组件间通信，来折叠侧边栏
    bus.$on('collapse', msg => {
      this.collapse = msg
      bus.$emit('collapse-content', msg)
    })
    this.power = String(localStorage.getItem('user_power'))
    for (let i = 1; i < this.items.length; i++) {
      this.ifShow(this.items[i])
    }
  },
  methods: {
    ifShow (item) {
      let ifshow = false
      let ifhas = false
      for (let i in item.subs) {
        ifhas = true
        if (this.ifShow(item.subs[i])) {
          ifshow = true
        }
      }
      if (ifhas) {
        item.ifshow = ifshow
        return ifshow
      }
      if (this.power.charAt(item.key) !== '0') {
        item.ifshow = true
        return true
      } else {
        item.ifshow = false
        return false
      }
    }
  }
}
</script>

<style scoped>
  .sidebar {
    display: block;
    position: absolute;
    left: 0;
    top: 70px;
    bottom: 0;
    overflow-y: scroll;
  }

  .sidebar::-webkit-scrollbar {
    width: 0;
  }

  .sidebar-el-menu:not(.el-menu--collapse) {
    width: 250px;
  }

  .sidebar > ul {
    height: 100%;
  }
</style>
