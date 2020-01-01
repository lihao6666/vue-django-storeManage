<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 库存组织管理
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
        <el-button type="primary" icon="el-icon-circle-plus-outline" @click="handleAlter" class="alter-button">新增</el-button>
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
                <span>{{ props.row.orga_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="orga_iden" sortable label="编码"  align="center"></el-table-column>
        <el-table-column prop="orga_name" sortable label="名称" :filters="orga_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="orga_area" sortable label="区域" :filters="orga_areaSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="orga_creator" sortable label="创建人" :filters="orga_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="orga_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.orga_status==='启用'"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.orga_status==='停用'"
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
      <el-form ref="form" :model="form" label-width="70px"  class="form" >
        <el-row>
        <el-form-item label="编码" class="inputs" align="left">
          <el-col :span="10">
            <el-input v-model="form.orga_iden" ></el-input>
          </el-col>
        </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="名称" class="inputs"  align="left">
            <el-col :span="10">
              <el-input v-model="form.orga_name" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="区域"  align="left">
            <el-select v-model="form.orga_area" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in area_options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="备注" align="left">
            <el-input type="textarea" class="textarea" v-model="form.orga_remarks"
                      placeholder="请输入内容" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
          </el-form-item>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
                <el-button @click="alterVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveAlter">确 定</el-button>
            </span>
    </el-dialog>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="35%">
      <el-form ref="form" :model="editform" label-width="70px">
        <el-row>
          <el-form-item label="编码" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="editform.orga_iden" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="名称" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="editform.orga_name" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="区域"  align="left">
            <el-select v-model="editform.orga_area" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in area_options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="备注" align="left">
            <el-input type="textarea" class="textarea" v-model="editform.orga_remarks"
                      placeholder="请输入内容" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
          </el-form-item>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
    </el-dialog>
  </div>
</template>

<script>
import {postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      area_options: [],
      query: {
        pageIndex: 1,
        pageSize: 10
      },
      search: '',
      form: {
        orga_iden: '',
        orga_name: '',
        orga_remarks: '',
        orga_area: ''
      },
      orga_iden: '',
      orga_nameSet: [],
      orga_areaSet: [],
      orga_creatorSet: [],
      editform: {
        orga_iden: '',
        orga_name: '',
        orga_remarks: '',
        orga_area: ''
      },
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
      delList: [],
      alterVisible: false,
      editVisible: false,
      pageTotal: 0,
      idx: -1,
      id: -1
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      this.getlist()
      let _this = this
      postAPI('/organization').then(function (res) {
        _this.tableData = res.data.list
        _this.tableDataNew = _this.tableData
        let nameset = new Set()
        let areaset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['orga_name'])
          areaset.add(_this.tableData[i]['orga_area'])
          creatorset.add(_this.tableData[i]['orga_creator'])
        }
        for (let i of nameset) {
          _this.orga_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of areaset) {
          _this.orga_areaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.orga_creatorSet.push({
            text: i,
            value: i
          })
        }
        _this.pageTotal = res.data.list.length
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
      let _this = this
      postAPI('/organization').then(function (res) {
        let maxiden = String(parseInt(res.data.max_iden) + 1)
        _this.form.orga_iden = maxiden
        for (let i = 0; i < 6 - maxiden.length; i++) {
          _this.form.orga_iden = '0' + _this.form.orga_iden
        }
      })
    },
    // 一键清除新增表单
    clearform () {
      this.form.orga_area = ''
      this.form.orga_iden = ''
      this.form.orga_name = ''
      this.form.orga_remarks = ''
    },
    // 禁用操作
    handleStop (row) {
      postAPI('/organization', {data: row, orga_status: '停用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.orga_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_area).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_createDate).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      postAPI('/organization', {data: row, orga_status: '启用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 获取列表
    getlist () {
      let _this = this
      postAPI('/area').then(function (res) {
        let alterarea = new Set()
        for (let i in res.data.list) {
          alterarea.add(res.data.list[i]['area_name'])
        }
        for (let j of alterarea) {
          _this.area_options.push(j)
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.orga_iden = row.orga_iden
      this.editform.orga_name = row.orga_name
      this.editform.orga_area = row.orga_area
      this.editform.orga_remarks = row.orga_remarks
      this.orga_iden = row.orga_iden
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false
      this.$message.success(`修改成功`)
      postAPI('/organization', {data: this.editform, orga_iden: this.orga_iden}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      this.alterVisible = false
      this.$message.success(`新增成功`)
      this.clearform()
      postAPI('/organization', {data: this.form, table: 'organization'}).then(function (res) {
        console.log(res)
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
