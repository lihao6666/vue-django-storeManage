<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.mso_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="出库仓库">
          <el-tag
            :type="'success'"
          >{{formadd.mso_warehouse}}
          </el-tag>
        </el-form-item>
        <el-form-item label="出库类型"  align="left">
          <el-select v-model="formadd.mso_type" placeholder="请选择类型"  class="option" >
            <el-option v-for="item in form_mso_type" v-bind:key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请部门">
          <el-select v-model="formadd.mso_req_department" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_mso_department" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="出库日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.mso_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.mso_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                      placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
          </el-form-item>
          <el-button type="primary" class="form-item-save" v-if="ifchange">保 存</el-button>
        </el-row>
      </el-form>
    </div>
    <MosDetail :formadd="formadd" :ifchange="ifchange" :msods="msods"
               @commit="this.$emit('commit')"
               @save="this.$emit('save')" @saveall="saveMosAdd"
               :orga_name="form_mso_orga" :ware_name="form_mso_warehouse"></MosDetail>
  </div>
</template>

<script>
import MosDetail from './MosDetail'
import {postAPI} from '../../../../api/api'
export default {
  name: 'mso_add',
  props: ['editform', 'ifchange'],
  components: {
    MosDetail
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
        mso_iden: this.editform.mso_iden,
        mso_orga: this.editform.mso_orga,
        mso_type: this.editform.mso_type,
        mso_warehouse: this.editform.mso_warehouse,
        mso_req_department: this.editform.mso_req_department,
        mso_remarks: this.editform.mso_remarks,
        mso_date: this.editform.mso_date
      },
      form_mos_orga: [],
      form_mso_warehouse: [],
      form_mso_department: [],
      form_mso_type: [
        {
          value: 0,
          label: '内部出库',
          type: 'success'
        },
        {
          value: 1,
          label: '外部出库',
          type: ''
        }
      ],
      msods: []
    }
  },
  methods: {
    getList (row = {}) {
      let _this = this
      postAPI('/material_so/mosNew', row).then(function (res) {
        console.log(res.data)
        _this.form_mso_department = []
        for (let i in res.data.dpms) {
          _this.form_mso_department.push(res.data.dpms[i][1])
        }
        _this.form_mos_orga = []
        for (let i in res.data.orga_names) {
          _this.form_mos_orga.push(res.data.orga_names[i][1])
        }
        _this.form_mso_warehouse = []
        for (let i in res.data.mso_warehouse) {
          _this.form_mso_warehouse.push(res.data.mso_warehouse[i][1])
        }
        if (res.data.mosds) {
          _this.mosds = res.data.mosds
          for (let i in res.data.mosds_present_num) {
            _this.mosds[i].mosd_present_num = res.data.mosds_present_num[i]
          }
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    getForm () {
      this.formadd.mso_iden = this.editform.mso_iden
      this.formadd.mso_orga = this.editform.mso_orga
      this.formadd.mso_warehouse = this.editform.mso_warehouse
      this.formadd.mso_req_department = this.editform.mso_req_department
      this.formadd.mso_remarks = this.editform.mso_remarks
      this.formadd.mso_date = this.editform.mso_date
    },
    saveMosAdd (callback = null) {
      if (this.formadd.mso_req_department === '' || this.formadd.mso_orga === '' ||
        this.formadd.mso_warehouse === '' || this.formadd.mso_date === '' || this.formadd.mso_type === '') {
        this.$message.error(`请填写完主明细信息`)
        if (typeof (callback) === 'function') {
          let back = false
          callback(back)
        }
        return
      }
      let _this = this
      console.log(_this.formadd)
      if (_this.formadd.mso_iden === '') {
        delete _this.formadd.mso_iden
      }
      postAPI('/material_so/msoUpdate', this.formadd).then(function (res) {
        console.log(res.data)
        if (res.data.signal === 0) {
          _this.$message.success(`保存主明细成功`)
          if (res.data.mso_new_iden) {
            _this.formadd.mso_iden = res.data.mso_new_iden
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
        _this.$refs.MosDetail.addShow()
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
