<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 材料出库
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
                <span>{{ props.row.mso_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="mso_iden" sortable label="出库单编号" align="center"></el-table-column>
        <el-table-column prop="mso_orga" sortable label="库存组织" :filters="mso_orgaSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="mso_warehouse" sortable label="出库仓库" :filters="mso_warehouseSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="mso_type" sortable label="出库分类" :filters="mso_typeSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="mso_date" sortable label="出库日期" align="center"></el-table-column>
        <el-table-column prop="mso_req_department" sortable label="申请部门" :filters="mso_dpmSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="mso_status" sortable label="状态" :filters="mso_statusSet"
                         :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="status[scope.row.mso_status].type"
            >{{status[scope.row.mso_status].label}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="mso_creator" sortable label="创建人" :filters="mso_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="mso_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.mso_status===0"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.mso_status===0"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.mso_status===1"
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
    <el-dialog title="新增" :visible.sync="addVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closeMcadd">
      <MsoAdd ref="Msoadd" @commit="addVisible = false" @save="getData" :editform="addform" :ifchange="true"></MsoAdd>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closeMcedit">
      <MsoAdd ref="Msodit" :editform="editform" :ifchange="true"></MsoAdd>
    </el-dialog>
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%" :destroy-on-close="true">
      <MsoAdd ref="Msomore" :editform="moreform" :ifchange="false"></MsoAdd>
    </el-dialog>
  </div>
</template>

<script>
import MsoAdd from './MosAdd'
import { postAPI } from '../../../../api/api'

export default {
  name: 'mos_check',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      mso_orgaSet: [],
      mso_warehouseSet: [],
      mso_typeSet: [],
      mso_dpmSet: [],
      mso_statusSet: [],
      mso_creatorSet: [],
      editVisible: false,
      editform: {},
      moreVisible: false,
      moreform: {},
      pageTotal: 0,
      addVisible: false,
      addform: {
        mso_iden: '',
        mso_orga: '',
        mso_type: '',
        mso_req_department: '',
        mso_warehouse: '',
        mso_remarks: '',
        mso_date: ''
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
      power: localStorage.getItem('user_power').charAt(8)
    }
  },
  components: {
    MsoAdd
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
      postAPI('/material_so/mso', data).then(function (res) {
        _this.tableData = res.data.mso
        _this.find()
        _this.mso_orgaSet = []
        _this.mso_warehouseSet = []
        _this.mso_typeSet = []
        _this.mso_dpmSet = []
        _this.mso_statusSet = []
        _this.mso_creatorSet = []
        let orgaset = new Set()
        let wareset = new Set()
        let statusset = new Set()
        let typeset = new Set()
        let dpmset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['mso_orga'])
          typeset.add(_this.tableData[i]['mso_type'])
          wareset.add(_this.tableData[i]['mso_warehouse'])
          dpmset.add(_this.tableData[i]['mso_req_department'])
          statusset.add(_this.tableData[i]['mso_status'])
          creatorset.add(_this.tableData[i]['mso_creator'])
        }
        for (let i of orgaset) {
          _this.mso_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of typeset) {
          _this.mso_typeSet.push({
            text: i,
            value: i
          })
        }
        for (let i of wareset) {
          _this.mso_warehouseSet.push({
            text: i,
            value: i
          })
        }
        for (let i of dpmset) {
          _this.mso_dpmSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.mso_statusSet.push({
            text: _this.status[i].label,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.mso_creatorSet.push({
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
          data.mso_iden.toLowerCase().includes(this.search.toLowerCase()) ||
          data.mso_orga.toLowerCase().includes(this.search.toLowerCase()) ||
          data.mso_warehouse.toLowerCase().includes(this.search.toLowerCase()) ||
        data.mso_req_department.toLowerCase().includes(this.search.toLowerCase()) ||
          data.mso_type.toLowerCase().includes(this.search.toLowerCase()) ||
          data.mso_creator.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
      let _this = this
      this.$nextTick(() => _this.$refs.Msoadd.getList())
      this.$nextTick(() => _this.$refs.Msoadd.getForm())
      this.$nextTick(() => _this.$refs.Msoadd.addShow())
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
          postAPI('/material_so/soDelete', row).then(function (res) {
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
      this.$nextTick(() => _this.$refs.poedit.getForm())
      this.$nextTick(() => _this.$refs.Reqedit.getList())
      this.editVisible = true
    },
    // 详情操作
    handleMore (index, row) {
      this.moreform = row
      let _this = this
      this.$nextTick(() => _this.$refs.pomore.getForm())
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
    closeMcedit () {
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
    closeMcadd () {
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

  .input-search {
    width: 50%;
  }
  .button-plus {
    float: right;
    margin-left: 30px;
  }
</style>
