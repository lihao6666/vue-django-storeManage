(global["webpackJsonp"] = global["webpackJsonp"] || []).push([["components/w-picker/w-picker"],{

/***/ 310:
/*!***************************************************************************!*\
  !*** C:/Users/流宇/Desktop/git/uni-appWeb/components/w-picker/w-picker.vue ***!
  \***************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./w-picker.vue?vue&type=template&id=7f1a73dd& */ 311);
/* harmony import */ var _w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./w-picker.vue?vue&type=script&lang=js& */ 313);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__) if(__WEBPACK_IMPORT_KEY__ !== 'default') (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__[key]; }) }(__WEBPACK_IMPORT_KEY__));
/* harmony import */ var _w_picker_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./w-picker.vue?vue&type=style&index=0&lang=scss& */ 319);
/* harmony import */ var _E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/runtime/componentNormalizer.js */ 14);

var renderjs





/* normalize component */

var component = Object(_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__["render"],
  _w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"],
  false,
  null,
  null,
  null,
  false,
  _w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__["components"],
  renderjs
)

/* hot reload */
if (false) { var api; }
component.options.__file = "C:/Users/流宇/Desktop/git/uni-appWeb/components/w-picker/w-picker.vue"
/* harmony default export */ __webpack_exports__["default"] = (component.exports);

/***/ }),

/***/ 311:
/*!**********************************************************************************************************!*\
  !*** C:/Users/流宇/Desktop/git/uni-appWeb/components/w-picker/w-picker.vue?vue&type=template&id=7f1a73dd& ***!
  \**********************************************************************************************************/
/*! exports provided: render, staticRenderFns, recyclableRender, components */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_16_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--16-0!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/template.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-uni-app-loader/page-meta.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./w-picker.vue?vue&type=template&id=7f1a73dd& */ 312);
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "render", function() { return _E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_16_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__["render"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return _E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_16_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "recyclableRender", function() { return _E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_16_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__["recyclableRender"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "components", function() { return _E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_16_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_template_id_7f1a73dd___WEBPACK_IMPORTED_MODULE_0__["components"]; });



/***/ }),

/***/ 312:
/*!**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--16-0!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/template.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-uni-app-loader/page-meta.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!C:/Users/流宇/Desktop/git/uni-appWeb/components/w-picker/w-picker.vue?vue&type=template&id=7f1a73dd& ***!
  \**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! exports provided: render, staticRenderFns, recyclableRender, components */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return staticRenderFns; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "recyclableRender", function() { return recyclableRender; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "components", function() { return components; });
var components
var render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
}
var recyclableRender = false
var staticRenderFns = []
render._withStripped = true



/***/ }),

/***/ 313:
/*!****************************************************************************************************!*\
  !*** C:/Users/流宇/Desktop/git/uni-appWeb/components/w-picker/w-picker.vue?vue&type=script&lang=js& ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _E_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_12_1_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!./node_modules/babel-loader/lib!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--12-1!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/script.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./w-picker.vue?vue&type=script&lang=js& */ 314);
/* harmony import */ var _E_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_12_1_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_E_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_12_1_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _E_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_12_1_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__) if(__WEBPACK_IMPORT_KEY__ !== 'default') (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _E_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_12_1_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__[key]; }) }(__WEBPACK_IMPORT_KEY__));
 /* harmony default export */ __webpack_exports__["default"] = (_E_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_12_1_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0___default.a); 

/***/ }),

