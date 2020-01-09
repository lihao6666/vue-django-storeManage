<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 采购订单
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
        <el-button v-if="power==='2'||power==='3'" type="primary" icon="el-icon-plus" class="button-plus" @click="addpc">按采购合同</el-button>
        <el-button v-if="power==='2'||power==='3'" type="primary" icon="el-icon-plus" class="button-plus" @click="addrp">按请购单</el-button>
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
                <span>{{ props.row.po_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="po_iden" sortable label="订单编号" align="center"></el-table-column>
        <el-table-column prop="orga_name" sortable label="库存组织" :filters="orga_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="supply_name" sortable label="供应商" :filters="supply_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="po_date" sortable label="订单日期" align="center"></el-table-column>
        <el-table-column prop="po_sum" sortable label="价税合计" align="center"></el-table-column>
        <el-table-column prop="pc_iden" sortable label="来源合同" :filters="pc_idenSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="po_status" sortable label="状态" :filters="po_statusSet"
      :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.po_status===1?'success':''"
            >{{status[scope.row.po_status].label}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="po_creator" sortable label="创建人" :filters="po_creatorSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="po_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.po_status===0"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.po_status===0"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.po_status===1"
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
    <!-- 按请购单弹出框 -->
    <el-dialog title="新增" :visible.sync="addrpVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closepoaddrp">
      <Poadd ref="poaddrp" @commit="addrpVisible = false" @save="getData" :editform="addrpform" :ifchange="true"></Poadd>
    </el-dialog>
    <!-- 按采购合同弹出框 -->
    <el-dialog title="新增" :visible.sync="addpcVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closepoaddpc">
      <Poadd ref="poaddpc" @commit="addpcVisible = false" @save="getData" :editform="addpcform" :ifchange="true"></Poadd>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closepoedit">
      <Poadd ref="poedit" @commit="editVisible = false" @save="getData" :editform="editform" :ifchange="true"></Poadd>
    </el-dialog>
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%" :destroy-on-close="true">
      <Poadd ref="pomore" :editform="moreform" :ifchange="false"></Poadd>
    </el-dialog>
  </div>
</template>

<script>
import Poadd from './PurOrdAdd'
import { postAPI } from '../../../api/api'

export default {
  name: 'po_check',
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
      pc_idenSet: [],
      supply_nameSet: [],
      po_statusSet: [],
      po_creatorSet: [],
      editVisible: false,
      editform: {},
      moreVisible: false,
      moreform: {},
      pageTotal: 0,
      addrpVisible: false,
      addpcVisible: false,
      addrpform: {
        po_iden: '',
        orga_name: '',
        supply_name: '',
        pc_iden: '',
        po_remarks: '',
        po_date: '',
        po_sum: 0
      },
      addpcform: {
        po_iden: '',
        orga_name: '',
        supply_name: '',
        pc_iden: '1',
        po_remarks: '',
        po_date: '',
        po_sum: 0
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
      power: localStorage.getItem('user_power').charAt(3)
    }
  },
  components: {
    Poadd
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
      postAPI('/purchase/pOs', data).then(function (res) {
        if (!res.data.pos) {
          return
        }
        _this.tableData = res.data.pos
        _this.pageTotal = res.data.pos.length
        _this.find()
        _this.orga_nameSet = []
        _this.supply_nameSet = []
        _this.pc_idenSet = []
        _this.po_statusSet = []
        _this.po_creatorSet = []
        let orgaset = new Set()
        let nameset = new Set()
        let statusset = new Set()
        let supplyset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['orga_name'])
          supplyset.add(_this.tableData[i]['supply_name'])
          nameset.add(_this.tableData[i]['pc_iden'])
          statusset.add(_this.tableData[i]['po_status'])
          creatorset.add(_this.tableData[i]['po_creator'])
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
          _this.pc_idenSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.po_statusSet.push({
            text: _this.status[i].label,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.po_creatorSet.push({
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
        data.po_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.orga_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.pc_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.supply_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.po_creator.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    addrp () {
      this.addrpVisible = true
      let _this = this
      this.$nextTick(() => _this.$refs.poaddrp.getList())
      this.$nextTick(() => _this.$refs.poaddrp.getForm())
      this.$nextTick(() => _this.$refs.poaddrp.addShow())
    },
    addpc () {
      this.addpcVisible = true
      let _this = this
      this.$nextTick(() => _this.$refs.poaddpc.getList())
      this.$nextTick(() => _this.$refs.poaddpc.getForm())
      this.$nextTick(() => _this.$refs.poaddpc.addShow())
    },
    // 删除操作
    handleDelete (index, row) {
      // 二次确认删除
      this.$confirm('确定要删除吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this

          postAPI('/purchase/pODelete', row).then(function (res) {
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
      this.$nextTick(() => _this.$refs.poedit.getList(row))
      this.editVisible = true
    },
    // 详情操作
    handleMore (index, row) {
      this.moreform = row
      let _this = this
      this.$nextTick(() => _this.$refs.pomore.getForm())
      this.$nextTick(() => _this.$refs.pomore.getList(row))
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
    closepoedit () {
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
    closepoaddrp () {
      this.$confirm('确定要关闭吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.addrpVisible = false
        })
        .catch(() => {
          this.addrpVisible = true
        })
    },
    closepoaddpc () {
      this.$confirm('确定要关闭吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.addpcVisible = false
        })
        .catch(() => {
          this.addpcVisible = true
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
