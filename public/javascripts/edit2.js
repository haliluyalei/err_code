setTimeout(function () {
	//获取毫秒 添加到结尾，得到不同的错误结果
	num = Math.random()
	if(num > 0.5)
	{
		document.getElementById("write").innerText = "1234567890十字符而已";
	}
	else
	{
		document.getElementById("write").innerText = "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890百字符而已";		
	}
	var errinfo = "这是一个固定长度的JS报错，应该被归纳在一起";	
  throw Error(errinfo);
}, 1);
