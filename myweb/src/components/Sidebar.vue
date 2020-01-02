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
      <template v-for="item in items">
        <template v-if="item.subs">
          <el-submenu :index="item.index" :key="item.index">
            <template slot="title">
              <i :class="item.icon"></i>
              <span slot="title">{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs">
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
      items: [
        {
          icon: 'el-icon-s-home',
          index: 'requisition',
          title: '请购'
        },
        {
          icon: 'el-icon-shopping-bag-1',
          index: '1',
          title: '销售业务',
          subs: [
            {
              index: 'sell',
              title: '销售订单'
            }
          ]
        },
        {
          icon: 'el-icon-shopping-cart-full',
          index: '2',
          title: '采购管理',
          subs: [
            {
              index: 'constract',
              title: '采购合同'
            },
            {
              index: 'purchase',
              title: '采购订单'
            }
          ]
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
                  title: '采购入库'
                },
                {
                  index: 'otherinstore',
                  title: '其他入库'
                }
              ]
            },
            {
              index: '4-3',
              title: '出库管理',
              subs: [
                {
                  index: 'materialsoutstore',
                  title: '材料出库'
                },
                {
                  index: 'selloutstore',
                  title: '销售出库'
                },
                {
                  index: 'otheroutstore',
                  title: '其他出库'
                }
              ]
            },
            {
              index: '4-4',
              title: '库存调整',
              subs: [
                {
                  index: 'storerequisition',
                  title: '转库申请'
                },
                {
                  index: 'storechange',
                  title: '转库单'
                },
                {
                  index: 'storeconfirm',
                  title: '库存盘点'
                },
                {
                  index: 'storebegin',
                  title: '期初库存'
                }
              ]
            },
            {
              index: '4-1',
              title: '库存查询',
              subs: [
                {
                  index: 'stockcheck',
                  title: '现存量查询'
                }
              ]
            }
          ]
        },
        {
          icon: 'el-icon-data-line',
          index: '3',
          title: '系统管理',
          subs: [
            {
              index: 'organizationmanage',
              title: '组织架构管理'
            },
            {
              index: 'rolemanage',
              title: '角色管理'
            },
            {
              index: 'usermanage',
              title: '用户管理'
            }
          ]
        },
        {
          icon: 'el-icon-document',
          index: '9',
          title: '基础数据管理',
          subs: [
            {
              index: 'organization',
              title: '库存组织管理'
            },
            {
              index: 'center',
              title: '中心管理'
            },
            {
              index: 'brand',
              title: '品牌管理'
            },
            {
              index: 'warehouse',
              title: '总仓维护'
            },
            {
              index: 'store',
              title: '仓库维护'
            },
            {
              index: 'supplier',
              title: '供应商维护'
            },
            {
              index: 'customer',
              title: '客户维护'
            },
            {
              index: 'meterage',
              title: '计量单位维护'
            },
            {
              index: 'materialtype',
              title: '物料类别维护'
            },
            {
              index: 'material',
              title: '物料维护'
            }
          ]
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
