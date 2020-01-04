<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.bis_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="仓库">
          <el-select v-model="formadd.bis_warehouse" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_bis_warehouse" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-model="formadd.bis_supply" placeholder="请选择" :disabled="!ifchange">
            <el-option v-for="item in form_bis_supply" v-bind:key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="入库日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.bis_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.bis_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
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
import Pood from './BisBd'
export default {
  name: 'bis_add',
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
        bis_iden: this.editform.bis_iden,
        bis_orga: this.editform.bis_orga,
        bis_warehouse: this.editform.bis_warehouse,
        bis_supply: this.editform.bis_supply,
        bis_remarks: this.editform.bis_remarks,
        bis_date: this.editform.bis_date
      },
      form_bis_supply: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_bis_warehouse: [
        '礼品',
        '教学用品',
        '销售商品'
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.bis_iden = this.editform.bis_iden
      this.formadd.bis_orga = this.editform.bis_orga
      this.formadd.bis_warehouse = this.editform.bis_warehouse
      this.formadd.bis_supply = this.editform.bis_supply
      this.formadd.bis_remarks = this.editform.bis_remarks
      this.formadd.bis_date = this.editform.bis_date
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