/***/ 314:
/*!***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--12-1!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/script.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!C:/Users/流宇/Desktop/git/uni-appWeb/components/w-picker/w-picker.vue?vue&type=script&lang=js& ***!
  \***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(uni) {Object.defineProperty(exports, "__esModule", { value: true });exports.default = void 0;




































































































































































var _province = _interopRequireDefault(__webpack_require__(/*! ./city-data/province.js */ 315));
var _city = _interopRequireDefault(__webpack_require__(/*! ./city-data/city.js */ 316));
var _area = _interopRequireDefault(__webpack_require__(/*! ./city-data/area.js */ 317));
var _wPicker = _interopRequireDefault(__webpack_require__(/*! ./w-picker.js */ 318));function _interopRequireDefault(obj) {return obj && obj.__esModule ? obj : { default: obj };}function _toConsumableArray(arr) {return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _nonIterableSpread();}function _nonIterableSpread() {throw new TypeError("Invalid attempt to spread non-iterable instance");}function _iterableToArray(iter) {if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === "[object Arguments]") return Array.from(iter);}function _arrayWithoutHoles(arr) {if (Array.isArray(arr)) {for (var i = 0, arr2 = new Array(arr.length); i < arr.length; i++) {arr2[i] = arr[i];}return arr2;}}
function oneOf(value, validList) {
  for (var i = 0; i < validList.length; i++) {
    if (value === validList[i]) {
      return true;
    }
  }
  throw new Error('mode无效，请选择有效的mode!');
  return false;
}var _default2 =
{
  data: function data() {
    return {
      result: [],
      data: {},
      checkArr: [],
      checkValue: [],
      pickVal: [],
      showPicker: false,
      resultStr: "",
      itemHeight: "height: ".concat(uni.upx2px(88), "px;"),
      confirmFlag: true };

  },
  computed: {},


  props: {
    mode: {
      type: String,
      validator: function validator(mode) {
        var modeList = ['half', 'date', 'dateTime', 'yearMonth', 'time', 'region', 'selector', 'limit', 'limitHour', 'range', 'linkage']; //过滤无效mode;
        return oneOf(mode, modeList);
      },
      default: function _default() {
        return "date";
      } },

    themeColor: {
      type: String,
      default: function _default() {
        return "#f5a200";
      } },

    startYear: {
      type: [String, Number],
      default: function _default() {
        return "1970";
      } },

    endYear: {
      type: [String, Number],
      default: function _default() {
        return new Date().getFullYear() + '';
      } },

    defaultVal: {
      type: [Array, String],
      default: "" },

    areaCode: {
      type: Array,
      default: function _default() {
        return null;
      } },

    hideArea: { //隐藏省市区三级联动   地区列
      type: Boolean,
      default: false },

    step: {
      type: [String, Number],
      default: 1 },

    current: {
      type: Boolean,
      default: false },

    selectList: {
      type: Array,
      default: function _default() {
        return [];
      } },

    //以下参数仅对mode==limit有效
    dayStep: {
      type: [String, Number],
      default: 7 },

    startHour: {
      type: [String, Number],
      default: 8 },

    endHour: {
      type: [String, Number],
      default: 20 },

    minuteStep: {
      type: [String, Number],
      default: 10 },

    afterStep: {
      type: [String, Number],
      default: 30 },

    disabledAfter: {
      type: Boolean,
      default: false },

    linkList: {
      type: Array,
      default: function _default() {
        return [];
      } },

    value: {
      type: Array,
      default: function _default() {
        return null;
      } },

    level: {
      type: [Number, String],
      default: 2 },

    timeout: {
      type: Boolean,
      default: false } },


  watch: {
    mode: function mode() {
      this.initData();
    },
    selectList: function selectList() {
      this.initData();
    },
    linkList: function linkList() {
      this.initData();
    },
    defaultVal: function defaultVal(val) {
      this.initData();
      console.log(val);
    },
    areaCode: function areaCode() {
      this.initData();
    },
    value: function value() {
      this.initData();
    } },

  methods: {
    touchStart: function touchStart() {
      if (this.timeout) {
        this.confirmFlag = false;
      }
    },
    touchEnd: function touchEnd() {var _this2 = this;
      if (this.timeout) {
        setTimeout(function () {
          _this2.confirmFlag = true;
        }, 500);
      }
    },
    getLinkageVal: function getLinkageVal(value, flag) {
      var dval = [];
      var list = this.linkList;
      var lev = this.level;
      var arr = value;
      var k = 0;
      var checkArr = [];
      var checkValue = [];
      var resultStr = "";
      var data = [];
      switch (lev) {
        case 2:
          dval = [0, 0];
          break;
        case 3:
          dval = [0, 0, 0];
          break;}

      var getData = function getData(obj, key, str) {
        if (key < lev) {
          data.push(obj);
          if (!arr) {
            var item = obj[0];
            checkArr.push(item.label);
            checkValue.push(item.value);
            resultStr += item.label;
            if (item.children) {
              getData(item.children, key += 1);
            }
          } else {
            obj.map(function (v, j) {
              if (flag ? v.value == arr[key] : v.label == arr[key]) {
                dval[key] = j;
                checkArr.push(v.label);
                checkValue.push(v.value);
                resultStr += v.label;
                if (v.children) {
                  getData(v.children, key += 1);
                }
              }
            });
          }
          return {
            data: data,
            dval: dval,
            checkArr: checkArr,
            checkValue: checkValue,
            resultStr: resultStr };

        } else {
          return false;
        }
      };
      return getData(list, k);
    },
    getRegionVal: function getRegionVal(value, useCode) {
      var province = value[0];
      var city = value[1];
      var a = 0,b = 0,c = 0,dval = [];
      var _this = this;
      _province.default.map(function (v, k) {
        if (useCode ? v.value == province : v.label == province) {
          a = k;
        }
      });
      _city.default[a].map(function (v, k) {
        if (useCode ? v.value == city : v.label == city) {
          b = k;
        }
      });
      if (!_this.hideArea) {
        var area = value[2];
        _area.default[a][b].map(function (v, k) {
          if (useCode ? v.value == area : v.label == area) {
            c = k;
          }
        });
        dval = [a, b, c];
      } else {
        dval = [a, b];
      }
      return dval;
    },
    useCurrent: function useCurrent() {
      var aToday = new Date();
      var tYear = aToday.getFullYear().toString();
      var tMonth = this.formatNum(aToday.getMonth() + 1).toString();
      var tDay = this.formatNum(aToday.getDate()).toString();
      var tHours = this.formatNum(aToday.getHours()).toString();
      var tMinutes = this.formatNum(aToday.getMinutes()).toString();
      var tSeconds = this.formatNum(aToday.getSeconds()).toString();
      if (this.current || !this.defaultVal) {
        switch (this.mode) {
          case "range":
            return [tYear + "-" + tMonth + "-" + tDay, tYear + "-" + tMonth + "-" + tDay];
            break;
          case "date":
            return tYear + "-" + tMonth + "-" + tDay;
            break;
          case "yearMonth":
            return tYear + "-" + tMonth;
            break;
          case "time":
            return tHours + ":" + (Math.floor(tMinutes / this.step) * this.step).toString() + ":" + tSeconds;
            break;
          default:
            return tYear + "-" + tMonth + "-" + tDay + " " + tHours + ":" + (Math.floor(tMinutes / this.step) * this.step).toString() + ":" + tSeconds;
            break;}

      } else {
        return this.defaultVal;
      }
    },
    formatNum: function formatNum(num) {
      return num < 10 ? '0' + num : num + '';
    },
    maskTap: function maskTap() {
      this.$emit("cancel", {
        checkArr: this.checkArr,
        defaultVal: this.pickVal });

      this.showPicker = false;
    },
    show: function show() {
      this.showPicker = true;
    },
    hide: function hide() {
      this.showPicker = false;
    },
    pickerCancel: function pickerCancel() {
      this.$emit("cancel", {
        checkArr: this.checkArr,
        defaultVal: this.pickVal });

      this.showPicker = false;
    },
    pickerConfirm: function pickerConfirm(e) {
      if (!this.confirmFlag) {
        return;
      }
      switch (this.mode) {
        case "range":
          var checkArr = this.checkArr;
          var fDateTime = new Date(checkArr[0], checkArr[1], checkArr[2]);
          var tDateTime = new Date(checkArr[3], checkArr[4], checkArr[5]);
          var dVal = this.pickVal;
          if (fDateTime > tDateTime) {
            this.checkArr = [checkArr[3], checkArr[4], checkArr[5], checkArr[0], checkArr[1], checkArr[2]];
            this.pickVal = [dVal[4], dVal[5], dVal[6], 0, dVal[0], dVal[1], dVal[2]];
            this.$emit("confirm", {
              checkArr: _toConsumableArray(this.checkArr),
              from: checkArr[3] + "-" + checkArr[4] + "-" + checkArr[5],
              to: checkArr[0] + "-" + checkArr[1] + "-" + checkArr[2],
              defaultVal: _toConsumableArray(this.pickVal),
              result: this.resultStr });

          } else {
            this.$emit("confirm", {
              checkArr: _toConsumableArray(this.checkArr),
              from: checkArr[0] + "-" + checkArr[1] + "-" + checkArr[2],
              to: checkArr[3] + "-" + checkArr[4] + "-" + checkArr[5],
              defaultVal: _toConsumableArray(this.pickVal),
              result: this.resultStr });

          }
          break;
        case "limit":
          var aTime = new Date().getTime();
          var bTime = new Date(this.resultStr.replace(/-/g, '/')).getTime();
          if (aTime > bTime) {
            uni.showModal({
              title: "提示",
              content: "选择时间必须大于当前时间",
              confirmColor: this.themeColor });

            return;
          }
          this.$emit("confirm", {
            checkArr: _toConsumableArray(this.checkArr),
            defaultVal: _toConsumableArray(this.pickVal),
            result: this.resultStr });

          break;
        case "region":
        case "linkage":
          this.$emit("confirm", {
            checkArr: _toConsumableArray(this.checkArr),
            checkValue: _toConsumableArray(this.checkValue),
            defaultVal: _toConsumableArray(this.pickVal),
            result: this.resultStr });

          break;
        case "selector":
          this.$emit("confirm", {
            checkArr: this.checkArr,
            defaultVal: _toConsumableArray(this.pickVal),
            result: this.resultStr });

          break;
        default:
          this.$emit("confirm", {
            checkArr: [this.checkArr],
            defaultVal: _toConsumableArray(this.pickVal),
            result: this.resultStr });

          break;}

      this.showPicker = false;
    },
    bindChange: function bindChange(val) {
      var _this = this;
      var arr = val.detail.value;
      var year = "",month = "",day = "",hour = "",minute = "",second = "",note = [],province,city,area;
      var checkArr = _this.checkArr;
      var days = [],months = [],endYears = [],endMonths = [],endDays = [],startDays = [];
      var mode = _this.mode;
      var col1, col2, col3, d, a, h, m;
      var xDate = new Date().getTime();
      switch (mode) {
        case "limitHour":
          col1 = _this.data.date[arr[0]];
          col2 = _this.data.areas[arr[1]];
          col3 = _this.data.hours[arr[2]];
          if (col1.value != checkArr[0].value) {
            arr[1] = 0;
            arr[2] = 0;
            var _areas = _wPicker.default.limitHour.initAreas(col1);
            _this.data.areas = _areas;
            var hours = _wPicker.default.limitHour.initHours(col1, _this.data.areas[arr[1]]);
            _this.data.hours = hours;
          };
          if (col2.value != checkArr[1].value) {
            arr[2] = 0;
            var _hours = _wPicker.default.limitHour.initHours(col1, _this.data.areas[arr[1]]);
            _this.data.hours = _hours;
          };
          d = _this.data.date[arr[0]] || _this.data.date[_this.data.date.length - 1];
          a = _this.data.areas[arr[1]] || _this.data.areas[_this.data.areas.length - 1];
          h = _this.data.hours[arr[2]] || _this.data.hours[_this.data.hours.length - 1];
          _this.checkArr = [d, a, h];
          _this.resultStr = "".concat(d.value + ' ' + a.label + ' ' + h.label + "时");
          break;
        case "limit":
          col1 = _this.data.date[arr[0]];
          col2 = _this.data.hours[arr[1]];
          if (col1.value != checkArr[0].value) {
            var _hours2 = _wPicker.default.limit.initHours(_this.startHour, _this.endHour, _this.minuteStep, _this.afterStep, col1.value);
            var minutes = _wPicker.default.limit.initMinutes(_this.startHour, _this.endHour, _this.minuteStep, _this.afterStep, col1.value, col2.value);
            _this.data.hours = _hours2;
            _this.data.minutes = minutes;
          };
          if (col2.value != checkArr[1].value) {
            var _minutes = _wPicker.default.limit.initMinutes(_this.startHour, _this.endHour, _this.minuteStep, _this.afterStep, col1.value, col2.value);
            _this.data.minutes = _minutes;
          };
          d = _this.data.date[arr[0]] || _this.data.date[_this.data.date.length - 1];
          h = _this.data.hours[arr[1]] || _this.data.hours[_this.data.hours.length - 1];
          m = _this.data.minutes[arr[2]] || _this.data.minutes[_this.data.minutes.length - 1];
          _this.checkArr = [d, h, m];
          _this.resultStr = "".concat(d.value + ' ' + h.value + ':' + m.value + ":" + "00");
          break;
        case "range":
          var fyear = _this.data.fyears[arr[0]] || _this.data.fyears[_this.data.fyears.length - 1];
          var fmonth = _this.data.fmonths[arr[1]] || _this.data.fmonths[_this.data.fmonths.length - 1];
          var fday = _this.data.fdays[arr[2]] || _this.data.fdays[_this.data.fdays.length - 1];
          var tyear = _this.data.tyears[arr[4]] || _this.data.tyears[_this.data.tyears.length - 1];
          var tmonth = _this.data.tmonths[arr[5]] || _this.data.tmonths[_this.data.tmonths.length - 1];
          var tday = _this.data.tdays[arr[6]] || _this.data.tdays[_this.data.tdays.length - 1];
          if (fyear != checkArr[0]) {
            arr[4] = 0;
            arr[5] = 0;
            arr[6] = 0;
            startDays = _wPicker.default.range.initStartDays(fyear, fmonth);
            endYears = _wPicker.default.range.initEndYears(fyear, _this.startYear, _this.endYear);
            endMonths = _wPicker.default.range.initEndMonths(fmonth);
            endDays = _wPicker.default.range.initEndDays(fyear, fmonth, fday, tyear, tmonth);
            _this.data.fdays = startDays;
            _this.data.tyears = endYears;
            _this.data.tmonths = endMonths;
            _this.data.tdays = endDays;
            tyear = _this.data.tyears[0];
            checkArr[3] = _this.data.tyears[0];
            tmonth = _this.data.tmonths[0];
            checkArr[4] = _this.data.tmonths[0];
            tday = _this.data.tdays[0];
            checkArr[5] = _this.data.tdays[0];
          };
          if (fmonth != checkArr[1]) {
            arr[4] = 0;
            arr[5] = 0;
            arr[6] = 0;
            startDays = _wPicker.default.range.initStartDays(fyear, fmonth);
            endYears = _wPicker.default.range.initEndYears(fyear, _this.startYear, _this.endYear);
            endMonths = _wPicker.default.range.initEndMonths(fmonth);
            endDays = _wPicker.default.range.initEndDays(fyear, fmonth, fday, tyear, tmonth);
            _this.data.fdays = startDays;
            _this.data.tyears = endYears;
            _this.data.tmonths = endMonths;
            _this.data.tdays = endDays;
            tyear = _this.data.tyears[0];
            checkArr[3] = _this.data.tyears[0];
            tmonth = _this.data.tmonths[0];
            checkArr[4] = _this.data.tmonths[0];
            tday = _this.data.tdays[0];
            checkArr[5] = _this.data.tdays[0];
          };
          if (fday != checkArr[2]) {
            arr[4] = 0;
            arr[5] = 0;
            arr[6] = 0;
            endYears = _wPicker.default.range.initEndYears(fyear, _this.startYear, _this.endYear);
            endMonths = _wPicker.default.range.initEndMonths(fmonth);
            endDays = _wPicker.default.range.initEndDays(fyear, fmonth, fday, tyear, tmonth);
            _this.data.tyears = endYears;
            _this.data.tmonths = endMonths;
            _this.data.tdays = endDays;
            tyear = _this.data.tyears[0];
            checkArr[3] = _this.data.tyears[0];
            tmonth = _this.data.tmonths[0];
            checkArr[4] = _this.data.tmonths[0];
            tday = _this.data.tdays[0];
            checkArr[5] = _this.data.tdays[0];
          };
          if (tyear != checkArr[3]) {
            arr[5] = 0;
            arr[6] = 0;
            endMonths = _wPicker.default.range.initToMonths(fyear, fmonth, fday, tyear);
            endDays = _wPicker.default.range.initEndDays(fyear, fmonth, fday, tyear, tmonth);
            _this.data.tmonths = endMonths;
            _this.data.tdays = endDays;
            tmonth = _this.data.tmonths[0];
            checkArr[4] = _this.data.tmonths[0];
            tday = _this.data.tdays[0];
            checkArr[5] = _this.data.tdays[0];
          };
          if (tmonth != checkArr[4]) {
            arr[6] = 0;
            endDays = _wPicker.default.range.initToDays(fyear, fmonth, fday, tyear, tmonth);
            _this.data.tdays = endDays;
            tday = _this.data.tdays[0];
            checkArr[5] = _this.data.tdays[0];
          };
          _this.checkArr = [fyear, fmonth, fday, tyear, tmonth, tday];
          _this.resultStr = "".concat(fyear + '-' + fmonth + '-' + fday + '至' + tyear + '-' + tmonth + '-' + tday);
          break;
        case "half":
          year = _this.data.years[arr[0]] || _this.data.years[_this.data.years.length - 1];
          month = _this.data.months[arr[1]] || _this.data.months[_this.data.months.length - 1];
          day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
          area = _this.data.areas[arr[3]] || _this.data.areas[_this.data.areas.length - 1];
          if (year != checkArr[0]) {
            months = _wPicker.default.date.initMonths(year, _this.disabledAfter);
            days = _wPicker.default.date.initDays(year, month, _this.disabledAfter);
            if (_this.disabledAfter) {
              arr[1] = arr[1] > months.length - 1 ? months.length - 1 : arr[1];
              arr[2] = arr[2] > days.length - 1 ? days.length - 1 : arr[2];
              month = _this.data.months[arr[1]] || _this.data.months[_this.data.months.length - 1];
              day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
            }
            _this.data.days = days;
            _this.data.months = months;
          };
          if (month != checkArr[1]) {
            days = _wPicker.default.date.initDays(year, month, _this.disabledAfter);
            arr[2] = arr[2] > days.length - 1 ? days.length - 1 : arr[2];
            day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
            _this.data.days = days;
          };
          _this.checkArr = [year, month, day, area];
          _this.resultStr = "".concat(year + '-' + month + '-' + day + area.label);
          break;
        case "date":
          year = _this.data.years[arr[0]] || _this.data.years[_this.data.years.length - 1];
          month = _this.data.months[arr[1]] || _this.data.months[_this.data.months.length - 1];
          day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
          if (year != checkArr[0]) {
            months = _wPicker.default.date.initMonths(year, _this.disabledAfter);
            days = _wPicker.default.date.initDays(year, month, _this.disabledAfter);
            if (_this.disabledAfter) {
              arr[1] = arr[1] > months.length - 1 ? months.length - 1 : arr[1];
              arr[2] = arr[2] > days.length - 1 ? days.length - 1 : arr[2];
              month = _this.data.months[arr[1]] || _this.data.months[_this.data.months.length - 1];
              day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
            }
            _this.data.days = days;
            _this.data.months = months;
          };
          if (month != checkArr[1]) {
            days = _wPicker.default.date.initDays(year, month, _this.disabledAfter);
            arr[2] = arr[2] > days.length - 1 ? days.length - 1 : arr[2];
            day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
            _this.data.days = days;
          };
          _this.checkArr = [year, month, day];
          _this.resultStr = "".concat(year + '-' + month + '-' + day);
          break;
        case "yearMonth":
          year = _this.data.years[arr[0]] || _this.data.years[_this.data.years.length - 1];
          month = _this.data.months[arr[1]] || _this.data.months[_this.data.months.length - 1];
          if (year != checkArr[0]) {
            if (_this.disabledAfter) {
              arr[1] = arr[1] > months.length - 1 ? months.length - 1 : arr[1];
              month = _this.data.months[arr[1]] || _this.data.months[_this.data.months.length - 1];
            }
            months = _wPicker.default.date.initMonths(year, _this.disabledAfter);
            _this.data.months = months;
          };
          _this.checkArr = [year, month];
          _this.resultStr = "".concat(year + '-' + month);
          break;
        case "dateTime":
          year = _this.data.years[arr[0]] || _this.data.years[_this.data.years.length - 1];
          month = _this.data.months[arr[1]] || _this.data.months[_this.data.months.length - 1];
          day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
          hour = _this.data.hours[arr[3]] || _this.data.hours[_this.data.hours.length - 1];
          minute = _this.data.minutes[arr[4]] || _this.data.minutes[_this.data.minutes.length - 1];
          second = _this.data.seconds[arr[5]] || _this.data.seconds[_this.data.seconds.length - 1];
          if (year != checkArr[0]) {
            arr[2] = 0;
            days = _wPicker.default.date.initDays(year, month);
            day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
            _this.data.days = days;
          };
          if (month != checkArr[1]) {
            arr[2] = 0;
            days = _wPicker.default.date.initDays(year, month);
            day = _this.data.days[arr[2]] || _this.data.days[_this.data.days.length - 1];
            _this.data.days = days;
          };
          _this.checkArr = [year, month, day, hour, minute, second];
          _this.resultStr = "".concat(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second);
          break;
        case "time":
          hour = _this.data.hours[arr[0]] || _this.data.hours[_this.data.hours.length - 1];
          minute = _this.data.minutes[arr[1]] || _this.data.minutes[_this.data.minutes.length - 1];
          second = _this.data.seconds[arr[2]] || _this.data.seconds[_this.data.seconds.length - 1];
          _this.checkArr = [hour, minute, second];
          _this.resultStr = "".concat(hour + ':' + minute + ':' + second);
          break;
        case "linkage":
          var c1, c2, c3;
          var list = this.linkList;
          c1 = _this.data[0][arr[0]] || _this.data[0][0];
          c2 = _this.data[1][arr[1]] || _this.data[1][0];
          if (this.level == 3) {
            c3 = _this.data[2][arr[2]] || _this.data[2][0];
            if (c1.label != checkArr[0]) {
              arr[1] = 0;
              arr[2] = 0;
              _this.data[1] = list[arr[0]].children;
              _this.data[2] = list[arr[0]].children[arr[1]].children;
              c2 = _this.data[1][arr[1]] || _this.data[1][0];
              c3 = _this.data[2][arr[2]] || _this.data[2][0];
            };
            if (c2.label != checkArr[1]) {
              arr[2] = 0;
              _this.data[2] = list[arr[0]].children[arr[1]].children;
              c3 = _this.data[2][arr[2]] || _this.data[2][0];
            };
            _this.checkArr = [c1.label, c2.label, c3.label];
            _this.checkValue = [
            _this.data[0][arr[0]] ? _this.data[0][arr[0]].value : _this.data[0][0].value,
            _this.data[1][arr[1]] ? _this.data[1][arr[1]].value : _this.data[1][0].value,
            _this.data[2][arr[2]] ? _this.data[2][arr[2]].value : _this.data[2][0].value];

            _this.resultStr = c1.label + c2.label + c3.label;
          } else {
            if (c1.label != checkArr[0]) {
              _this.data[1] = list[arr[0]].children;
              arr[1] = 0;
              c2 = _this.data[1][arr[1]] || _this.data[1][0];
            };
            _this.checkArr = [c1.label, c2.label];
            _this.checkValue = [
            _this.data[0][arr[0]] ? _this.data[0][arr[0]].value : _this.data[0][0].value,
            _this.data[1][arr[1]] ? _this.data[1][arr[1]].value : _this.data[1][0].value];

            _this.resultStr = c1.label + c2.label;
          }
          break;
        case "region":
          province = _this.data.provinces[arr[0]] || _this.data.provinces[0];
          city = _this.data.citys[arr[1]] || _this.data.citys[0];
          if (!_this.hideArea) {
            area = _this.data.areas[arr[2]] || _this.data.areas[0];
          }

          if (province.label != checkArr[0]) {
            _this.data.citys = _city.default[arr[0]] || _city.default[0];
            if (!_this.hideArea) {
              _this.data.areas = _area.default[arr[0]][0] || _area.default[0][0];
            }
            arr[1] = 0;
            arr[2] = 0;
            city = _this.data.citys[arr[1]] || _this.data.citys[0];
            if (!_this.hideArea) {
              area = _this.data.areas[arr[2]] || _this.data.areas[0];
            }
          };
          if (city.label != checkArr[1] && !_this.hideArea) {
            _this.data.areas = _area.default[arr[0]][arr[1]] || _area.default[0][0];
            arr[2] = 0;
            area = _this.data.areas[arr[2]] || _this.data.areas[0];
          };
          if (!_this.hideArea) {
            _this.checkArr = [province.label, city.label, area.label];
            _this.checkValue = [
            _this.data.provinces[arr[0]] ? _this.data.provinces[arr[0]].value : _this.data.provinces[0].value,
            _this.data.citys[arr[1]] ? _this.data.citys[arr[1]].value : _this.data.citys[0].value,
            _this.data.areas[arr[2]] ? _this.data.areas[arr[2]].value : _this.data.areas[0].value];

            _this.resultStr = province.label + city.label + area.label;
          } else {
            _this.checkArr = [province.label, city.label];
            _this.checkValue = [
            _this.data.provinces[arr[0]] ? _this.data.provinces[arr[0]].value : _this.data.provinces[0].value,
            _this.data.citys[arr[1]] ? _this.data.citys[arr[1]].value : _this.data.citys[0].value];

            _this.resultStr = province.label + city.label;
          };
          break;
        case "selector":
          _this.checkArr = _this.data[arr[0]] || _this.data[_this.data.length - 1];
          _this.resultStr = _this.data[arr[0]] ? _this.data[arr[0]].label : _this.data[_this.data.length - 1].label;
          break;}

      _this.$nextTick(function () {
        _this.pickVal = arr;
      });
    },
    initData: function initData() {var _this3 = this;
      var _this = this;
      var data = {};
      var mode = _this.mode;
      var year, month, day, hour, minute, second, province, city, area;
      var col1, col2, col3;
      var dVal = [];
      switch (mode) {
        case "linkage":
          var init;
          if (_this.value) {
            init = _this.getLinkageVal(_this.value, true);
          } else {
            init = _this.getLinkageVal(_this.defaultVal);
          }
          dVal = init.dval;
          data = init.data;
          _this.checkArr = init.checkArr;
          _this.checkValue = init.checkValue;
          _this.resultStr = init.resultStr;
          break;
        case "region":
          if (_this.areaCode) {
            dVal = _this.getRegionVal(_this.areaCode, true);
          } else {
            dVal = _this.getRegionVal(_this.defaultVal);
          }
          if (_this.hideArea) {
            data = {
              provinces: _province.default,
              citys: _city.default[dVal[0]] };

          } else {
            data = {
              provinces: _province.default,
              citys: _city.default[dVal[0]],
              areas: _area.default[dVal[0]][dVal[1]] };

          };
          break;
        case "selector":
          var idx = 0;
          data = _toConsumableArray(_this.selectList);
          _this.selectList.map(function (v, k) {
            if (v.label == _this3.defaultVal) {
              idx = k;
            }
          });
          dVal = [idx];
          break;
        case "limit":
          data = _wPicker.default.limit.init(_this.dayStep, _this.startHour, _this.endHour, _this.minuteStep, _this.afterStep, this.defaultVal);
          dVal = data.defaultVal || _this.defaultVal;
          break;
        case "limitHour":
          data = _wPicker.default.limitHour.init(_this.dayStep, this.defaultVal);
          dVal = data.defaultVal || _this.defaultVal;
          break;
        case "range":
          data = _wPicker.default.range.init(_this.startYear, _this.endYear, _this.useCurrent(), _this.current);
          dVal = data.defaultVal || _this.defaultVal;
          break;
        default:
          data = _wPicker.default.date.init(_this.startYear, _this.endYear, _this.mode, _this.step, _this.useCurrent(), _this.current, _this.disabledAfter);
          dVal = data.defaultVal || _this.defaultVal;
          break;}

      _this.data = data;
      switch (mode) {
        case "limitHour":
          col1 = data.date[dVal[0]] || data.date[data.date.length - 1];
          col2 = data.areas[dVal[2]] || data.areas[data.areas.length - 1];
          col3 = data.hours[dVal[1]] || data.hours[data.hours.length - 1];
          _this.checkArr = [col1, col2, col3];
          _this.resultStr = "".concat(col1.value + ' ' + col2.label + ' ' + col3.label + '时');
          break;
        case "limit":
          col1 = data.date[dVal[0]] || data.date[data.date.length - 1];
          col2 = data.hours[dVal[1]] || data.hours[data.hours.length - 1];
          col3 = data.minutes[dVal[2]] || data.minutes[data.minutes.length - 1];
          _this.checkArr = [col1, col2, col3];
          _this.resultStr = "".concat(col1.value + ' ' + col2.value + ':' + col3.value + ":" + "00");
          break;
        case "range":
          var fYear = data.fyears[dVal[0]] || data.fyears[data.fyears.length - 1];
          var fmonth = data.fmonths[dVal[1]] || data.fmonths[data.fmonths.length - 1];
          var fday = data.fdays[dVal[2]] || data.fdays[data.fdays.length - 1];
          var tYear = data.tyears[dVal[4]] || data.tyears[data.tyears.length - 1];
          var tmonth = data.tmonths[dVal[5]] || data.tmonths[data.tmonths.length - 1];
          var tday = data.tdays[dVal[6]] || data.tdays[data.tdays.length - 1];
          _this.checkArr = [fYear, fmonth, fday, tYear, tmonth, tday];
          _this.resultStr = "".concat(fYear + '-' + fmonth + '-' + fday + '至' + tYear + '-' + tmonth + '-' + tday);
          break;
        case "half":
          year = data.years[dVal[0]] || data.years[data.years.length - 1];
          month = data.months[dVal[1]] || data.months[data.months.length - 1];
          day = data.days[dVal[2]] || data.days[data.days.length - 1];
          area = data.areas[dVal[3]] || data.areas[data.areas.length - 1];
          _this.checkArr = [year, month, day, area];
          _this.resultStr = "".concat(year + '-' + month + '-' + day + ' ' + area.label);
          break;
        case "date":
          year = data.years[dVal[0]] || data.years[data.years.length - 1];
          month = data.months[dVal[1]] || data.months[data.months.length - 1];
          day = data.days[dVal[2]] || data.days[data.days.length - 1];
          _this.checkArr = [year, month, day];
          _this.resultStr = "".concat(year + '-' + month + '-' + day);
          break;
        case "yearMonth":
          year = data.years[dVal[0]] || data.years[data.years.length - 1];
          month = data.months[dVal[1]] || data.months[data.months.length - 1];
          _this.checkArr = [year, month];
          _this.resultStr = "".concat(year + '-' + month);
          break;
        case "dateTime":
          year = data.years[dVal[0]] || data.years[data.years.length - 1];
          month = data.months[dVal[1]] || data.months[data.months.length - 1];
          day = data.days[dVal[2]] || data.days[data.days.length - 1];
          hour = data.hours[dVal[3]] || data.hours[data.hours.length - 1];
          minute = data.minutes[dVal[4]] || data.minutes[data.minutes.length - 1];
          second = data.seconds[dVal[5]] || data.seconds[data.seconds.length - 1];
          _this.resultStr = "".concat(year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second);
          _this.checkArr = [year, month, day, hour, minute];
          break;
        case "time":
          hour = data.hours[dVal[0]] || data.hours[data.hours.length - 1];
          minute = data.minutes[dVal[1]] || data.minutes[data.minutes.length - 1];
          second = data.seconds[dVal[2]] || data.seconds[data.seconds.length - 1];
          _this.checkArr = [hour, minute, second];
          _this.resultStr = "".concat(hour + ':' + minute + ':' + second);
          break;
        case "region":
          province = data.provinces[dVal[0]];
          city = data.citys[dVal[1]];
          if (!_this.hideArea) {
            area = data.areas[dVal[2]];
            _this.checkArr = [province.label, city.label, area.label];
            _this.checkValue = [province.value, city.value, area.value];
            _this.resultStr = province.label + city.label + area.label;
          } else {
            _this.checkArr = [province.label, city.label];
            _this.checkValue = [province.value, city.value];
            _this.resultStr = province.label + city.label;
          }
          break;
        case "selector":
          _this.checkArr = data[dVal[0]] || data[data.length - 1];
          _this.resultStr = data[dVal[0]].label || data[data.length - 1].label;
          break;}

      _this.$nextTick(function () {
        _this.pickVal = _toConsumableArray(dVal);
      });
    } },

  mounted: function mounted() {
    this.initData();
  } };exports.default = _default2;
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/index.js */ 1)["default"]))

