	if(!document.getElementsByClassName){
        document.getElementsByClassName = function(className, element){
            var children = (element || document).getElementsByTagName('*');
            var elements = new Array();
            for (var i=0; i<children.length; i++){
                var child = children[i];
                var classNames = child.className.split(' ');
                for (var j=0; j<classNames.length; j++){
                    if (classNames[j] == className){ 
                        elements.push(child);
                        break;
                    }
                }
            } 
            return elements;
        };
    }

/*  获取URl中的参数
* @para url 
* @para key 参数名*/
function getUrlParam(sUrl, sKey) {
    var left= sUrl.indexOf("?") + 1
    var right= sUrl.lastIndexOf("#")
    var parasString 
    if(right==-1){
    	 parasString = sUrl.substring(left)
    }else{
    	 parasString = sUrl.substring(left, right)
    }
    var paras = parasString.split('&');
    var parasjson = {}
    
    for(var i= 0;i<paras.length;i++){
    	 var value=paras[i]
    	 var a = value.split('=');
         parasjson[a[0]] !== undefined ? parasjson[a[0]] = [].concat(parasjson[a[0]], a[1]) : parasjson[a[0]] = a[1];
    }
    /**
    for (key in paras){ 
    	
    }
    paras.forEach(function (value, index, arr) {
        var a = value.split('=');
        parasjson[a[0]] !== undefined ? parasjson[a[0]] = [].concat(parasjson[a[0]], a[1]) : parasjson[a[0]] = a[1];
    });
 	*/
    return  arguments[1] !== void 0 ? (parasjson[arguments[1]] || '') : parasjson;
}
function encodeURIHanZi(url){
	if(new RegExp("℃|[\\u4E00-\\u9FFF]+","g").test(url)){//包含中文，
		var params=getUrlParam(url);
		jQuery.each(params, function(key, value) {  
			if(new RegExp("℃|[\\u4E00-\\u9FFF]+","g").test(value)){
				//alert(key+"="+value +"==="+key+"="+encodeURI(value))
				//var reg = new RegExp(value , "g" )
				//url = url.replace( reg , encodeURI(value) );
				url = url.replace( value , encodeURI(value) );
			}
		});  
	}
	return url;
}
$.dialog.openhanzi=function (url,config){
	url=encodeURIHanZi(url);
	return $.dialog.open(url,config);
};
$(function(){
	if($("#mainForm").length>0){
		var path=$("#mainForm").attr("action")
		$('#mainForm').attr("action", encodeURIHanZi(path));
	}
})
