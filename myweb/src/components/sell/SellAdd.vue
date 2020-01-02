<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.so_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="发货仓库">
          <el-tag
            :type="'success'"
          >{{formadd.so_warehouse}}
          </el-tag>
        </el-form-item>
        <el-form-item label="订单类型">
          <el-select v-model="formadd.so_type" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_so_type" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="客户">
          <el-select v-model="formadd.so_custom" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_so_custom" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="订单日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.so_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="formadd.so_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                    placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
        </el-form-item>
        <el-button type="primary" class="form-item-save" v-if="ifchange">保 存</el-button>
      </el-form>
    </div>
    <Sosod :formadd="formadd" :ifchange="ifchange"></Sosod>
  </div>
</template>

<script>
import Sosod from './SellSod'
export default {
  name: 'sell_add',
  props: ['editform', 'ifchange'],
  components: {
    Sosod
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
        so_iden: this.editform.so_iden,
        so_orga: this.editform.so_orga,
        so_custom: this.editform.so_custom,
        so_warehouse: this.editform.so_warehouse,
        so_type: this.editform.so_type,
        so_remarks: this.editform.so_remarks,
        so_date: this.editform.so_date
      },
      form_so_custom: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_so_type: [
        '普通发票',
        '退换货'
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.so_iden = this.editform.so_iden
      this.formadd.so_orga = this.editform.so_orga
      this.formadd.so_custom = this.editform.so_custom
      this.formadd.so_warehouse = this.editform.so_warehouse
      this.formadd.so_type = this.editform.so_type
      this.formadd.so_remarks = this.editform.so_remarks
      this.formadd.so_date = this.editform.so_date
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
