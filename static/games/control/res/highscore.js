
function Highscore(new_game){
	var new_game=new_game;
	$("body").append("<div id=highscore style=\"position: absolute; text-align:center;height: 50%; width: 500px; top: 50%; left: 50%;margin-left:-250px;margin-top:-15%;background-color:transparent\"></div>");
	var IMG_URL = './res/images/';
		
	$("#highscore").hide();	
	$("#highscore").append("<table id=htable style=\"color:white;table-layout:fixed;width:500px; text-align:center;margin-left: auto; margin-right: auto; background-color:brown; \"><thead style=\"background-color:black\"><tr><th>AVENTURERO</th><th>BOTIN</th></tr></thead></table>");
	for(i=0;i<10;i++){
		$("#htable").append("<tr><td><p>...</p></td><td><p>...</p></td></tr>");
	}
	$("#htable").append("<tr style=\"background-color:#E49213\"><td colspan= 2><p id=puntos>TUS PUNTOS: </p></td></tr>");
	$("#htable").append("<tr style=\"background-color:red\"><td id=nuevo style=\"cursor:pointer;cursor:hand;\"><p>NUEVO</p></td><td id=\"exit\"><a href= \""+$.games.main_site+"\">SALIR</a></td></tr>");
	$("#nuevo").bind("click",function(){
		$("#highscore").hide();	
		new_game();
	});
	this.showTable = function(puntos){ // Show the Highscores table
		var scores = $.games.get_highscores();
		for ( i=0;i<(scores.length<10?scores.length:10);i++){
				$("#htable td:even:eq("+i+") p").text(scores[i].name)
											.css("background-color","#9B8677");

				$("#htable td:odd:eq("+i+") p").text(scores[i].score+" keV")
											.css("background-color","white")
											.css("color","black");
			}			
		$("#puntos").text("TUS PUNTOS: "+puntos+" keV");
		$("#highscore").slideDown();		
		
	}
	
	this.hideTable = function(){ 
		$("#highscore").hide();	
	}
	
	
}
