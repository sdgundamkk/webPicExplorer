var dragging = false;  
var startTop = 0; 
var startLeft = 0;  
var dragPosY = 0;  
var dragPosX = 0;  
var resultList = [];
var picindex = 0;

window.addEventListener("load", initPage, false);

function trimPX (_px) {  
  if(_px==null || _px=="")  
	return 0;  
  return parseInt(_px.substr(0, _px.lastIndexOf("px")));  
}  

function hitInRect (hitX, hitY, rcLeft, rcTop, rcWidth, rcHeight) {  
  return (hitX>=rcLeft && hitX<rcLeft+rcWidth && hitY>=rcTop && hitY<rcTop+rcHeight);  
}  

function outerDiv () {  
  return document.getElementById("_outerDivA");  
}  

function imageDiv () {  
  return document.getElementById("_imageDivA");  
}  

function imageObj () {  
  return document.getElementById("_imageObjA");  
}  

function imageDivB () {  
  return document.getElementById("_imageDivB");  
}  

function imageObjB () {  
  return document.getElementById("_imageObjB");  
}  

function imageNameA () {  
  return document.getElementById("imageName_A");  
}  

function imageNameB () {  
  return document.getElementById("imageName_B");  
} 

function getTaskItem () {  
	var obj_list = document.getElementById("tasklist").getElementsByTagName("li");
	for(i=0;i<obj_list.length;i++){
    	obj_list[i].onclick = function(){
    		data = JSON.stringify({'change':this.innerHTML});
			$.ajax({
			    type:'POST',
			    url:'/work',
			    data: data,
			    contentType:'application/json; charset=UTF-8',
			    dataType:'json',
			    success:function(data){
			        alert(data);
			    }
		    }); 
        	}}
} 

function MouseWheelHandler(e) {   
    var e = window.event || e; 
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)))
		imageObj().style.width = Math.max(500, Math.min(4000, imageObj().width + (100 * delta))) + "px";
	e.preventDefault();  
    return false;   
}

function MouseWheelHandlerAll(e) {   
    var e = window.event || e; 
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)))
		imageObj().style.width = Math.max(500, Math.min(4000, imageObj().width + (100 * delta))) + "px";
	e.preventDefault();  
    return false;   
}

function MouseWheelHandlerB(e) {   
    var e = window.event || e; 
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)))
		imageObjB().style.width = Math.max(500, Math.min(4000, imageObjB().width + (100 * delta))) + "px";
	e.preventDefault();   
    return false;   
}

function getpicName(){
	imageNameA().innerHTML  = imageObj().src.split('/').slice(-1)[0];
	imageNameB().innerHTML  = imageObjB().src.split('/').slice(-1)[0];
}


function getLastpic(){
    var tempList = [];
	var js_data = document.getElementById('dataid').getAttribute('d').split(',');
	var input = document.getElementsByTagName('input');
	tempList.push(js_data[picindex].slice(2,-1).split('/').pop());
   	for (var i=0;i<input.length;i++)
	{
		if (input[i].checked) {
			tempList.push(input[i].value);
		}
	}
	
	picindex -= 1;
	if(picindex < 0){
		picindex = 0;
		alert('这是第一组！');
		return;
	}
	src = js_data[picindex].slice(2,-1);
	if (src.slice(-1) == "'"){
		src = src.slice(0,-1);
	}
	imageObj().src = src;
	imageObjB().src = src;
	getpicName();
	
	data = JSON.stringify({'dates':tempList});
	$.ajax({
	    type:'POST',
	    url:'/work',
	    data: data,
	    contentType:'application/json; charset=UTF-8',
	    dataType:'json',
	    success:function(data){
	        alert(data);
	    }
    }); 
}

function getNextpic(){
    var tempList = [];
	var js_data = document.getElementById('dataid').getAttribute('d').split(',');
	var input = document.getElementsByTagName('input');
	console.log(picindex);
	tempList.push(js_data[picindex].slice(2,-1).split('/').pop());
   	for (var i=0;i<input.length;i++)
	{
		if (input[i].checked) {
			if (input[i].value == '左边'){result = 1;}
			else if (input[i].value == '右边'){result = 2;}
			else {result = 0;}
			tempList.push(result);
		}
	}
	
	data = JSON.stringify({'dates':tempList});
	$.ajax({
	    type:'POST',
	    url:'/work',
	    data: data,
	    contentType:'application/json; charset=UTF-8',
	    dataType:'json',
	    success:function(data){
	        alert(data);
	    }
    }); 
	
	picindex += 1;
	if(picindex >= js_data.length){
		picindex -= 1;
		window.location.href="/result";
		return;
	}
	console.log(picindex);
	src = js_data[picindex].slice(2,-1);
	if (src.slice(-1) == "'"){
		src = src.slice(0,-1);
	}
	imageObj().src = src;
	imageObjB().src = src;
	getpicName();
	
	
}

function initPage() { 
	outerDiv().addEventListener("mousedown", 
		function (event) { 
			startTop   = trimPX(imageDiv().style.top);  
			startLeft  = trimPX(imageDiv().style.left);  
			var width  = trimPX(imageDiv().style.width);  
			var height = trimPX(imageDiv().style.height);  

			if (hitInRect(event.clientX, event.clientY, startLeft, startTop, width, height)) {  
			dragging = true;  
			dragPosX = event.clientX;  
			dragPosY = event.clientY;  
			event.preventDefault(); 
		  }  
		},  
		false  
	);  

	outerDiv().addEventListener("mousemove",
		function (event) {  
		  if (dragging){  
			imageDiv().style.cursor="pointer"; 
			imageDiv().style.top = "0px";  
			var dx = parseInt(startLeft)+(event.clientX - dragPosX);  
			if(dx < -800){  
				dx = -300;  
			}else if(dx > 800){ 
				dx = 300;  
			}  
			imageDiv().style.left = dx + "px";
			
			var dy = parseInt(startTop)+(event.clientY - dragPosY);  
			if(dy < -800){  
				dy = -300;  
			}else if(dy > 800){  
				dy = 300;  
			}  
			imageDiv().style.top = dy + "px";
		  }  
		  event.preventDefault();  
		},  
		false  
	);  

	outerDiv().addEventListener("mouseup", 
		function (event) {  
		  dragging = false;  
		  imageDiv().style.cursor="default";            
		  event.preventDefault();
		},  
		false  
	);  

    imageDiv().addEventListener("mousewheel", MouseWheelHandler, false); 
    imageDivB().addEventListener("mousewheel", MouseWheelHandlerB, false); 
    getTaskItem();
    getpicName();
}
