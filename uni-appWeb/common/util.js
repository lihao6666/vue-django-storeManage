function forMatNum(num){
	return num<10?'0'+num:num+'';
}

function initDays(year,month){
	let totalDays=new Date(year,month,0).getDate();
	let dates=[];
	for(let d=1;d<=totalDays;d++){
		dates.push(forMatNum(d));
	};
	return dates;
}
function initPicker(start,end,mode="date",step,value,flag) {
	let aToday=new Date();
	let tYear,tMonth,tDay,tHours,tMinutes,tSeconds,defaultVal=[];
	let initstartDate=new Date(start);
	let endDate=new Date(end);
	if(start>end){
		initstartDate=new Date(end);
		endDate=new Date(start);
	};
	let startYear=initstartDate.getFullYear();
	let startMonth=initstartDate.getMonth()+1;
	let endYear=endDate.getFullYear();
	let years=[],months=[],days=[],hours=[],minutes=[],seconds=[],returnArr=[];
	let curMonth=flag?value[1]*1:(value[1]+1);
	let totalDays=new Date(startYear,curMonth,0).getDate();
	for(let s=startYear;s<=endYear;s++){
		years.push(s+'');
	};
	for(let m=1;m<=12;m++){
		months.push(forMatNum(m));
	};
	for(let d=1;d<=totalDays;d++){
		days.push(forMatNum(d));
	}
	for(let h=0;h<24;h++){
		hours.push(forMatNum(h));
	}
	for(let m=0;m<60;m+=step*1){
		minutes.push(forMatNum(m));
	}
	for(let s=0;s<60;s++){
		seconds.push(forMatNum(s));
	}
	if(flag){
		returnArr=[
			years.indexOf(value[0]),
			months.indexOf(value[1]),
			days.indexOf(value[2]),
			hours.indexOf(value[3]),
			minutes.indexOf(value[4])==-1?0:minutes.indexOf(value[4]),
			seconds.indexOf(value[5])
		]
	};
	switch(mode){
		case "range":
			if(flag){
				defaultVal=[returnArr[0],returnArr[1],returnArr[2],0,returnArr[0],returnArr[1],returnArr[2]];
				return {years,months,days,defaultVal}
			}else{
				return {years,months,days}
			}
			break;
		case "date":
			if(flag){
				defaultVal=[returnArr[0],returnArr[1],returnArr[2]];
				return {years,months,days,defaultVal}
			}else{
				return {years,months,days}
			}
			break;
		case "yearMonth":
			if(flag){
				defaultVal=[returnArr[0],returnArr[1]];
				return {years,months,defaultVal}
			}else{
				return {years,months}
			}
			break;
		case "dateTime":
			if(flag){
				defaultVal=returnArr;
				return {years,months,days,hours,minutes,seconds,defaultVal}
			}else{
				return {years,months,days,hours,minutes,seconds}
			}
			break;
		case "time":
			if(flag){
				defaultVal=[returnArr[3],returnArr[4],returnArr[5]];
				return {hours,minutes,seconds,defaultVal}
			}else{
				return {hours,minutes,seconds}
			}
			break;			
	}
}
export{
	initDays,
	initPicker
}