var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var bgimage = new Image();
var width = canvas.width;
var height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
var mode='pencil'
var degree_slider = document.getElementById("degree_slider");
var degree_value = document.getElementById("degree_value");
var width_slider = document.getElementById("width_slider");
var width_value = document.getElementById("width_value");
var color=[255,0,0]
var degree=1;
var lineWidth=12;

// bgimage.src = "static/img/meta/input.jpg";
// bgimage.onload=function(){
//     window.ctx.drawImage(bgimage, 0, 0, canvas.width, canvas.height);
// }

function reset(){
    this.ctx.clearRect(0, 0, canvas.width, canvas.height);
    // this.ctx.drawImage(bgimage, 0, 0, bgimage.width, bgimage.height);

}

function mouseDown(e){
    this.draw=true;
    this.ctx = this.getContext("2d");


    var o=this;
    this.offsetX=this.offsetLeft;
    this.offsetY=this.offsetTop;

    while(o.offsetParent){
    	o=o.offsetParent;
    	this.offsetX+=o.offsetLeft;
    	this.offsetY+=o.offsetTop;
    }
    
    this.ctx.beginPath();
    this.ctx.moveTo(e.pageX-this.offsetX,e.pageY-this.offsetY);
    
}

function mouseMove(e){
    if (this.draw){
        if (mode=='pencil'){
            this.ctx.globalCompositeOperation="source-over";
            this.ctx.lineTo(e.pageX-this.offsetX,e.pageY-this.offsetY);
            this.ctx.stroke();
        }else{
            this.ctx.globalCompositeOperation="destination-out";
            this.ctx.lineTo(e.pageX-this.offsetX,e.pageY-this.offsetY);
            this.ctx.stroke();
        }
    
    }
}

function mouseUp(e){
    this.draw=false;
}

function touchStart(e){
    this.draw=true;
    this.ctx=this.getContext("2d");
    this.touch=e.targetTouches[0];


    var o=this;
    this.offsetX=this.offsetLeft;
    this.offsetY=this.offsetTop;

    while(o.offsetParent){
    	o=o.offsetParent;
    	this.offsetX+=o.offsetLeft;
    	this.offsetY+=o.offsetTop;
    }

    this.ctx.beginPath();
    this.ctx.moveTo(this.touch.pageX-this.offsetX,this.touch.pageY-this.offsetY);
    e.preventDefault();
}

function touchMove(e){
    this.touch=e.targetTouches[0];
    if (this.draw){
        if(mode=='pencil'){
            this.ctx.globalCompositeOperation="source-over";    
        }else{
            this.ctx.globalCompositeOperation="destination-out";
        }
        
        this.ctx.lineTo(this.touch.pageX-this.offsetX,this.touch.pageY-this.offsetY);
        this.ctx.stroke();
    }
    e.preventDefault();
}

function touchEnd(e){
    this.draw=false;
    e.preventDefault();
}

function clearPad(){
    var canvas=document.querySelector('#myCanvas');
    var ctx=canvas.getContext("2d");
    ctx.clearRect(0,0,canvas.width,canvas.height);
}


function set_color(r,g,b){    
    this.mode='pencil'
    this.color[0]=r;
    this.color[1]=g;
    this.color[2]=b;
    set_prop();
}

function init(){
    set_prop();
    degree_value.innerHTML = degree_slider.value;

    degree_slider.oninput = function() {
        degree_value.innerHTML = this.value;
        window.degree = this.value;
        set_prop();
        
    };
    
    width_value.innerHTML = width_slider.value;    
    width_slider.oninput = function() {
        width_value.innerHTML = this.value;
        window.lineWidth = this.value;
        set_prop();
    };
    
    pencil()
}
// pencil tool
function pencil(){
    this.mode='pencil'
    
    canvas.addEventListener('mousedown',mouseDown);
    canvas.addEventListener('mousemove',mouseMove);
    canvas.addEventListener('mouseup',mouseUp);

    canvas.addEventListener('touchstart',touchStart);
    canvas.addEventListener('touchmove',touchMove);
    canvas.addEventListener('touchend',touchEnd);
}
        
