$(function(){
	alignCenter();
	$(".top-nav ul li").click(function(){
		$(this).addClass("cur").siblings().removeClass("cur");
	});
	$(".tb-con table tr:even").css("background","#f3f3f3");
	$(".tb-con1 table tr:even").css("background","#f3f3f3");
	$(".tb-con2 table tr:even").css("background","#f3f3f3");
	$(".tb-con3 table tr:even").css("background","#f3f3f3");
	var w=$(window).width();
	var	lm=w/2-298;
	var	lm2=w/2-420;
	$(".banner .tit").css("left",lm);
	$(".tit2").css("left",lm2);
	var userAgent = navigator.userAgent.toLowerCase(); 
	// Figure out what browser is being used 
	jQuery.browser = { 
	version: (userAgent.match( /.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/ ) || [])[1], 
	safari: /webkit/.test( userAgent ), 
	opera: /opera/.test( userAgent ), 
	msie: /msie/.test( userAgent ) && !/opera/.test( userAgent ), 
	mozilla: /mozilla/.test( userAgent ) && !/(compatible|webkit)/.test( userAgent ) 
	}; 
	if($.browser.msie&&($.browser.version == "8.0")){ 
		$(".content-search select,.content-search input").offset({top:400});
	} 
	$(window).resize(function() {
		alignCenter();
	});
});
function alignCenter(){
	var w1=$("#disclosure-title").width()/2;
	var	w2=$("#disclosure-title").parent().width()/2;
	var	w3=w2-w1;
	$("#disclosure-title").css("left",w3);
}