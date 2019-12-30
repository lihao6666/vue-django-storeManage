<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 用户管理
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
        <el-button type="primary" icon="el-icon-circle-plus-outline" @click="handleAlter" class="alterbutton">新增</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="user_name" sortable label="姓名" align="center"></el-table-column>
        <el-table-column prop="user_id" sortable label="工号" align="center"></el-table-column>
        <el-table-column prop="user_phone_number" sortable label="手机号" align="center"></el-table-column>
        <el-table-column prop="user_mailbox" sortable label="邮箱" align="center"></el-table-column>
        <el-table-column prop="user_area" sortable label="区域" :filters="user_areaSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="user_department" sortable label="部门" :filters="user_dpmSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="user_role" sortable label="角色" :filters="user_roleSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="user_creator" sortable label="创建人" :filters="user_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="user_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.user_status==='启用'"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart( scope.row)"
              v-if="scope.row.user_status==='停用'"
            >启用
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          :total="pageTotal"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>

    <!-- 新增弹出框 -->
    <el-dialog title="新增" :visible.sync="alterVisible" width="30%" >
      <el-form ref="form" :model="form" label-width="80px"  class="form" >
        <el-row>
          <el-form-item label="姓名" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="form.user_name" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="工号" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="form.user_id" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="手机号" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="form.user_phone_number" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="邮箱" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="form.user_mailbox"></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="区域"  align="left">
            <el-select v-model="form.user_area" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="部门"  align="left">
            <el-select v-model="form.user_department" placeholder="请选择部门" class="option" >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="角色"  align="left">
            <el-select v-model="form.user_role" placeholder="请选择角色" class="option">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="创建日期"    class="option" align="left">
              <p>{{time}}</p>
          </el-form-item>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
                <el-button @click="alterVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveAlter">确 定</el-button>
            </span>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
      <el-form ref="form" :model="editform" label-width="80px"  class="form" >
        <el-row>
          <el-form-item label="姓名" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="editform.user_name" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="工号" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="editform.user_id" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="手机号" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="editform.user_phone_number" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="邮箱" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="editform.user_mailbox"></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="区域"  align="left">
            <el-select v-model="editform.user_area" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="部门"  align="left">
            <el-select v-model="editform.user_department" placeholder="请选择部门" class="option" >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="角色"  align="left">
            <el-select v-model="editform.user_role" placeholder="请选择角色" class="option">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
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
import moment from 'moment'
import {postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      time: moment(new Date()).format('YYYY-MM-DD hh:mm:ss'),
      query: {
        pageIndex: 1,
        pageSize: 10
      },
      search: '',
      form: {},
      user_id: '',
      editform: {
        user_name: '',
        user_id: '',
        user_mailbox: '',
        user_area: '',
        user_phone_number: '',
        user_department: '',
        user_role: ''
      },
      tableData: [],
      tableDataNew: [],
      user_roleSet: [],
      user_areaSet: [],
      user_dpmSet: [],
      user_creatorSet: [],
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
      let _this = this
      postAPI('/test2').then(function (res) {
        _this.tableData = res.data.list
        _this.tableDataNew = _this.tableData
        let areaset = new Set()
        let creatorset = new Set()
        let dpmset = new Set()
        let roleset = new Set()
        for (let i in _this.tableData) {
          areaset.add(_this.tableData[i]['user_area'])
          dpmset.add(_this.tableData[i]['user_department'])
          roleset.add(_this.tableData[i]['user_role'])
          creatorset.add(_this.tableData[i]['user_creator'])
        }
        for (let i of areaset) {
          _this.user_areaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.user_creatorSet.push({
            text: i,
            value: i
          })
        }
        for (let i of dpmset) {
          _this.user_dpmSet.push({
            text: i,
            value: i
          })
        }
        for (let i of roleset) {
          _this.user_roleSet.push({
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
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
        String(data.user_name).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.user_id).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.user_phone_number).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.user_mailbox).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.user_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 触发搜索按钮
    handleSearch () {
      this.$set(this.query, 'pageIndex', 1)
      this.getData()
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
    },
    // 禁用操作
    handleStop (index, row) {
      postAPI('/test2', {data: row, status: '停用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 启用
    handleStart (index, row) {
      postAPI('/test2', {data: row, status: '启用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.user_name = row.user_name
      this.editform.user_id = row.user_id
      this.editform.user_mailbox = row.user_mailbox
      this.editform.user_area = row.user_area
      this.editform.user_role = row.user_role
      this.editform.user_phone_number = row.user_phone_number
      this.editform.user_department = row.user_department
      this.user_id = row.user_id
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false
      this.$message.success(`修改成功`)
      postAPI('/test2', {data: this.editform, user_id: this.user_id}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      this.alterVisible = false
      this.$message.success(`新增成功`)
      postAPI('/test2', {data: this.form, table: 'users'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.$set(this.query, 'pageIndex', val)
      this.getData()
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
  .people {
    width:200px;
    position: relative;
  }
  .alterbutton{
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
    width: 600px;
  }
</style>
