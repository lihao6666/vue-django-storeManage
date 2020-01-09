<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.pc_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="合同名称">
          <el-input type="textarea" v-model="formadd.pc_name" rows="1" :disabled="!ifchange"
                    placeholder="请输入合同名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-model="formadd.pc_supply" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_pc_supply" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="签订日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.pc_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="合同总额">
          <el-tag
            :type="'success'"
          >{{formadd.pc_sum}}
          </el-tag>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.pc_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                      placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
          </el-form-item>
        <el-button type="primary" class="form-item-save" v-if="ifchange" @click="saveReqPurAdd">保 存</el-button>
        </el-row>
      </el-form>
    </div>
    <Pccd ref="Pccd" :cds="cds" :orga_name="form_orga_name" :formadd="formadd" :ifchange="ifchange"></Pccd>
    <Pcpay ref="Pcpay" :pays="pays" :formadd="formadd" :ifchange="ifchange"></Pcpay>
    <el-row :gutter="20" v-if="ifchange" class="el-row-button">
      <el-col :span="1" :offset="18">
        <el-button @click="this.$emit('commit')">取 消</el-button>
      </el-col>
      <el-col :span="1" :offset="1">
        <el-button type="primary">提 交</el-button>
      </el-col>
      <el-col :span="1" :offset="1">
        <el-button type="primary">保 存</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Pccd from './PurConCd'
import Pcpay from './PurConPay'
import {postAPI} from '../../../api/api'
export default {
  name: 'pc_add',
  props: ['editform', 'ifchange'],
  components: {
    Pccd,
    Pcpay
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
        pc_iden: this.editform.pc_iden,
        pc_orga: this.editform.pc_orga,
        pc_name: this.editform.pc_name,
        pc_supply: this.editform.pc_supply,
        pc_remarks: this.editform.pc_remarks,
        pc_date: this.editform.pc_date,
        pc_sum: this.editform.pc_sum
      },
      form_orga_name: [],
      form_pc_supply: [],
      cds: [],
      pays: []
    }
  },
  methods: {
    getList (row = {}) {
      let _this = this

      postAPI('/purchase/pcNew', row).then(function (res) {
        console.log(res.data)
        _this.form_pc_supply = []
        for (let i in res.data.supply_names) {
          _this.form_pc_supply.push(res.data.supply_names[i][1])
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
      }).catch(function (err) {
        console.log(err)
      })
    },
    getForm () {
      this.formadd.pc_iden = this.editform.pc_iden
      this.formadd.pc_orga = this.editform.pc_orga
      this.formadd.pc_name = this.editform.pc_name
      this.formadd.pc_supply = this.editform.pc_supply
      this.formadd.pc_remarks = this.editform.pc_remarks
      this.formadd.pc_date = this.editform.pc_date
      this.formadd.pc_sum = this.editform.pc_sum
    },
    saveReqPurAdd (callback = null) {

      if (this.formadd.pc_department === '' || this.formadd.orga_name === '' ||
        this.formadd.pc_type === '' || this.formadd.pc_date === '') {
        this.$message.error(`请填写完主明细信息`)
        if (typeof (callback) === 'function') {
          let back = false
          callback(back)
        }
        return
      }
      let _this = this
      console.log(_this.formadd)
      if (_this.formadd.pc_iden === '') {
        delete _this.formadd.pc_iden
      }
      postAPI('/purchase/pcUpdate', this.formadd).then(function (res) {
        console.log(res.data)
        if (res.data.signal === 0) {
          _this.$message.success(`保存主明细成功`)
          if (res.data.pc_new_iden) {
            _this.formadd.pc_iden = res.data.pc_new_iden
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
        _this.$refs.Pccd.addShow()
      })
    }
  }
}
</script>

<style scoped>
  .form-item-from {
    width: 200%;
  }
  .form-item-save {
    float: right;
    margin-top: 20px;
  }
  .el-row-button {
    top: 15px;
  }
</style>
