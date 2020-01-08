<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 物料维护
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-input
          placeholder="关键字搜索"
          prefix-icon="el-icon-search"
          class="input-search"
          @input="find"
          clearable
          v-model="search">
        </el-input>
        <el-button type="primary" icon="el-icon-plus" @click="handleAlter" class="alter-button">新增</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        :row-class-name="tableRowClassName"
        header-cell-class-name="table-header"
      >
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="material_iden" sortable label="编码" align="center"></el-table-column>
        <el-table-column prop="material_name" sortable label="名称" :filters="material_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_specification" sortable label="规格" :filters="material_specSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_model" sortable label="型号" :filters="material_modelSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="meterage_name" sortable label="计量单位" :filters="meterage_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_attr" sortable label="存货属性" :filters="material_attrSet"
                         :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.material_attr===0?'success':(scope.row.material_attr===1?'info':'')">{{materialattr[scope.row.material_attr].label}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="material_creator" sortable label="创建人" :filters="material_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.row)"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-unlock"
              class="red"
              @click="handleStop(scope.row)"
              v-if="scope.row.material_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.material_status===0"
            >启用
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
          :page-sizes="[5, 10, 20, 50, 100, 200, 500]"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="pageTotal">
        </el-pagination>
      </div>
    </div>

    <!-- 新增弹出框 -->
    <el-dialog title="新增" :visible.sync="alterVisible" width="35%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="form" label-width="100px"  class="form" >
          <el-row>
            <el-form-item label="分类" class="inputs" align="left">
              <el-col :span="10">
                <el-cascader :options="options" :props="{ expandTrigger: 'hover', checkStrictly: true  }"
                             clearable @change="changeCascaderType">
                  <template slot-scope="{ node, data }">
                    <span>{{ data.label }}</span>
                    <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                  </template>
                </el-cascader>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.material_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="规格" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.material_specification" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="型号" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.material_model" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="计量单位"  align="left">
              <el-cascader :show-all-levels="false" :options="meterage_options"
                           :props="{ expandTrigger: 'hover'}" @change="changeCascaderMeterage"></el-cascader>
            </el-form-item>
          </el-row>
          <el-row>
          <el-form-item label="存货属性"  align="left">
            <el-select v-model="form.material_attr" placeholder="请选择"  class="option" >
                <el-option v-for="item in materialattr" v-bind:key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveAlter">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="35%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="100px">
          <el-row>
            <el-form-item label="编码" class="inputs" align="left">
              <el-col :span="10">
                <el-tag>{{editform.material_iden}}</el-tag>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.material_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="规格" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.material_specification" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="型号" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.material_model" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="计量单位"  align="left">
              <el-cascader v-model="editform.meterage_name" :show-all-levels="false" :options="meterage_options"
                           :props="{ expandTrigger: 'hover'}" @change="changeCascader"></el-cascader>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="存货属性"  align="left">
              <el-select v-model="editform.material_attr" placeholder="请选择"  class="option" >
                <el-option v-for="item in materialattr" v-bind:key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="editVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {getAPI, postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      materialattr: [
        {
          value: 0,
          label: '存货'
        },
        {
          value: 1,
          label: '固定资产'
        },
        {
          value: 2,
          label: '费用'
        }
      ],
      options: [],
      meterage_options: [],
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      form: {
        material_type_iden: '',
        material_name: '',
        material_specification: '',
        material_model: '',
        meterage_name: '',
        material_attr: ''
      },
      material_name: '',
      material_specSet: [],
      material_nameSet: [],
      material_modelSet: [],
      meterage_nameSet: [],
      material_attrSet: [],
      material_creatorSet: [],
      editform: {
        material_iden: '',
        material_name: '',
        material_specification: '',
        material_model: '',
        meterage_name: '',
        material_attr: ''
      },
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
      delList: [],
      alterVisible: false,
      editVisible: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      this.getlist()
      let _this = this
      getAPI('/base/materials').then(function (res) {
        if (!res.data.materials) {
          return
        }
        _this.tableData = res.data.materials
        _this.pageTotal = res.data.materials.length
        _this.find()
        _this.material_specSet = []
        _this.material_nameSet = []
        _this.material_modelSet = []
        _this.meterage_nameSet = []
        _this.material_attrSet = []
        _this.material_creatorSet = []
        let nameset = new Set()
        let specset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        let attrset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['material_name'])
          specset.add(_this.tableData[i]['material_specification'])
          modelset.add(_this.tableData[i]['material_model'])
          meterageset.add(_this.tableData[i]['meterage_name'])
          attrset.add(_this.tableData[i]['material_attr'])
          creatorset.add(_this.tableData[i]['material_creator'])
        }
        for (let i of nameset) {
          _this.material_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specset) {
          _this.material_specSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.material_modelSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.meterage_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of attrset) {
          _this.material_attrSet.push({
            text: _this.materialattr[i].label,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.material_creatorSet.push({
            text: i,
            value: i
          })
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 表格每行的class样式
    tableRowClassName ({row, rowIndex}) {
      this.pageTotal = rowIndex + 1
      if (rowIndex >= (this.query.pageIndex - 1) * this.query.pageSize && rowIndex < this.query.pageIndex * this.query.pageSize) {
        return ''
      }
      return 'tableRowDisplay'
    },
    // 表格下拉筛选
    filter (value, row, column) {
      const property = column['property']
      if (row[property] === value) {
        return true
      }
      return false
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
    },
    // 一键清除新增表单
    clearform () {
      this.form.material_attr = ''
      this.form.material_iden = ''
      this.form.material_model = ''
      this.form.material_specification = ''
      this.form.material_name = ''
    },
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.material_status = 0
          postAPI('/base/materialStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`停用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.material_status = 1
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`停用失败`)
            row.material_status = 1
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消停用'
          })
        })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.material_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_specification).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_model).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.meterage_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.meterage_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_attr).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      this.$confirm('确定要启用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.material_status = 1
          postAPI('/base/materialStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`启用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.material_status = 0
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`启用失败`)
            row.material_status = 0
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消启用'
          })
        })
    },
    // 选择分类
    changeCascaderType (val) {
      this.form.material_type_iden = val[val.length - 1]
    },
    // 新增选择计量单位
    changeCascaderMeterage (val) {
      this.form.meterage_name = val[val.length - 1]
    },
    // 编辑选择计量单位
    changeCascader (val) {
      this.editform.meterage_name = val[val.length - 1]
    },
    // 获取级联选择器
    optionsAdd (parent, child, length, end) {
      if (length === end) {
        parent.push({
          value: child[0],
          label: child[1],
          children: []
        })
        return
      }
      let pub = child[0].substring(0, length)
      for (let i in parent) {
        if (parent[i].value === pub) {
          this.optionsAdd(parent[i].children, child, length + 2, end)
          return
        }
      }
      parent.push({
        value: child[0],
        label: child[1],
        children: []
      })
    },
    // 获取列表
    getlist () {
      let _this = this
      getAPI('/base/materialNew').then(function (res) {
        console.log(res.data)
        _this.options = []
        let length = 2
        while (res.data.material_types.length > 0) {
          for (let i = 0; i < res.data.material_types.length; i++) {
            if (res.data.material_types[i][0].length === length) {
              _this.optionsAdd(_this.options, res.data.material_types[i], 2, length)
              res.data.material_types.splice(i, 1)
              i -= 1
            }
          }
          length += 2
        }
        _this.meterage_options = [
          {
            value: 0,
            label: '重量',
            children: []
          },
          {
            value: 1,
            label: '长度',
            children: []
          },
          {
            value: 2,
            label: '面积',
            children: []
          },
          {
            value: 3,
            label: '体积',
            children: []
          },
          {
            value: 4,
            label: '件数',
            children: []
          }
        ]
        for (let i in res.data.meterages) {
          _this.meterage_options[res.data.meterages[i][0]].children.push({
            value: res.data.meterages[i][2],
            label: res.data.meterages[i][2]
          })
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.material_name = row.material_name
      this.editform.material_iden = row.material_iden
      this.editform.material_specification = row.material_specification
      this.editform.material_model = row.material_model
      this.editform.meterage_name = row.meterage_name
      this.editform.material_attr = row.material_attr
      this.editform.id = row.id
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      if (!this.editform.material_name || !this.editform.material_specification ||
      !this.editform.material_model || !this.editform.meterage_name || (this.editform.material_attr !== 0 && !this.editform.material_attr)) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      postAPI('/base/materialUpdate', this.editform).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`修改成功`)
          _this.editVisible = false
          _this.getData()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        console.log(err)
        _this.$message.error(`修改失败`)
      })
    },
    // 保存新增
    saveAlter () {
      console.log(this.form)
      if (!this.form.material_name || !this.form.material_type_iden || !this.form.material_specification ||
      !this.form.material_model || !this.form.meterage_name || (this.form.material_attr !== 0 && !this.form.material_attr)) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      postAPI('/base/materialAdd', this.form).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`新增成功`)
          _this.alterVisible = false
          _this.clearform()
          _this.getData()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        console.log(err)
        _this.$message.error(`新增失败`)
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    }
  }
}</script>

<style>
  .tableRowDisplay {
    display: none;
  }
  .el-row-button-save {
    top: 15px;
  }
</style>

<style scoped>
  .handle-box {
    margin-bottom: 20px;
    position: relative;
  }

  .input-search {
    width: 50%;
  }
  .alter-button{
    position: absolute;
    right:0;
  }

  .table {
    width: 100%;
    font-size: 14px;
  }
  .red {
    color: #ff0000;
  }
  .green {
    color: GREEN;
  }
  .inputs {
    width: 590px;
  }
</style>
