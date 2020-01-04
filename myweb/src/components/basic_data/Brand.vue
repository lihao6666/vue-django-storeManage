<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 品牌管理
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
        max-height="580"
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        :row-class-name="tableRowClassName"
        header-cell-class-name="table-header"
      >
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注：">
                <span>{{ props.row.brand_description }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="brand_name" sortable label="名称" :filters="brand_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="brand_creator" sortable label="创建人" :filters="brand_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="brand_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.brand_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.brand_status===0"
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
    <el-dialog title="新增" :visible.sync="alterVisible" width="35%" >
      <div class="container">
        <el-form ref="form" :model="form" label-width="70px"  class="form" >
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.brand_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="form.brand_description"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
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
    <el-dialog title="编辑" :visible.sync="editVisible" width="35%">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="70px">
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.brand_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="editform.brand_description"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {postAPI, getAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      form: {
        brand_name: '',
        brand_description: ''
      },
      oldbrand_name: '',
      oldbrand_status: '',
      brand_nameSet: [],
      brand_creatorSet: [],
      editform: {
        brand_name: '',
        brand_description: ''
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
      let _this = this
      console.log(getAPI('/base/brands'))
      getAPI('/base/brands').then(function (res) {
        _this.tableData = res.data.brands
        _this.tableDataNew = _this.tableData
        let nameset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['brand_name'])
          creatorset.add(_this.tableData[i]['brand_creator'])
        }
        for (let i of nameset) {
          _this.brand_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.brand_creatorSet.push({
            text: i,
            value: i
          })
        }
        _this.pageTotal = res.data.brands.length
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
    // 清除新增表单
    clearform () {
      this.form.brand_name = ''
      this.form.brand_description = ''
    },
    // 停用操作
    handleStop (row) {
      let data = {
        'brand_name': row.brand_name,
        'brand_description': row.brand_description,
        'brand_status': 0,
        'brand_oldname': row.brand_name
      }
      postAPI('/base/brandUpdate', {data: data}).then(function (res) {
        if (res.signal === 0) {
          this.$message.success(`停用成功`)
        } else {
          this.$message.error(`停用失败`)
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.brand_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.brand_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.brand_createDate).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.brand_description).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      let data = {
        'brand_name': row.brand_name,
        'brand_description': row.brand_description,
        'brand_status': 1,
        'brand_oldname': row.brand_name
      }
      postAPI('/base/brandUpdate', {data: data}).then(function (res) {
        if (res.signal === 0) {
          this.$message.success(`启用成功`)
        } else {
          this.$message.error(`启用失败`)
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.brand_name = row.brand_name
      this.editform.brand_description = row.brand_description
      this.oldbrand_name = row.brand_name
      this.oldbrand_status = row.brand_status
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      let _this = this
      let data = {
        'brand_name': this.editform.brand_name,
        'brand_description': this.editform.brand_description,
        'brand_status': this.oldbrand_status,
        'brand_oldname': this.oldbrand_name// 改之前的名字
      }
      postAPI('/base/brandUpdate', data).then(function (res) {
        if (res.data.signal === 0) {
          _this.editVisible = false
          _this.$message.success(`修改成功`)
          _this.getData()
        } else {
          _this.$message.error(`修改失败`)
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      let _this = this
      let data = {
        'brand_name': this.form.brand_name,
        'brand_description': this.form.brand_description,
        'brand_status': 0
      }
      postAPI('/base/brandAdd', data).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`新增成功`)
          _this.clearform()
          _this.alterVisible = false
          _this.getData()
        } else {
          _this.$message.error(`信息已存在`)
        }
      }).catch(function (err) {
        console.log(err)
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
}
</script>

<style>
  .tableRowDisplay {
    display: none;
  }
  .el-row-button-save {
    top: 15px;
  }
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
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
