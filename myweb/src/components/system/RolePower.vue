<template>
  <div class="container">
    <el-tabs :value="data[0].label">
      <el-tab-pane v-for="item in data" v-bind:key="item.key" :label="item.label" :name="item.label">
        <div v-if="item.child" class="checkbox-group-ch">
          <div v-for="child in item.child" v-bind:key="child.key">
            <el-checkbox :indeterminate="child.isIndeterminate" v-model="child.checkAll"
                         @change="handleCheckAllChangeData(child,child.checkAll)">{{child.label}}</el-checkbox>
            <el-checkbox-group v-if="child.options" v-model="child.checked" @change="handlecheckedOptionsChangeData(child,child.checked)" class="checkbox-group-ch">
              <el-checkbox v-for="option in child.options" v-bind:key="option.value" :label="option.value" :value="option.value">{{option.label}}</el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="库存管理" name="库存管理">
        <el-tabs :tab-position="'left'" :value="store[0].label">
          <el-tab-pane v-for="item in store" v-bind:key="item.key" :label="item.label" :name="item.label">
            <div v-if="item.child" class="checkbox-group-ch">
              <div v-for="child in item.child" v-bind:key="child.key">
                <el-checkbox :indeterminate="child.isIndeterminate" v-model="child.checkAll"
                             @change="handleCheckAllChangeStore(child,child.checkAll)">{{child.label}}</el-checkbox>
                <el-checkbox-group v-if="child.options" v-model="child.checked" @change="handlecheckedOptionsChangeStore(child,child.checked)" class="checkbox-group-ch">
                  <el-checkbox v-for="option in child.options" v-bind:key="option.value" :label="option.value" :value="option.value">{{option.label}}</el-checkbox>
                </el-checkbox-group>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-tab-pane>
      <el-tab-pane v-for="item in system" v-bind:key="item.key" :label="item.label" :name="item.label">
        <div v-if="item.child" class="checkbox-group-ch">
          <div v-for="child in item.child" v-bind:key="child.key">
            <el-checkbox :indeterminate="child.isIndeterminate" v-model="child.checkAll"
                         @change="handleCheckAllChangeSystem(child,child.checkAll)">{{child.label}}</el-checkbox>
            <el-checkbox-group v-if="child.options" v-model="child.checked" @change="handlecheckedOptionsChangeSystem(child,child.checked)" class="checkbox-group-ch">
              <el-checkbox class="el-checkbox-ch" v-for="option in child.options" v-bind:key="option.value" :label="option.value" :value="option.value">{{option.label}}</el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>
import {postAPI} from '../../api/api'

