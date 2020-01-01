<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 中心仓库维护
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
                <span>{{ props.row.center_wh_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="center_wh_name" sortable label="仓库编码"  align="center"></el-table-column>
        <el-table-column prop="center_wh_belong_orga" sortable label="所属组织" :filters="center_wh_orgaSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="center_wh_name" sortable label="仓库名称" :filters="center_wh_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="center_wh_belong_center" sortable label="所属中心" :filters="center_wh_centerSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="center_wh_belong_brand" sortable label="所属品牌" :filters="center_wh_brandSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="center_wh_creator" sortable label="创建人" :filters="center_wh_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="center_wh_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.center_wh_status==='启用'"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.center_wh_status==='停用'"
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
          <el-form-item label="所属组织"  align="left">
            <el-select v-model="form.center_wh_belong_orga" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in orga_options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="仓库编码" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="form.center_wh_iden" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="仓库名称" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="form.center_wh_name" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="所属中心"  align="left">
            <el-select v-model="form.center_wh_belong_center" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in center_options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="所属品牌"  align="left">
            <el-select v-model="form.center_wh_belong_brand" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in brand_options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="备注" align="left">
            <el-input type="textarea" class="textarea" v-model="form.center_wh_remarks"
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
      <el-form ref="form" :model="editform" label-width="70px"  class="form" >
        <el-row>
          <el-form-item label="所属组织"  align="left">
            <el-select v-model="editform.center_wh_belong_orga" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in orga_options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="仓库编码" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="editform.center_wh_iden" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="仓库名称" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="editform.center_wh_name" ></el-input>
            </el-col>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="所属中心"  align="left">
            <el-select v-model="editform.center_wh_belong_center" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in center_options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="所属品牌"  align="left">
            <el-select v-model="editform.center_wh_belong_brand" placeholder="请选择区域"  class="option" >
              <el-option
                v-for="item in brand_options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-row>
        <el-row>
          <el-form-item label="备注" align="left">
            <el-input type="textarea" class="textarea" v-model="editform.center_wh_remarks"
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
      orga_options: [],
      center_options: [],
      brand_options: [],
      query: {
        pageIndex: 1,
        pageSize: 10
      },
      search: '',
      form: {
        center_wh_name: '',
        center_wh_remarks: '',
        center_wh_iden: '',
        center_wh_belong_orga: '',
        center_wh_belong_center: '',
        center_wh_belong_brand: ''
      },
      center_wh_iden: '',
      center_wh_nameSet: [],
      center_wh_orgaSet: [],
      center_wh_centerSet: [],
      center_wh_brandSet: [],
      center_wh_creatorSet: [],
      editform: {
        center_wh_name: '',
        center_wh_remarks: '',
        center_wh_iden: '',
        center_wh_belong_orga: '',
        center_wh_belong_center: '',
        center_wh_belong_brand: ''
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
      postAPI('/store').then(function (res) {
        _this.tableData = res.data.list
        _this.tableDataNew = _this.tableData
        let nameset = new Set()
        let orgaset = new Set()
        let centerset = new Set()
        let brandset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['center_wh_name'])
          orgaset.add(_this.tableData[i]['center_wh_belong_orga'])
          brandset.add(_this.tableData[i]['center_wh_belong_brand'])
          centerset.add(_this.tableData[i]['center_wh_belong_center'])
          creatorset.add(_this.tableData[i]['center_wh_creator'])
        }
        for (let i of nameset) {
          _this.center_wh_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of orgaset) {
          _this.center_wh_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of centerset) {
          _this.center_wh_centerSet.push({
            text: i,
            value: i
          })
        }
        for (let i of brandset) {
          _this.center_wh_brandSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.center_wh_creatorSet.push({
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
      postAPI('/store').then(function (res) {
        let maxiden = String(parseInt(res.data.max_iden) + 1)
        _this.form.store_iden = maxiden
        for (let i = 0; i < 6 - maxiden.length; i++) {
          _this.form.store_iden = '0' + _this.form.store_iden
        }
      })
    },
    // 一键清除新增表单
    clearform () {
      this.form.center_wh_belong_brand = ''
      this.form.center_wh_belong_center = ''
      this.form.center_wh_belong_orga = ''
      this.form.center_wh_iden = ''
      this.form.center_wh_name = ''
      this.form.center_wh_remarks = ''
    },
    // 禁用操作
    handleStop (row) {
      postAPI('/store', {data: row, center_wh_status: '停用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.center_wh_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.center_wh_belong_orga).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.center_wh_belong_brand).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.center_wh_belong_center).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.center_wh_createDate).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.center_wh_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.center_wh_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      postAPI('/store', {data: row, center_wh_status: '启用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 获取列表
    getlist () {
      let _this = this
      postAPI('/organization').then(function (res) {
        let alterorga = new Set()
        for (let i in res.data.list) {
          alterorga.add(res.data.list[i]['orga_name'])
        }
        for (let j of alterorga) {
          _this.orga_options.push(j)
        }
      }).catch(function (err) {
        console.log(err)
      })
      postAPI('/center').then(function (res) {
        let altercenter = new Set()
        for (let i in res.data.list) {
          altercenter.add(res.data.list[i]['center_name'])
        }
        for (let j of altercenter) {
          _this.center_options.push(j)
        }
      }).catch(function (err) {
        console.log(err)
      })
      postAPI('/brand').then(function (res) {
        let alterbrand = new Set()
        for (let i in res.data.list) {
          alterbrand.add(res.data.list[i]['brand_name'])
        }
        for (let j of alterbrand) {
          _this.brand_options.push(j)
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.center_wh_iden = row.center_wh_iden
      this.editform.center_wh_name = row.center_wh_name
      this.editform.center_wh_belong_orga = row.center_wh_belong_orga
      this.editform.center_wh_belong_brand = row.center_wh_belong_brand
      this.editform.center_wh_belong_center = row.center_wh_belong_center
      this.editform.center_wh_remarks = row.center_wh_remarks
      this.center_wh_iden = row.center_wh_iden
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false
      this.$message.success(`修改成功`)
      postAPI('/store', {data: this.editform, center_wh_iden: this.center_wh_iden}).then(function (res) {
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
      postAPI('/store', {data: this.form, table: 'center_warehouse'}).then(function (res) {
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
