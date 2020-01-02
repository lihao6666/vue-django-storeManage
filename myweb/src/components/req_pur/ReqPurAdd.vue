<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.req_pur_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="申请部门">
          <el-select v-model="formadd.req_pur_from" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_req_pur_from" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="需求类型">
          <el-select v-model="formadd.req_pur_type" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_req_pur_type" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="请购日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.req_pur_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.req_pur_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                      placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
          </el-form-item>
          <el-button type="primary" class="form-item-save" v-if="ifchange">保 存</el-button>
        </el-row>
      </el-form>
    </div>
    <Reqprd :formadd="formadd" :ifchange="ifchange"></Reqprd>
  </div>
</template>

<script>
import Reqprd from './ReqPurPrd'
export default {
  name: 'req_pur_add',
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
        req_pur_iden: this.editform.req_pur_iden,
        req_pur_orga: this.editform.req_pur_orga,
        req_pur_from: this.editform.req_pur_from,
        req_pur_type: this.editform.req_pur_type,
        req_pur_remarks: this.editform.req_pur_remarks,
        req_pur_date: this.editform.req_pur_date
      },
      form_req_pur_from: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_req_pur_type: [
        '礼品',
        '教学用品',
        '销售商品'
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.req_pur_iden = this.editform.req_pur_iden
      this.formadd.req_pur_orga = this.editform.req_pur_orga
      this.formadd.req_pur_from = this.editform.req_pur_from
      this.formadd.req_pur_type = this.editform.req_pur_type
      this.formadd.req_pur_remarks = this.editform.req_pur_remarks
      this.formadd.req_pur_date = this.editform.req_pur_date
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