export default {
  data () {
    return {
      data: [
        {
          label: '销售业务',
          key: 0,
          value: '0',
          child: [
            {
              label: '销售订单',
              key: 0,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            }
          ]
        },
        {
          label: '采购管理',
          key: 1,
          value: '0',
          child: [
            {
              label: '请购单',
              key: 1,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            },
            {
              label: '采购合同',
              key: 2,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            },
            {
              label: '采购订单',
              key: 3,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            }
          ]
        }
      ],
      store: [
        {
          label: '入库管理',
          key: 4,
          value: '0',
          child: [
            {
              label: '采购入库',
              key: 4,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            },
            {
              label: '其他入库',
              key: 5,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            }
          ]
        },
        {
          label: '出库管理',
          key: 6,
          value: '0',
          child: [
            {
              label: '材料出库',
              key: 6,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            },
            {
              label: '销售出库',
              key: 7,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            },
            {
              label: '其他出库',
              key: 8,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            }
          ]
        },
        {
          label: '库存调整',
          key: 9,
          value: '0',
          child: [
            {
              label: '转库申请',
              key: 9,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            },
            {
              label: '转库单',
              key: 10,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            },
            {
              label: '库存盘点',
              key: 11,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            },
            {
              label: '期初库存',
              key: 12,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            }
          ]
        },
        {
          label: '库存查询',
          key: 13,
          value: '0',
          child: [
            {
              label: '现存量查询',
              key: 13,
              value: '0',
              checkAll: false,
              options: [
                {
                  value: 1,
                  label: '查看数据'
                },
                {
                  value: 2,
                  label: '新增编辑'
                }
              ],
              checked: [],
              isIndeterminate: false
            }
          ]
        }
      ],
      system: [
        {
          label: '系统管理',
          key: 14,
          value: '0',
          child: [
            {
              label: '系统管理',
              key: 14,
              value: '0',
              checkAll: false,
              options: [
                {
                  key: 14,
                  value: 1,
                  label: '组织架构管理'
                },
                {
                  key: 15,
                  value: 2,
                  label: '角色管理'
                },
                {
                  key: 16,
                  value: 3,
                  label: '用户管理'
                }
              ],
              checked: [],
              isIndeterminate: false
            }
          ]
        },
        {
          label: '基础数据管理',
          key: 17,
          value: '0',
          child: [
            {
              label: '基础数据管理',
              key: 17,
              value: '0',
              checkAll: false,
              options: [
                {
                  key: 17,
                  value: 1,
                  label: '库存组织管理'
                },
                {
                  key: 18,
                  value: 2,
                  label: '中心管理'
                },
                {
                  key: 19,
                  value: 3,
                  label: '品牌管理'
                },
                {
                  key: 20,
                  value: 4,
                  label: '仓库维护'
                },
                {
                  key: 21,
                  value: 5,
                  label: '供应商维护'
                },
                {
                  key: 22,
                  value: 6,
                  label: '客户维护'
                },
                {
                  key: 23,
                  value: 7,
                  label: '计量单位维护'
                },
                {
                  key: 24,
                  value: 8,
                  label: '物料类别维护'
                },
                {
                  key: 25,
                  value: 9,
                  label: '物料维护'
                }
              ],
              checked: [],
              isIndeterminate: false
            }
          ]
        }
      ],
      form: {}
    }
  },
  props: ['powerform'],
  methods: {
    getForm () {
      this.form.role_power = this.powerform.role_power
      for (let i in this.data) {
        for (let j in this.data[i].child) {
          let x = this.data[i].child[j].key
          let ch = parseInt(this.form.role_power.charAt(x))
          if (ch === 0) {
            this.data[i].child[j].checked = []
            this.data[i].child[j].isIndeterminate = false
            this.data[i].child[j].checkAll = false
          } else if (ch === 1) {
            this.data[i].child[j].checked = [1]
            this.data[i].child[j].isIndeterminate = true
            this.data[i].child[j].checkAll = false
          } else if (ch === 2) {
            this.data[i].child[j].checked = [2]
            this.data[i].child[j].isIndeterminate = true
            this.data[i].child[j].checkAll = false
          } else if (ch === 3) {
            this.data[i].child[j].checked = [1, 2]
            this.data[i].child[j].isIndeterminate = false
            this.data[i].child[j].checkAll = true
          }
        }
      }
      for (let i in this.store) {
        for (let j in this.store[i].child) {
          let x = this.store[i].child[j].key
          let ch = parseInt(this.form.role_power.charAt(x))
          if (ch === 0) {
            this.store[i].child[j].checked = []
            this.store[i].child[j].isIndeterminate = false
            this.store[i].child[j].checkAll = false
          } else if (ch === 1) {
            this.store[i].child[j].checked = [1]
            this.store[i].child[j].isIndeterminate = true
            this.store[i].child[j].checkAll = false
          } else if (ch === 2) {
            this.store[i].child[j].checked = [2]
            this.store[i].child[j].isIndeterminate = true
            this.store[i].child[j].checkAll = false
          } else if (ch === 3) {
            this.store[i].child[j].checked = [1, 2]
            this.store[i].child[j].isIndeterminate = false
            this.store[i].child[j].checkAll = true
          }
        }
      }
      for (let i in this.system) {
        for (let j in this.system[i].child) {
          for (let k in this.system[i].child[j].options) {
            let x = this.system[i].child[j].options[k].key
            let ch = parseInt(this.form.role_power.charAt(x))
            if (ch === 1) {
              this.system[i].child[j].checked.push(parseInt(k) + 1)
            }
          }
          if (this.system[i].child[j].checked.length > 0 && this.system[i].child[j].checked.length < this.system[i].child[j].options.length) {
            this.system[i].child[j].isIndeterminate = true
            this.system[i].child[j].checkAll = false
          } else if (this.system[i].child[j].checked.length === this.system[i].child[j].options.length) {
            this.system[i].child[j].isIndeterminate = false
            this.system[i].child[j].checkAll = true
          } else {
            this.system[i].child[j].isIndeterminate = false
            this.system[i].child[j].checkAll = false
          }
        }
      }
      this.form.role = this.powerform.role
      this.form.id = this.powerform.id
    },
    handleCheckAllChangeData (item, value) {
      if (value) {
        let arr = []
        for (let j in item.options) {
          arr.push(parseInt(j) + 1)
        }
        item.checked = arr
        item.isIndeterminate = false
        item.checkAll = true
      } else {
        item.checked = []
        item.isIndeterminate = false
        item.checkAll = false
      }
    },
    handlecheckedOptionsChangeData (item, value) {
      console.log(item.checked)
      item.checkAll = value.length === item.options.length
      item.isIndeterminate = value.length > 0 && value.length < item.options.length
    },
    handleCheckAllChangeStore (item, value) {
      if (value) {
        let arr = []
        for (let j in item.options) {
          arr.push(parseInt(j) + 1)
        }
        item.checked = arr
        item.isIndeterminate = false
        item.checkAll = true
      } else {
        item.checked = []
        item.isIndeterminate = false
        item.checkAll = false
      }
    },
    handlecheckedOptionsChangeStore (item, value) {
      console.log(item.checked)
      item.checkAll = value.length === item.options.length
      item.isIndeterminate = value.length > 0 && value.length < item.options.length
    },
    handleCheckAllChangeSystem (item, value) {
      if (value) {
        let arr = []
        for (let j in item.options) {
          arr.push(parseInt(j) + 1)
        }
        item.checked = arr
        item.isIndeterminate = false
        item.checkAll = true
      } else {
        item.checked = []
        item.isIndeterminate = false
        item.checkAll = false
      }
    },
    handlecheckedOptionsChangeSystem (item, value) {
      console.log(item.checked)
      item.checkAll = value.length === item.options.length
      item.isIndeterminate = value.length > 0 && value.length < item.options.length
    },
    save () {
      let str = ''
      for (let i in this.data) {
        for (let j in this.data[i].child) {
          let x = 0
          for (let k in this.data[i].child[j].checked) {
            x += this.data[i].child[j].checked[k]
          }
          str += x
        }
      }
      for (let i in this.store) {
        for (let j in this.store[i].child) {
          let x = 0
          for (let k in this.store[i].child[j].checked) {
            x += this.store[i].child[j].checked[k]
          }
          str += x
        }
      }
      for (let i in this.system) {
        for (let j in this.system[i].child) {
          let s = ''
          while (s.length < this.system[i].child[j].options.length) {
            s += '0'
          }
          for (let k in this.system[i].child[j].checked) {
            let x = this.system[i].child[j].checked[k] - 1
            if (x === s.length - 1) {
              s = s.substring(0, x) + '1'
            } else {
              s = s.substring(0, x) + '1' + s.substring(x + 1)
            }
          }
          str += s
        }
      }
      console.log(str)
      this.form.role_power = str
      let _this = this
      postAPI('/base/roleUpdate', this.form).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`授权成功`)
          return true
        } else {
          _this.$message.error(res.data.message)
          return false
        }
      }).catch(function (err) {
        console.log(err)
        _this.$message.error(`授权失败`)
        return false
      })
    }
  }
}
</script>

<style scoped>
  .checkbox-group-ch {
    margin: 20px 0 20px 50px;
  }
  .el-checkbox-ch {
    margin-bottom: 20px;
  }
</style>
