<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.st_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="转出仓库">
          <el-tag
            :type="'success'"
          >{{formadd.st_from}}
          </el-tag>
        </el-form-item>
        <el-form-item label="转入仓库">
          <el-tag v-if="!ifdirect"
            :type="'success'"
          >{{formadd.st_to}}
          </el-tag>
          <el-select v-model="formadd.st_to"  v-if="ifdirect" placeholder="请选择转入仓库" :disabled="ifhasto">
            <el-option v-for="item in form_td_to" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="出库日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.st_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-button type="primary" class="form-item-save" v-if="ifchange">保 存</el-button>
      </el-form>
    </div>
    <Changedetail :formadd="formadd" :ifdirect="ifdirect" @close="close" :ifchange="ifchange"></Changedetail>
  </div>
</template>

<script>
import Changedetail from './ChangeDetail'
export default {
  props: ['editform', 'ifchange', 'ifdirect'],
  components: {
    Changedetail
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
        st_iden: this.editform.st_iden,
        st_orga: this.editform.st_orga,
        st_to: this.editform.st_to,
        st_from: this.editform.st_from,
        st_req_department: this.editform.st_req_department,
        st_req_date: this.editform.st_req_date
      },
      form_st_orga: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_st_to: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_st_from: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_st_req_department: [
        '普通发票',
        '退换货'
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.st_iden = this.editform.iden
      this.formadd.st_orga = this.editform.st_orga
      this.formadd.st_to = this.editform.st_to
      this.formadd.st_from = this.editform.st_from
      this.formadd.st_req_department = this.editform.st_req_department
      this.formadd.st_req_date = this.editform.st_req_date
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
