
function get_high_scores(ranking_url){
	var ret;
		$.ajax({
			  type: "GET",
			  url: ranking_url,
			  dataType: "json",
			  async: false,
			  error: function(err,errtype){
					console.log(errtype);
					alert("No highscore");
				},
				success: function(json){
					ret = json;
				}
			});
	return ret;
}

function Highscore(url){
	var url  =url;
	$("body").append("<div id=highscore style=\"position: fixed; text-align:center;height: 50%; width: 500px; top: 50%; left: 50%;margin-left:-250px;margin-top:-15%;background-color:transparent\"></div>");
	var IMG_URL = './res/images/';
		
	$("#highscore").hide();	
	$("#highscore").append("<table id=htable style=\"color:white;table-layout:fixed;width:500px; text-align:center;margin-left: auto; margin-right: auto; background-color:brown; \"><thead style=\"background-color:black\"><tr><th>AVENTURERO</th><th>BOTIN</th></tr></thead></table>");
	for(i=0;i<10;i++){
		$("#htable").append("<tr><td><p style=\"padding:0;margin:0;\">...</p></td><td><p style=\"padding:0;margin:0;\">...</p></td></tr>");
	}
	$("#htable").append("<tr style=\"background-color:red\"><td id=seguir style=\"cursor:pointer;cursor:hand;\"><p style=\"padding:0;margin:0;\" ></p></td><td id=\"exit\"><p style=\"padding:0;margin:0;cursor:pointer;cursor:hand\" >OCULTAR</p></td></tr>");
	$("#exit").click(function(){$("#highscore").hide();	})
	this.showTable = function(ranking_url){ // Show the Highscores table
		var scores = get_high_scores(ranking_url);
		for ( i=0;i<scores.length;i++){
				$("#htable td:even:eq("+i+") p").text(scores[i].name)
											.css("background-color","#9B8677");

				$("#htable td:odd:eq("+i+") p").text(scores[i].score+" keV")
											.css("background-color","white")
											.css("color","black");
			}			
		$("#highscore").fadeIn();		
		
	}
	
	this.hideTable = function(){ 
		$("#highscore").hide();	
	}
	
	
}