// eraser tool
        
function eraser(){
    this.mode='eraser'
}  

function save(){
    
    var filename = document.getElementById("fname").value;
    if (filename){
        var image = canvas.toDataURL("image/png");
        var d = { "filename": filename,"save_image":image};

        $.ajax({
            type:"POST",
            url: "/",
            contentType:"application/json",
            
            data:JSON.stringify(d),
            success: function(response) {
                alert(filename + " is completed calculated !!!");
            },
            error: function(xhr) {
                //Do Something to handle error
                console.log("error");
            }
            });
        alert(filename + " saved");
    }
    else{
        alert("Please enter the filename !!!");
    }
    document.getElementById("fname").value = "";
    document.getElementById("download").value = "";
} 
function download(){
        var zipname = document.getElementById("download").value;
        if (zipname){
            window.location.href = '/download/' + zipname
            document.getElementById("download").value = "";
            document.getElementById("fname").value = "";
        }
        else{
            alert("Please enter the download name !!!");
        }
} 
function set_prop(){
    var range=15;
    if (this.color[0]=== 255 && this.color[1]===0 && this.color[2] === 0){
        degree_pixel = (this.color[2]+parseInt(this.degree)*range).toString();
        window.ctx.strokeStyle = 'rgb('+this.color[0]+','+this.color[1]+','+degree_pixel+')';
        window.ctx.fillStyle = 'rgb('+this.color[0]+','+this.color[1]+','+degree_pixel+')';
        color_value.innerHTML = '1';
    }else if(this.color[0]=== 0 && this.color[1]===255 && this.color[2] === 255){
        degree_pixel = (this.color[0]+parseInt(this.degree)*range).toString();
        window.ctx.strokeStyle = 'rgb('+degree_pixel+','+this.color[1]+','+this.color[2]+')';
        window.ctx.fillStyle = 'rgb('+degree_pixel+','+this.color[1]+','+this.color[2]+')';
        color_value.innerHTML = '2';
    }else if(this.color[0]=== 0 && this.color[1]===0 && this.color[2] === 255){
        degree_pixel = (this.color[1]+parseInt(this.degree)*range).toString();
        window.ctx.strokeStyle = 'rgb('+this.color[0]+','+degree_pixel+','+this.color[2]+')';
        window.ctx.fillStyle = 'rgb('+this.color[0]+','+degree_pixel+','+this.color[2]+')';
        color_value.innerHTML = '3';
    }else if(this.color[0]=== 0 && this.color[1]===210 && this.color[2] === 87){
        degree_pixel = (this.color[0]+parseInt(this.degree)*range).toString();
        window.ctx.strokeStyle = 'rgb('+degree_pixel+','+this.color[1]+','+this.color[2]+')';
        window.ctx.fillStyle = 'rgb('+degree_pixel+','+this.color[1]+','+this.color[2]+')';
        color_value.innerHTML = '4';
    }else if(this.color[0]=== 255 && this.color[1]===153 && this.color[2] === 0){
        degree_pixel = (this.color[2]+parseInt(this.degree)*range).toString();
        window.ctx.strokeStyle = 'rgb('+this.color[0]+','+this.color[1]+','+degree_pixel+')';
        window.ctx.fillStyle = 'rgb('+this.color[0]+','+this.color[1]+','+degree_pixel+')';
        color_value.innerHTML = '5';
    }else if(this.color[0]=== 255 && this.color[1]===255 && this.color[2] === 0){
        degree_pixel = (this.color[2]+parseInt(this.degree)*range).toString();
        window.ctx.strokeStyle = 'rgb('+this.color[0]+','+this.color[1]+','+degree_pixel+')';
        window.ctx.fillStyle = 'rgb('+this.color[0]+','+this.color[1]+','+degree_pixel+')';
        color_value.innerHTML = '6';
    }else{
        console.log("else")
    }
    window.ctx.lineWidth = this.lineWidth;
}
