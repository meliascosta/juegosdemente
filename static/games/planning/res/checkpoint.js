
function Checkpoint(trials,on_end,on_check){
	$("body").css({
		"text-align": 'center',
		"margin": '0 auto'
	})
	$("body").append("<div id=check-holder style=\"position: absolute; height: 3em; width: 98%; top: 1%; left: 0%;background-color:#2E81FF;-moz-border-radius:5px;-webkit-border-radius:5px;\"></div>");
	var IMG_URL = './res/images/checkpoints/',
		$chdiv = $("#check-holder"),
		trials = trials,
		TRIALS = trials.slice(0),
		on_end = on_end,
		on_check = on_check;
		N = trials.length,
		ntrials = trials[N-1],
		curr_trial = 0,
		curr_checkpoint = 1,
		fallback = 0;
		
	$("body").append("<div id=text class=messages style=\"position: absolute;left:20%; width:60%;bottom:0; color: #C79EE1;font-weight:bold;font-size:2em;text-align:center;border:solid;-moz-border-radius:10px;-webkit-border-radius:10px;background-color:#481369;\"><p>PEPE</p></div>")
	$("#text").hide();
	
	for(i=0;i<N;i++){
		$($chdiv).append("<div id=checkpoint"+ i +" class=checkpoint style=\"position: absolute; height: 100%; width: 5%; top: 0%; left: "+Math.round(trials[i]*93/ntrials)+"%;background-color: white\"></div>");
	}
	$($chdiv).append("<div id=slider style=\"position: absolute; height: 100%; width: 5%; top: 0%; left: 0px;background-color: grey;\"></div>");
	for(i=0;i<=N;i++){
	$("#slider").append("<img id=\"checkimg"+i+"\" src=\""+IMG_URL+(i+1)+".png\" style=\" width:100%;height:100% \">")		
	}

	$("#slider > img").not("#checkimg0").hide();
	
	$($chdiv).append("<div id=moving-bar style=\"position: absolute; height: 100%; width: 0%; top: 0%; left: 0%;background-color: red;opacity:0.5; \"></div>");
	var $mv = $("#moving-bar"),
		$sl = $("#slider"),
	    $sl_imgs = $("#slider > img");
		
	this.step = function(){ // advance bar one unit if it reaches a checkpoint change image and slide it.
		curr_trial++;
		$($mv).animate({width: Math.round(curr_trial/ntrials*93) +"%"}, 500 );
		
		if (curr_trial== trials[0]){
			curr_checkpoint++;
			fallback = parseInt(trials.splice(0,1));
			$($sl_imgs).not("#checkimg"+(curr_checkpoint-1)).hide();
			$("#checkimg"+(curr_checkpoint-1)).show();
			setTimeout(function(){$($sl).animate({left: Math.round(curr_trial/ntrials*93) +"%"},500,function(){if (trials.length == 0){ on_end();}else{on_check();}})},500);
		}
	}
	this.fallback = function(){ //fallback to last checkpoint
		$($mv).animate({width: Math.round(fallback/ntrials*93)+"%"}, 500 );
		curr_trial = fallback;	
	}
	this.set_at = function(checkN){ // set everything to be at checkpoint number checkN
		trials = TRIALS.slice(0);
		if (checkN>0){temp = trials[checkN-1]; trials.splice(0,checkN);}else{temp=0}
		$($mv).css("width", Math.round(temp/ntrials*93)+"%");
		$($sl_imgs).not("#checkimg"+checkN).hide();
		$("#checkimg"+(checkN)).show();
		$($sl).css("left", Math.round(temp/ntrials*93)+ "%");
		curr_trial = temp;
		fallback = temp;
		curr_checkpoint = checkN+1;
	}
	this.displaytext = function(text){
		$("#text > p").text(text);
		$("#text").slideDown();
		setTimeout(function(){$("#text").fadeOut('fast')},3000);
	}
	
}
