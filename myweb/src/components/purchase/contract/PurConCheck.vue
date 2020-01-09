<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 采购合同
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
                <span>{{ props.row.pc_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="pc_iden" sortable label="合同编号" align="center"></el-table-column>
        <el-table-column prop="orga_name" sortable label="库存组织" :filters="orga_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pc_name" sortable label="合同名称" :filters="pc_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="supply_name" sortable label="供应商" :filters="supply_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pc_date" sortable label="签订日期" align="center"></el-table-column>
        <el-table-column prop="pc_sum" sortable label="合同金额" align="center"></el-table-column>
        <el-table-column prop="pc_status" sortable label="状态" :filters="pc_statusSet"
      :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.pc_status===0?'success':''"
            >{{status[scope.row.pc_status].label}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pc_creator" sortable label="创建人" :filters="pc_creatorSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pc_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.pc_status===0"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.pc_status===0"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.pc_status===1"
            >详情
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
      <Pcadd ref="Pcadd" @commit="addVisible = false" @save="getData" :editform="addform" :ifchange="true"></Pcadd>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closePcedit">
      <Pcadd ref="Pcedit" @commit="editVisible = false" @save="getData" :editform="editform" :ifchange="true"></Pcadd>
    </el-dialog>
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%" :destroy-on-close="true">
      <Pcadd ref="Pcmore" :editform="moreform" :ifchange="false"></Pcadd>
    </el-dialog>
  </div>
</template>

<script>
import Pcadd from './PurConAdd'
import {postAPI} from '../../../api/api'

export default {
  name: 'pc_check',
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
      pc_nameSet: [],
      supply_nameSet: [],
      pc_statusSet: [],
      pc_creatorSet: [],
      editVisible: false,
      editform: {},
      moreVisible: false,
      moreform: {},
      pageTotal: 0,
      addVisible: false,
      addform: {
        pc_iden: '',
        orga_name: '',
        supply_name: '',
        pc_name: '',
        pc_remarks: '',
        pc_date: '',
        pc_sum: 0
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
        }
      ],
      power: localStorage.getItem('user_power').charAt(2)
    }
  },
  components: {
    Pcadd
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
      postAPI('/purchase/pcs', data).then(function (res) {
        if (!res.data.pcs) {
          return
        }
        _this.tableData = res.data.pcs
        _this.pageTotal = res.data.pcs.length
        _this.find()
        _this.orga_nameSet = []
        _this.supply_nameSet = []
        _this.pc_nameSet = []
        _this.pc_statusSet = []
        _this.pc_creatorSet = []
        let orgaset = new Set()
        let nameset = new Set()
        let statusset = new Set()
        let supplyset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['orga_name'])
          supplyset.add(_this.tableData[i]['supply_name'])
          nameset.add(_this.tableData[i]['pc_name'])
          statusset.add(_this.tableData[i]['pc_status'])
          creatorset.add(_this.tableData[i]['pc_creator'])
        }
        for (let i of orgaset) {
          _this.orga_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of supplyset) {
          _this.supply_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of nameset) {
          _this.pc_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.pc_statusSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.pc_creatorSet.push({
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
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
        data.pc_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.orga_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.pc_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.supply_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.pc_creator.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
      let _this = this
      this.$nextTick(() => _this.$refs.Pcadd.getList())
      this.$nextTick(() => _this.$refs.Pcadd.getForm())
      this.$nextTick(() => _this.$refs.Pcadd.addShow())
    },
    // 删除操作
    handleDelete (index, row) {
      // 二次确认删除
      this.$confirm('确定要删除吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this

          postAPI('/purchase/pcDelete', row).then(function (res) {
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
      this.$nextTick(() => _this.$refs.Pcedit.getForm())
      this.$nextTick(() => _this.$refs.Pcedit.getList())
      this.editVisible = true
    },
    // 详情操作
    handleMore (index, row) {
      this.moreform = row
      let _this = this
      this.$nextTick(() => _this.$refs.Pcmore.getForm())
      this.moreVisible = true
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
    margin-left: 30px;
  }
</style>
