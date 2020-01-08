<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.ois_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="入库仓库">
          <el-tag
            :type="'success'"
          >{{formadd.ois_warehouse}}
          </el-tag>
        </el-form-item>
        <el-form-item label="入库日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.ois_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.ois_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                      placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
          </el-form-item>
          <el-button type="primary" class="form-item-save" v-if="ifchange">保 存</el-button>
        </el-row>
      </el-form>
    </div>
    <Pood :formadd="formadd" :ifchange="ifchange"></Pood>
  </div>
</template>

<script>
import Pood from './OisBd'
export default {
  name: 'ois_add',
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
        ois_iden: this.editform.ois_iden,
        ois_orga: this.editform.ois_orga,
        ois_warehouse: this.editform.ois_warehouse,
        ois_remarks: this.editform.ois_remarks,
        ois_date: this.editform.ois_date
      },
      form_ois_transfer: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_ois_warehouse: [
        'a',
        'b',
        'c'
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.ois_iden = this.editform.ois_iden
      this.formadd.ois_orga = this.editform.ois_orga
      this.formadd.ois_warehouse = this.editform.ois_warehouse
      this.formadd.ois_remarks = this.editform.ois_remarks
      this.formadd.ois_date = this.editform.ois_date
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
