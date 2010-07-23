

var $flashFile = './res/movies/memoria_bien_1.swf'; 

var $flashString= "<div style = \"background-color: #AAA; position: absolute; visibility: hidden; width:160px; height:200px; top:50%; padding:10px; -moz-border-radius:  5px;-webkit-border-radius: 5px; left:50%; margin-left:-80px; margin-top:-100px; \"id=\"video-player\"> <object classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\" codebase=\"http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0\" id=\"flashp\" width=\"160px\"height=\"200px\"><param name=\"movie\" value=\""+ $flashFile +"\"><param name=\"quality\" value=\"high\"> <param name=\"play\" value=\"false\" /> <embed id=\"flashpe\" src=\""+$flashFile+"\" quality=\"high\" pluginspage=\"http://www.macromedia.com/go/getflashplayer\" play = \"false\" loop= \"false\" type=\"application/x-shockwave-flash\" width=\"160px\" height=\"200px\"></embed> </object> <div>";  //una forma medio desprolija de agregar codigo.

function videoPlayer(){
		
	$("body").append($flashString)

	this.play = function () {
		$("#video-player").css('visibility','visible');
		document.getElementById('flashpe').Play();
		setTimeout(function(){$("#video-player").css('visibility','hidden')},5500);
	}
	
}
