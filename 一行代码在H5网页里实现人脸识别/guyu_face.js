
var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
function getUserMediaToPhoto(constraints,success,error) {
    if(navigator.mediaDevices.getUserMedia){
        //最新标准API
        navigator.mediaDevices.getUserMedia(constraints).then(success).catch(error);
    }else if (navigator.webkitGetUserMedia) {
        //webkit核心浏览器
        navigator.webkitGetUserMedia(constraints,success,error);
    }else if(navigator.mozGetUserMedia){
        //firefox浏览器
        navigator.mozGetUserMedia(constraints,success,error);
    }else if(navigator.getUserMedia){
        //旧版API
        navigator.getUserMedia(constraints,success,error);
    }
}
//成功回调函数
function success(stream){
    //兼容webkit核心浏览器
    var CompatibleURL = window.URL || window.webkitURL;
    //将视频流转化为video的源
    video.src = CompatibleURL.createObjectURL(stream);
    video.play();//播放视频

}
function error(error) {
    console.log('访问用户媒体失败：',error.name,error.message);
    alert('访问摄像头失败：\n'+error.message+"\n请使用Chrome内核浏览器，如360极速、QQ浏览器等");
}

if(navigator.mediaDevices.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.getUserMedia){
    getUserMediaToPhoto({video:{width:320,height:240}},success,error);
}
else
{
    alert('你的浏览器不支持访问用户媒体设备');
}

function faceDetection()
{
    setTimeout(function () {
        $('.face').remove();
        context.drawImage(video,0,0,320,240);
        var img=canvas.toDataURL('image/jpg');
        try
        {
            $('#video').faceDetection({
                complete: function (faces) {     
                    console.log(faces);                   
                    for (var i = 0; i < faces.length; i++) {
                        $('<div>', {
                            'class':'face',
                            'css': {
                                'position': 'absolute',
                                'left':     faces[i].x * faces[i].scaleX + 'px',
                                'top':      faces[i].y * faces[i].scaleY+90 + 'px',
                                'width':    faces[i].width  * faces[i].scaleX + 'px',
                                'height':   faces[i].height * faces[i].scaleY + 'px'
                            }
                        })
                        .insertAfter(this);
                    }
                },
                error:function (code, message) {
                    console.log('err');
                    alert('Error: ' + message);
                }
            });
        }catch(e){}
        faceDetection();                    
    },100);        

}
