<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.str_orga}}
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
            <el-option v-for="item in form_str_req_department" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.str_req_date"
              align="right"
              type="date"
              placeholder="选择日期"
              format="yyyy 年 MM 月 dd 日"
              :disabled="!ifchange"
              :picker-options="pickerOptions">
            </el-date-picker>
          </el-col>
        </el-form-item>
      </el-form>
    </div>
    <Trdetail :formadd="formadd" @close="close" :ifchange="ifchange"></Trdetail>
  </div>
</template>

<script>
import Trdetail from './TrDetail'
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
      form_str_orga: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_str_to: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_str_from: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_str_req_department: [
        '普通发票',
        '退换货'
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.str_iden = this.editform.iden
      this.formadd.str_orga = this.editform.str_orga
      this.formadd.str_to = this.editform.str_to
      this.formadd.str_from = this.editform.str_from
      this.formadd.str_req_department = this.editform.str_req_department
      this.formadd.str_req_date = this.editform.str_req_date
    },
    // 关闭新增弹窗
    close () {
      this.$emit('close')
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
