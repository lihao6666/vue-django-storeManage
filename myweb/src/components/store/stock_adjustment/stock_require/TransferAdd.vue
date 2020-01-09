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
        <el-form-item label="转出仓库">
          <el-tag
            :type="'success'"
          >{{formadd.str_from}}
          </el-tag>
        </el-form-item>
        <el-form-item label="转入仓库">
          <el-select v-model="formadd.str_to" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_str_to" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请部门">
          <el-select v-model="formadd.str_req_department" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_str_department" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.str_req_date"
              align="right"
              type="datetime"
              placeholder="选择日期"
              :disabled="!ifchange"
              :picker-options="pickerOptions">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-button type="primary" class="form-item-save" @click="saveTrdAdd" v-if="ifchange">保 存</el-button>
      </el-form>
    </div>
    <Trdetail :formadd="formadd" @close="close" :ifchange="ifchange" :orga_name="form_orga_name" :trds="trds"
              :str_from="form_str_from" @commit="this.$emit('commit')"
              @save="this.$emit('save')" @saveall="saveReqPurAdd"></Trdetail>
  </div>
</template>

<script>
import Trdetail from './TrDetail'
import {postAPI} from '../../../../api/api'
export default {
  props: ['editform', 'ifchange'],
  components: {
    Trdetail
  },
  data () {
    return {
      pickerOptions: {
        disabledDate (time) {
          return time.getTime() > Date.now()
        },
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
        str_iden: this.editform.str_iden,
        str_orga: this.editform.str_orga,
        str_to: this.editform.str_to,
        str_from: this.editform.str_from,
        str_req_department: this.editform.str_req_department,
        str_req_date: this.editform.str_req_date
      },
      form_orga_name: [],
      form_str_to: [],
      form_str_from: [],
      form_str_department: [],
      trds: []
    }
  },
  methods: {
    getList (row = {}) {
      let _this = this
      postAPI('/purchaseRequest/prNew', row).then(function (res) {
        console.log(res.data)
        _this.form_str_department = []
        for (let i in res.data.dpms) {
          _this.form_str_department.push(res.data.dpms[i][1])
        }
        _this.form_orga_name = []
        for (let i in res.data.orga_names) {
          _this.form_orga_name.push(res.data.orga_names[i][1])
        }
        if (res.data.trds) {
          _this.prds = res.data.trds
          for (let i in res.data.trds_present_num) {
            _this.prds[i].trd_present_num = res.data.trds_present_num[i]
          }
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    getForm () {
      this.formadd.str_iden = this.editform.iden
      this.formadd.str_orga = this.editform.str_orga
      this.formadd.str_to = this.editform.str_to
      this.formadd.str_from = this.editform.str_from
      this.formadd.str_req_department = this.editform.str_req_department
      this.formadd.str_req_date = this.editform.str_req_date
    },
    saveTrdAdd (callback = null) {
      if (this.formadd.str_req_department === '' || this.formadd.orga_name === '' || this.formadd.str_to === '' ||
        this.formadd.str_from === '' || this.formadd.str_req_date === '') {
        this.$message.error(`请填写完主明细信息`)
        if (typeof (callback) === 'function') {
          let back = false
          callback(back)
        }
        return
      }
      let _this = this
      console.log(_this.formadd)
      if (_this.formadd.str_iden === '') {
        delete _this.formadd.str_iden
      }
      postAPI('/purchaseRequest/prUpdate', this.formadd).then(function (res) {
        console.log(res.data)
        if (res.data.signal === 0) {
          _this.$message.success(`保存主明细成功`)
          if (res.data.str_new_iden) {
            _this.formadd.str_iden = res.data.str_new_iden
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
        _this.$refs.Trdetail.addShow()
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
</style>
