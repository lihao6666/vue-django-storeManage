<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.orga_name}}
          </el-tag>
        </el-form-item>
        <el-form-item label="申请部门">
          <el-select v-model="formadd.pr_department" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_pr_department" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="需求类型">
          <el-select v-model="formadd.pr_type" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_pr_type" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="请购日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.pr_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.pr_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                      placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
          </el-form-item>
          <el-tooltip content="保存主明细数据" placement="bottom" effect="light">
            <el-button type="primary" class="form-item-save" v-if="ifchange" @click="saveReqPurAdd">保 存</el-button>
          </el-tooltip>
        </el-row>
      </el-form>
    </div>
    <Reqprd ref="Reqprd" :formadd="formadd" :prds="prds"
            @commit="commit"
            @save="save" @saveall="saveReqPurAdd"
            :orga_name="form_orga_name" :ifchange="ifchange"></Reqprd>
  </div>
</template>

<script>
import Reqprd from './ReqPurPrd'
import {postAPI} from '../../../api/api'
export default {
  name: 'pr_add',
  props: ['editform', 'ifchange'],
  components: {
    Reqprd
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
        pr_iden: this.editform.pr_iden,
        orga_name: this.editform.orga_name,
        pr_department: this.editform.pr_department,
        pr_type: this.editform.pr_type,
        pr_remarks: this.editform.pr_remarks,
        pr_date: this.editform.pr_date
      },
      form_pr_department: [],
      form_orga_name: [],
      form_pr_type: [
        '礼品',
        '教学用品',
        '销售商品',
        '办公用品',
        '市场物资'
      ],
      prds: []
    }
  },
  methods: {
    getList (row = {}) {
      let _this = this
      postAPI('/purchaseRequest/prNew', row).then(function (res) {
        console.log(res.data)
        _this.form_pr_department = []
        for (let i in res.data.dpms) {
          _this.form_pr_department.push(res.data.dpms[i][1])
        }
        _this.form_orga_name = []
        for (let i in res.data.orga_names) {
          _this.form_orga_name.push(res.data.orga_names[i][1])
        }
        if (res.data.prds) {
          _this.prds = res.data.prds
          for (let i in res.data.prds_present_num) {
            _this.prds[i].prd_present_num = res.data.prds_present_num[i].prd_present_num
          }
        }
        _this.$nextTick(() => _this.$refs.Reqprd.getData())
      }).catch(function (err) {
        console.log(err)
      })
    },
    getForm () {
      this.formadd.pr_iden = this.editform.pr_iden
      this.formadd.orga_name = this.editform.orga_name
      this.formadd.pr_department = this.editform.pr_department
      this.formadd.pr_type = this.editform.pr_type
      this.formadd.pr_remarks = this.editform.pr_remarks
      this.formadd.pr_date = this.editform.pr_date
      // this.getData()
    },
    saveReqPurAdd (callback = null) {
      if (this.formadd.pr_department === '' || this.formadd.orga_name === '' ||
        this.formadd.pr_type === '' || this.formadd.pr_date === '') {
        this.$message.error(`请填写完主明细信息`)
        if (typeof (callback) === 'function') {
          let back = false
          callback(back)
        }
        return
      }
      let _this = this
      console.log(_this.formadd)
      if (_this.formadd.pr_iden === '') {
        delete _this.formadd.pr_iden
      }
      postAPI('/purchaseRequest/prUpdate', this.formadd).then(function (res) {
        console.log(res.data)
        if (res.data.signal === 0) {
          _this.$message.success(`保存主明细成功`)
          if (res.data.pr_new_iden) {
            _this.formadd.pr_iden = res.data.pr_new_iden
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
        _this.$refs.Reqprd.addShow()
      })
    },
    commit () {
      this.$emit('commit')
    },
    save () {
      this.$emit('save')
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
</style>