/***/ }),

/***/ 319:
/*!*************************************************************************************************************!*\
  !*** C:/Users/流宇/Desktop/git/uni-appWeb/components/w-picker/w-picker.vue?vue&type=style&index=0&lang=scss& ***!
  \*************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _E_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_1_E_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_index_js_ref_8_oneOf_1_2_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_E_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_E_HBuilderX_plugins_uniapp_cli_node_modules_sass_loader_lib_loader_js_ref_8_oneOf_1_4_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!./node_modules/mini-css-extract-plugin/dist/loader.js??ref--8-oneOf-1-0!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-1!./node_modules/css-loader??ref--8-oneOf-1-2!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/src??ref--8-oneOf-1-3!./node_modules/sass-loader/lib/loader.js??ref--8-oneOf-1-4!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-5!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./w-picker.vue?vue&type=style&index=0&lang=scss& */ 320);
/* harmony import */ var _E_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_1_E_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_index_js_ref_8_oneOf_1_2_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_E_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_E_HBuilderX_plugins_uniapp_cli_node_modules_sass_loader_lib_loader_js_ref_8_oneOf_1_4_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_E_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_1_E_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_index_js_ref_8_oneOf_1_2_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_E_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_E_HBuilderX_plugins_uniapp_cli_node_modules_sass_loader_lib_loader_js_ref_8_oneOf_1_4_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _E_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_1_E_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_index_js_ref_8_oneOf_1_2_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_E_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_E_HBuilderX_plugins_uniapp_cli_node_modules_sass_loader_lib_loader_js_ref_8_oneOf_1_4_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__) if(__WEBPACK_IMPORT_KEY__ !== 'default') (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _E_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_1_E_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_index_js_ref_8_oneOf_1_2_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_E_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_E_HBuilderX_plugins_uniapp_cli_node_modules_sass_loader_lib_loader_js_ref_8_oneOf_1_4_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__[key]; }) }(__WEBPACK_IMPORT_KEY__));
 /* harmony default export */ __webpack_exports__["default"] = (_E_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_1_E_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_index_js_ref_8_oneOf_1_2_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_E_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_E_HBuilderX_plugins_uniapp_cli_node_modules_sass_loader_lib_loader_js_ref_8_oneOf_1_4_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_E_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_w_picker_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0___default.a); 

/***/ }),

/***/ 320:
/*!*****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js??ref--8-oneOf-1-0!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-1!./node_modules/css-loader??ref--8-oneOf-1-2!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/src??ref--8-oneOf-1-3!./node_modules/sass-loader/lib/loader.js??ref--8-oneOf-1-4!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-5!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!C:/Users/流宇/Desktop/git/uni-appWeb/components/w-picker/w-picker.vue?vue&type=style&index=0&lang=scss& ***!
  \*****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ })

}]);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/components/w-picker/w-picker.js.map
;(global["webpackJsonp"] = global["webpackJsonp"] || []).push([
    'components/w-picker/w-picker-create-component',
    {
        'components/w-picker/w-picker-create-component':(function(module, exports, __webpack_require__){
            __webpack_require__('1')['createComponent'](__webpack_require__(310))
        })
    },
    [['components/w-picker/w-picker-create-component']]
]);
