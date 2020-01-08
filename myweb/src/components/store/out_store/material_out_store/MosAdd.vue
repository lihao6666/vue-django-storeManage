<template>
  <div>
    <div class="container">
      <el-form ref="form" :inline="true" :model="formadd" label-width="70px" size="mini">
        <el-form-item label="库存组织">
          <el-tag
            :type="'success'"
          >{{formadd.mos_orga}}
          </el-tag>
        </el-form-item>
        <el-form-item label="出库仓库">
          <el-tag
            :type="'success'"
          >{{formadd.mos_warehouse}}
          </el-tag>
        </el-form-item>
        <el-form-item label="出库类型"  align="left">
          <el-select v-model="formadd.mos_type" placeholder="请选择类型"  class="option" >
            <el-option v-for="item in mostype" v-bind:key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="出库日期">
          <el-col :span="11">
            <el-date-picker
              v-model="formadd.mos_date"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
              :picker-options="pickerOptions" :disabled="!ifchange">
            </el-date-picker>
          </el-col>
        </el-form-item>
        <el-row>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="formadd.mos_remarks" rows="3" class="form-item-from" :disabled="!ifchange"
                      placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
          </el-form-item>
          <el-button type="primary" class="form-item-save" v-if="ifchange">保 存</el-button>
        </el-row>
      </el-form>
    </div>
    <MosDetail :formadd="formadd" :ifchange="ifchange"></MosDetail>
  </div>
</template>

<script>
import MosDetail from './MosDetail'
export default {
  name: 'mos_add',
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
        mos_iden: this.editform.mos_iden,
        mos_orga: this.editform.mos_orga,
        mos_warehouse: this.editform.mos_warehouse,
        mos_remarks: this.editform.mos_remarks,
        mos_date: this.editform.mos_date
      },
      form_mos_transfer: [
        '礼品',
        '教学用品',
        '销售商品'
      ],
      form_mos_warehouse: [
        'a',
        'b',
        'c'
      ],
      mostype: [
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
      ]
    }
  },
  methods: {
    getForm () {
      this.formadd.mos_iden = this.editform.mos_iden
      this.formadd.mos_orga = this.editform.mos_orga
      this.formadd.mos_warehouse = this.editform.mos_warehouse
      this.formadd.mos_remarks = this.editform.mos_remarks
      this.formadd.mos_date = this.editform.mos_date
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
