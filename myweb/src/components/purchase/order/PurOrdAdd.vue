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
          <el-select v-if="!formadd.po_contractFrom" v-model="formadd.po_supply" placeholder="请选择" :disabled="!ifchange">
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
          >{{formadd.po_contractFrom}}
          </el-tag>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.po_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
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
import Pood from './PurOrdOd'
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
        po_contractFrom: this.editform.po_contractFrom,
        po_supply: this.editform.po_supply,
        po_remarks: this.editform.po_remarks,
        po_date: this.editform.po_date,
        po_sum: this.editform.po_sum
      },
      form_po_orga: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_po_supply: [
        '礼品',
        '教学用品',
        '销售商品'
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.po_iden = this.editform.po_iden
      this.formadd.po_orga = this.editform.po_orga
      this.formadd.po_contractFrom = this.editform.po_contractFrom
      this.formadd.po_supply = this.editform.po_supply
      this.formadd.po_remarks = this.editform.po_remarks
      this.formadd.po_date = this.editform.po_date
      this.formadd.po_sum = this.editform.po_sum
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
