
function formateDate(datetime,type) {
            var year = datetime.getFullYear(),
                month = ("0" + (datetime.getMonth() + 1)).slice(-2),
                date = ("0" + datetime.getDate()).slice(-2),
                hour = ("0" + datetime.getHours()).slice(-2),
                minute = ("0" + datetime.getMinutes()).slice(-2),
                second = ("0" + datetime.getSeconds()).slice(-2);
            if(type === "Y-M-D h:min:s"){
                var result = year + "-"+ month +"-"+ date +" "+ hour +":"+ minute +":" + second;
            }else if(type === "Y-M-D h:min"){
                var result = year + "-"+ month +"-"+ date +" "+ hour +":"+ minute;
            }else if(type === "Y-M-D"){
                var result = year + "-"+ month +"-"+ date;
            }else if(type === "Y"){
                var result = year;
            }else if(type === "Y-M"){
                var result = year + "-"+ month;
            }else if(type === "M"){
                var result = month;
            }else if(type === "h:min:s"){
                var result = hour +":"+ minute +":" + second;
            }else if(type === "h:min"){
                var result =  hour +":"+ minute;
            }else if(type === "h"){
                var result = hour;
            }else if(type === "min"){
                var result = minute;
            }else if(type === "s"){
                var result =second;
            }
            return result;
}

function formatNumber(value, pattern) {
        if (value == null)
            return value;
        let strarr = value ? value.toString().split('.') : ['0'];
        let fmtarr = pattern ? pattern.split('.') : [''];
        let retstr = '';
        // 整数部分   
        let str = strarr[0];
        let fmt = fmtarr[0];
        let i = str.length - 1;
        let comma = false;
        for (let f = fmt.length - 1; f >= 0; f--) {
            switch (fmt.substr(f, 1)) {
                case '#':
                    if (i >= 0) retstr = str.substr(i--, 1) + retstr;
                    break;
                case '0':
                    if (i >= 0) retstr = str.substr(i--, 1) + retstr;
                    else retstr = '0' + retstr;
                    break;
                case ',':
                    comma = true;
                    retstr = ',' + retstr;
                    break;
            }
        }
        if (i >= 0) {
            if (comma) {
                let l = str.length;
                for (; i >= 0; i--) {
                    retstr = str.substr(i, 1) + retstr;
                    if (i > 0 && ((l - i) % 3) == 0) retstr = ',' + retstr;
                }
            } else retstr = str.substr(0, i + 1) + retstr;
        }
        retstr = retstr + '.';
        // 处理小数部分   
        str = strarr.length > 1 ? strarr[1] : '';
        fmt = fmtarr.length > 1 ? fmtarr[1] : '';
        i = 0;
        for (let f = 0; f < fmt.length; f++) {
            switch (fmt.substr(f, 1)) {
                case '#':
                    if (i < str.length) retstr += str.substr(i++, 1);
                    break;
                case '0':
                    if (i < str.length) retstr += str.substr(i++, 1);
                    else retstr += '0';
                    break;
            }
        }
        return retstr.replace(/^,+/, '').replace(/\.$/, '');
}
//格式化金额
function catformatMoney(value, pattern) {
        if (!value || value == 0)
            return 0;
        let sign = value < 0 ? '-' : '';
        return sign + formatNumber(Math.abs(value), pattern || '#,##0.00');
}
function formatMoneyAuto(value, pattern = '#,##0.00') {
        let unit = "元";
        if (value) {
            let unitNum = {
                // '千': 1000.00,
                '万': 10000.00,
                '千万': 10000000.00,
                '亿': 100000000.00,
                '百亿': 10000000000.00
            };
            let unitCount = {
                // "4": '千',
                "5": '万',
                "8": '千万',
                "9": '亿',
                "11": '百亿'
            };
            let count = 0;
            let money = value;

            while (money >= 1) {
                money = money / 10;
                count++;
            }
            let tmp = unitCount[count + ""];
            while (count >= 4 && tmp === undefined) {
                tmp = unitCount[(--count) + ""];
            }
            unit = tmp === undefined ? unit : tmp;
            value = (count >= 4) ? value / (unitNum[unit]) : value;
        }
        return formatMoney(value, pattern) + unit || "";
}
// 格式化文件大小
function formatFileSize(value) {
        if (null == value || value == '') {
            return "0 Bytes";
        }
        var unitArr = new Array("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB");
        var index = 0;
        var srcsize = parseFloat(value);
        index = Math.floor(Math.log(srcsize) / Math.log(1024));
        var size = srcsize / Math.pow(1024, index);
        size = size.toFixed(2);
        return size + unitArr[index];
}






const emptyPatt = /(^$)|(^[\u4E00-\u9FA5a-zA-Z0-9,，,.,!,@,#,$,%,^,&,*,(,),-,+,/,\\,!,￥,……,*,（,）,~,·,]{1,250}$)/;
const phonePatt = /^1((3[\d])|(4[5,6,9])|(5[0-3,5-9])|(6[5-7])|(7[0-8])|(8[1-8])|(9[1,8,9]))\d{8}$/;
const cardPatt = /(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$)/;
module.exports = {
	formatMoney,
	formateDate,
	catformatMoney,
	formatMoneyAuto,
	formatFileSize,
	phonePatt,
	cardPatt,
}
