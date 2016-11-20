setTimeout(function () {
	//获取毫秒 添加到结尾，得到不同的错误结果
	var myDate = new Date();
	myDate.getMilliseconds();
	var errinfo = "~!@#$%^&*()_+=-[]{};'\|\":,./?><./  ";
	errinfo+="获取毫秒 添加到结尾，得到不同的错误结果 =>"
	errinfo+= myDate.getMilliseconds();
  throw Error(errinfo);
}, 1);
