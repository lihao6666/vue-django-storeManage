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
          <el-input placeholder="请输入内容" v-model="req_pur.value" class="input-with-select">
            <el-select v-model="req_pur.select" slot="prepend" placeholder="请选择" class="input-select">
              <el-option label="请购单号" value="req_pur_iden"></el-option>
              <el-option label="库存组织" value="req_pur_orga"></el-option>
              <el-option label="需求类型" value="req_pur_type"></el-option>
              <el-option label="申请部门" value="req_pur_from"></el-option>
              <el-option label="创建人" value="req_pur_creator"></el-option>
            </el-select>
            <el-button slot="append" icon="el-icon-search" @click="find"></el-button>
          </el-input>
        <el-button type="primary" icon="el-icon-plus" class="button_plus">新增</el-button>
      </div>
      <el-table
        :data="tableData"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注">
                <span>{{ props.row.req_pur_remarks }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.req_pur_status==='已关闭'" label="关闭人">
                <span>{{ props.row.req_pur_closer }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.req_pur_status==='已关闭'" label="关闭时间">
                <span>{{ props.row.req_pur_closeDate }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.req_pur_status==='已关闭'" label="关闭原因">
                <span>{{ props.row.req_pur_closeReason}}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="req_pur_iden" sortable label="请购单号" align="center"></el-table-column>
        <el-table-column prop="req_pur_orga" sortable label="库存组织" :filters="req_pur_orgaSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="req_pur_type" sortable label="需求类型" :filters="req_pur_typeSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="req_pur_from" sortable label="申请部门" :filters="req_pur_fromSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="req_pur_date" sortable label="请购日期" align="center"></el-table-column>
        <el-table-column prop="req_pur_status" sortable label="状态" :filters="req_pur_statusSet"
      :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top" v-if="scope.row.req_pur_status==='已关闭'">
              <p>关闭人: {{ scope.row.req_pur_closer }}</p>
              <p>关闭时间: {{ scope.row.req_pur_closeDate }}</p>
              <p>关闭原因: {{ scope.row.req_pur_closeReason }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag :type="'info'">{{scope.row.req_pur_status}}</el-tag>
              </div>
            </el-popover>
            <el-tag v-else
              :type="scope.row.req_pur_status==='已审批'?'success':(scope.row.req_pur_status==='已关闭'?'info':'')"
            >{{scope.row.req_pur_status}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="req_pur_creator" sortable label="创建人" :filters="req_pur_creatorSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="req_pur_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.req_pur_status==='草稿'"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.req_pur_status==='草稿'"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              v-if="scope.row.req_pur_status==='已审批' || scope.row.req_pur_status==='已关闭'"
            >详情
            </el-button>
            <el-button
              type="text"
              icon="el-icon-document-delete"
              class="block"
              v-if="scope.row.req_pur_status==='已审批'"
            >关闭
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          @current-change="handlePageChange"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          background
          layout="total, prev, pager, next, jumper"
          :total="pageTotal">
        </el-pagination>
      </div>
    </div>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
      <el-form ref="form" :model="form" label-width="70px">
        <el-form-item label="用户名">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'test',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      req_pur: {
        select: '',
        value: ''
      },
      tableData: [],
      req_pur_orgaSet: [],
      req_pur_typeSet: [],
      req_pur_fromSet: [],
      req_pur_statusSet: [],
      req_pur_creatorSet: [],
      multipleSelection: [],
      delList: [],
      editVisible: false,
      pageTotal: 0,
      form: {},
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
      axios.post('/test').then(function (res) {
        _this.tableData = res.data.list
        let orgaset = new Set()
        let typeset = new Set()
        let statusset = new Set()
        let fromset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['req_pur_orga'])
          fromset.add(_this.tableData[i]['req_pur_from'])
          typeset.add(_this.tableData[i]['req_pur_type'])
          statusset.add(_this.tableData[i]['req_pur_status'])
          creatorset.add(_this.tableData[i]['req_pur_creator'])
        }
        for (let i of orgaset) {
          _this.req_pur_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of fromset) {
          _this.req_pur_fromSet.push({
            text: i,
            value: i
          })
        }
        for (let i of typeset) {
          _this.req_pur_typeSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.req_pur_statusSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.req_pur_creatorSet.push({
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
    find () {
    },
    // 删除操作
    handleDelete (index, row) {
      // 二次确认删除
      this.$confirm('确定要删除吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.$message.success('删除成功');
          this.tableData.splice(index, 1);
        })
        .catch(() => {
        });
    },
    // 编辑操作
    handleEdit (index, row) {
      this.idx = index;
      this.form = row;
      this.editVisible = true;
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false;
      this.$message.success(`修改第 ${this.idx + 1} 行成功`);
      this.$set(this.tableData, this.idx, this.form);
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
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

  .input-with-select {
    width: 50%;
  }
  .input-select {
    width: 130px;
  }
  .button_plus {
    float: right;
  }
</style>
