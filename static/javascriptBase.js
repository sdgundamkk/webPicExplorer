window.addEventListener("load", initPage, false);

function submitResult(){
	 title = document.getElementById("title").innerHTML;
	 data = JSON.stringify({'finish':title});
	 $.ajax({
	    type:'POST',
	    url:'/result',
	    data: data,
	    contentType:'application/json; charset=UTF-8',
	    dataType:'json',
	    error:function(data){
	        console.log(data);
	        window.location.href="/task";
        }
    }); 
}

function getTaskItem () {  
//	var obj_list = document.getElementById("tasklist").getElementsByTagName("li");
    obj_list = [];
	for(i=0;i<obj_list.length;i++){
    	obj_list[i].onclick = function(){
    		data = JSON.stringify({'change':this.innerHTML});
			$.ajax({
			    type:'POST',
			    url:'/task',
			    data: data,
			    contentType:'application/json; charset=UTF-8',
			    dataType:'json',
			    success:function(data){
			        alert(data);
			    }
		    }); 
        	}}
} 

function initPage() { 
    getTaskItem();
}
