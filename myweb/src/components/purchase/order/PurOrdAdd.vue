<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.po_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-if="!formadd.pc_iden" v-model="formadd.po_supply" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_po_supply" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
          <el-tag v-else :type="'success'">{{formadd.po_supply}}</el-tag>
        </el-form-item>
        <el-form-item label="订单日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.po_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="价税合计">
          <el-tag
            :type="'success'"
          >{{formadd.po_sum}}
          </el-tag>
        </el-form-item>
        <el-form-item label="来源合同">
          <el-tag
            :type="'success'"
          >{{formadd.pc_iden}}
          </el-tag>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.po_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                      placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
          </el-form-item>
          <el-tooltip content="保存主明细数据" placement="bottom" effect="light">
            <el-button type="primary" class="form-item-save" v-if="ifchange" @click="saveReqPurAdd">保 存</el-button>
          </el-tooltip>
        </el-row>
      </el-form>
    </div>
    <Pood ref="Pood" :formadd="formadd" :ods="ods" :orga_name="form_orga_name" :ifchange="ifchange"></Pood>
  </div>
</template>

<script>
import Pood from './PurOrdOd'
import {postAPI} from '../../../api/api'
export default {
  name: 'po_add',
  props: ['editform', 'ifchange'],
  components: {
    Pood
  },
  data () {
    return {
      pickerOptions: {
        shortcuts: [{
          text: '今天',
          onClick (picker) {
            picker.$emit('pick', new Date())
          }
        }, {
          text: '昨天',
          onClick (picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', date)
          }
        }, {
          text: '一周前',
          onClick (picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', date)
          }
        }]
      },
      formadd: {
        po_iden: this.editform.po_iden,
        po_orga: this.editform.po_orga,
        pc_iden: this.editform.pc_iden,
        po_supply: this.editform.po_supply,
        po_remarks: this.editform.po_remarks,
        po_date: this.editform.po_date,
        po_sum: this.editform.po_sum
      },
      form_orga_name: [],
      form_po_supply: [],
      ods: []
    }
  },
  methods: {
    getList (row = {}) {
      let _this = this

      postAPI('/purchase/pONewByPr', row).then(function (res) {
        console.log(res.data)
        _this.form_po_supply = []
        for (let i in res.data.supply_names) {
          _this.form_po_supply.push(res.data.supply_names[i][1])
        }
        _this.form_orga_name = []
        for (let i in res.data.orga_names) {
          _this.form_orga_name.push(res.data.orga_names[i][1])
        }
        if (res.data.cds) {
          _this.cds = res.data.cds
        }
        if (res.data.pays) {
          _this.pays = res.data.pays
        }
        _this.$nextTick(() => _this.$refs.Pood.getData())
      }).catch(function (err) {
        console.log(err)
      })
    },
    getForm () {
      this.formadd.po_iden = this.editform.po_iden
      this.formadd.po_orga = this.editform.po_orga
      this.formadd.pc_iden = this.editform.pc_iden
      this.formadd.po_supply = this.editform.po_supply
      this.formadd.po_remarks = this.editform.po_remarks
      this.formadd.po_date = this.editform.po_date
      this.formadd.po_sum = this.editform.po_sum
    },
    saveReqPurAdd (callback = null) {
      if (this.formadd.po_department === '' || this.formadd.orga_name === '' ||
        this.formadd.po_type === '' || this.formadd.po_date === '') {
        this.$message.error(`请填写完主明细信息`)
        if (typeof (callback) === 'function') {
          let back = false
          callback(back)
        }
        return
      }
      let _this = this
      console.log(_this.formadd)
      if (_this.formadd.po_iden === '') {
        delete _this.formadd.po_iden
      }
      postAPI('/purchase/poUpdate', this.formadd).then(function (res) {
        console.log(res.data)
        if (res.data.signal === 0) {
          _this.$message.success(`保存主明细成功`)
          if (res.data.po_new_iden) {
            _this.formadd.po_iden = res.data.po_new_iden
          }
          _this.$emit('save')
          if (typeof (callback) === 'function') {
            let back = true
            callback(back)
          }
        } else {
          _this.$message.error('保存主明细失败')
          if (typeof (callback) === 'function') {
            let back = false
            callback(back)
          }
        }
      }).catch(function (err) {
        _this.$message.error('保存主明细失败')
        console.log(err)
        if (typeof (callback) === 'function') {
          let back = false
          callback(back)
        }
      })
    },
    // 新增窗口弹出
    addShow () {
      let _this = this
      this.$nextTick(function () {
        _this.$refs.Pood.addShow()
      })
    }
  }
}
</script>

<style scoped>
  .form-item-save {
    float: right;
    margin-top: 20px;
  }
  .form-item-from {
    width: 200%;
  }
</style>
