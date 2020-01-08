<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 请购单
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
        <el-button v-if="power==='2'||power==='3'" type="primary" icon="el-icon-plus" class="button-plus" @click="add">新增</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注">
                <span>{{ props.row.pr_remarks }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.pr_status==='已关闭'" label="关闭人">
                <span>{{ props.row.pr_closer }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.pr_status==='已关闭'" label="关闭时间">
                <span>{{ props.row.pr_closeDate }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.pr_status==='已关闭'" label="关闭原因">
                <span>{{ props.row.pr_closeReason}}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="pr_iden" sortable label="请购单号" align="center"></el-table-column>
        <el-table-column prop="orga_name" sortable label="库存组织" :filters="orga_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pr_type" sortable label="需求类型" :filters="pr_typeSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pr_department" sortable label="申请部门" :filters="pr_departmentSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pr_date" sortable label="请购日期" align="center"></el-table-column>
        <el-table-column prop="pr_status" sortable label="状态" :filters="pr_statusSet"
      :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top" v-if="scope.row.pr_status===2">
              <p>关闭人: {{ scope.row.pr_closer }}</p>
              <p>关闭时间: {{ scope.row.pr_closeDate }}</p>
              <p>关闭原因: {{ scope.row.pr_closeReason }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag :type="status[scope.row.pr_status].type">{{status[scope.row.pr_status].label}}</el-tag>
              </div>
            </el-popover>
            <el-tag v-else
              :type="status[scope.row.pr_status].type"
            >{{status[scope.row.pr_status].label}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pr_creator" sortable label="创建人" :filters="pr_creatorSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pr_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.pr_status===0"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.pr_status===0"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.pr_status==='1' || scope.row.pr_status===2"
            >详情
            </el-button>
            <el-button
              type="text"
              icon="el-icon-document-delete"
              class="block"
              @click="handleClose(scope.$index, scope.row)"
              v-if="scope.row.pr_status===1"
            >关闭
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
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
    <el-dialog title="新增" :visible.sync="addVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closePcadd">
      <Reqadd ref="Reqadd" @commit="addVisible = false" @save="getData" :editform="addform" :ifchange="true"></Reqadd>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closePcedit">
      <Reqadd ref="Reqedit" @commit="editVisible = false" @save="getData" :editform="editform" :ifchange="true"></Reqadd>
    </el-dialog>
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%" :destroy-on-close="true">
      <Reqadd ref="Reqmore" :editform="moreform" :ifchange="false"></Reqadd>
    </el-dialog>
  </div>
</template>

<script>
import Reqadd from './ReqPurAdd'
import { postAPI } from '../../../api/api'

export default {
  name: 'pr_check',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      orga_nameSet: [],
      pr_typeSet: [],
      pr_departmentSet: [],
      pr_statusSet: [],
      pr_creatorSet: [],
      editVisible: false,
      editform: {},
      moreVisible: false,
      moreform: {},
      pageTotal: 0,
      addVisible: false,
      addform: {
        pr_iden: '',
        orga_name: '',
        pr_department: '',
        pr_type: '',
        pr_remarks: '',
        pr_date: ''
      },
      status: [
        {
          value: 0,
          label: '草稿',
          type: ''
        },
        {
          value: 1,
          label: '已审批',
          type: 'success'
        },
        {
          value: 2,
          label: '已关闭',
          type: 'info'
        }
      ],
      power: localStorage.getItem('user_power').charAt(1)
    }
  },
  components: {
    Reqadd
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      let data = {
        power: this.power
      }
      console.log(data)
      postAPI('/purchaseRequest/prs', data).then(function (res) {
        if (!res.data.prs) {
          return
        }
        _this.tableData = res.data.prs
        _this.find()
        _this.orga_nameSet = []
        _this.pr_typeSet = []
        _this.pr_departmentSet = []
        _this.pr_statusSet = []
        _this.pr_creatorSet = []
        let orgaset = new Set()
        let typeset = new Set()
        let statusset = new Set()
        let fromset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['orga_name'])
          fromset.add(_this.tableData[i]['pr_department'])
          typeset.add(_this.tableData[i]['pr_type'])
          statusset.add(_this.tableData[i]['pr_status'])
          creatorset.add(_this.tableData[i]['pr_creator'])
        }
        for (let i of orgaset) {
          _this.orga_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of fromset) {
          _this.pr_departmentSet.push({
            text: i,
            value: i
          })
        }
        for (let i of typeset) {
          _this.pr_typeSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.pr_statusSet.push({
            text: _this.status[i].label,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.pr_creatorSet.push({
            text: i,
            value: i
          })
        }
        _this.pageTotal = res.data.prs.length
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
        data.pr_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.orga_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.pr_type.toLowerCase().includes(this.search.toLowerCase()) ||
        data.pr_department.toLowerCase().includes(this.search.toLowerCase()) ||
        data.pr_creator.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
      let _this = this
      this.$nextTick(() => _this.$refs.Reqadd.getList())
      this.$nextTick(() => _this.$refs.Reqadd.getForm())
      this.$nextTick(() => _this.$refs.Reqadd.addShow())
    },
    // 删除操作
    handleDelete (index, row) {
      // 二次确认删除
      this.$confirm('确定要删除吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          console.log(row)
          postAPI('/purchaseRequest/prDelete', row).then(function (res) {
            console.log(res.data)
            if (res.data.signal === 0) {
              _this.$message.success(`删除成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
            }
          }).catch(function (err) {
            _this.$message.error('删除失败')
            console.log(err)
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消删除'
          })
        })
    },
    // 编辑操作
    handleEdit (index, row) {
      this.editform = row
      let _this = this
      this.$nextTick(() => _this.$refs.Reqedit.getForm())
      this.$nextTick(() => _this.$refs.Reqedit.getList())
      this.editVisible = true
    },
    // 详情操作
    handleMore (index, row) {
      this.moreform = row
      let _this = this
      this.$nextTick(() => _this.$refs.Reqmore.getForm())
      this.moreVisible = true
    },
    // 关闭操作
    handleClose (index, row) {
      this.$prompt('请输入关闭原因', '关闭', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(({ value }) => {
        this.$confirm('确定要关闭吗？', '提示', {
          type: 'warning'
        }).then(() => {
          this.$message.success('关闭成功')
          let _this = this
          console.log(value)
          let data = row
          data.pr_closerReason = value
          postAPI('/purchaseRequest/prClose', data).then(function (res) {
            console.log(res.data)
            if (res.data.signal === 0) {
              _this.$message.success(`关闭成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
            }
          }).catch(function (err) {
            _this.$message.error('关闭失败')
            console.log(err)
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消关闭'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消关闭'
        })
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    },
    // 关闭窗口二次确认
    closePcedit () {
      this.$confirm('确定要关闭吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.editVisible = false
        })
        .catch(() => {
          this.editVisible = true
        })
    },
    closePcadd () {
      this.$confirm('确定要关闭吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.addVisible = false
        })
        .catch(() => {
          this.addVisible = true
        })
    }
  }
}
</script>

<style>
  .tableRowDisplay {
    display: none;
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
  }
  .table {
    width: 100%;
    font-size: 14px;
  }
  .red {
    color: #ff0000;
  }
  .green {
    color: #00a854;
  }
  .block {
    color: grey;
  }
  .input-search {
    width: 50%;
  }
  .button-plus {
    float: right;
  }
</style>
