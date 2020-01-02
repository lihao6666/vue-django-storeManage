<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-select v-model="formadd.pc_orga" placeholder="请选择" :disabled="!ifchange">
            <el-option  v-for="item in form_pc_orga" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
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
        <el-form-item label="备注">
          <el-input type="textarea" v-model="formadd.pc_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                    placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
        </el-form-item>
        <el-button type="primary" class="form-item-save" v-if="ifchange">保 存</el-button>
      </el-form>
    </div>
    <Pccd :formadd="formadd" :ifchange="ifchange"></Pccd>
    <Pcpay :formadd="formadd" :ifchange="ifchange"></Pcpay>
    <el-row :gutter="20" v-if="ifchange" class="el-row-button">
      <el-col :span="1" :offset="18">
        <el-button >取 消</el-button>
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
        pc_orga: this.editform.pc_orga,
        pc_name: this.editform.pc_name,
        pc_supply: this.editform.pc_supply,
        pc_remarks: this.editform.pc_remarks,
        pc_date: this.editform.pc_date,
        pc_sum: this.editform.pc_sum
      },
      form_pc_orga: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_pc_supply: [
        '礼品',
        '教学用品',
        '销售商品'
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.pc_orga = this.editform.pc_orga
      this.formadd.pc_name = this.editform.pc_name
      this.formadd.pc_supply = this.editform.pc_supply
      this.formadd.pc_remarks = this.editform.pc_remarks
      this.formadd.pc_date = this.editform.pc_date
      this.formadd.pc_sum = this.editform.pc_sum
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
  .null {
    width: 70%;
  }
  .button-save {
    margin-left: 30px;
  }
  .el-row-button {
    top: 15px;
  }
</style>
