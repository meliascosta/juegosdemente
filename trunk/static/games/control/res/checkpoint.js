
function Checkpoint(trials,on_end,on_check){
	
	$("body").append("<div id=check-holder style=\"position: absolute; height: "+80/1024*screen.width+"px; width: 98%; top: 0%; left: 0%;background-color:#2E81FF\"></div>");
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
		
	$("body").append("<div id=text class=messages style=\"position: absolute; height: 20%; width:100%; top: 50%; left: 0%;color: red;font-size:28px;text-align:center\"><p>PEPE</p></div>")
	$("#text").hide();
	
	for(i=0;i<N;i++){
		$($chdiv).append("<div id=checkpoint"+ i +" class=checkpoint style=\"position: absolute; height: 100%; width:"+80/1024*screen.width+"px; top: 0%; left: "+Math.round(trials[i]*((1-80/1024)*100/ntrials))+"%;background-color: white\"></div>");
	}
	$($chdiv).append("<div id=slider style=\"position: absolute; height: 100%; width: "+80/1024*screen.width+"px; top: 0%; left: 0px;background-color: grey\"></div>");
	for(i=0;i<=N;i++){
	$("#slider").append("<img id=\"checkimg"+i+"\" src=\""+IMG_URL+(i+1)+".png\" style=\"left:2px; top:5px; \" height="+69/1024*screen.width+" width= "+75/1024*screen.width+">")		
	}

	$("#slider > img").not("#checkimg0").hide();
	
	$($chdiv).append("<div id=moving-bar style=\"position: absolute; height: 20%; width: 0%; top: 80%; left: 0%;background-color: red; \"></div>");
	var $mv = $("#moving-bar"),
		$sl = $("#slider"),
	    $sl_imgs = $("#slider > img");
		
	this.step = function(){ // advance bar one unit if it reaches a checkpoint change image and slide it.
		curr_trial++;
		$($mv).animate({width: Math.round(curr_trial/ntrials*((1-80/1024)*100)) +"%"}, 500 );
		
		if (curr_trial== trials[0]){
			curr_checkpoint++;
			fallback = parseInt(trials.splice(0,1));
			$($sl_imgs).not("#checkimg"+(curr_checkpoint-1)).hide();
			$("#checkimg"+(curr_checkpoint-1)).show();
			setTimeout(function(){$($sl).animate({left: Math.round(curr_trial/ntrials*((1-80/1024)*100)) +"%"},500,function(){if (trials.length == 0){ on_end();}else{on_check();}})},500);
		}
	}
	this.fallback = function(){ //fallback to last checkpoint
		$($mv).animate({width: Math.round(fallback/ntrials*((1-80/1024)*100))+"%"}, 500 );
		curr_trial = fallback;	
	}
	this.set_at = function(checkN){ // set everything to be at checkpoint number checkN
		trials = TRIALS.slice(0);
		if (checkN>0){temp = trials[checkN-1]; trials.splice(0,checkN);}else{temp=0}
		$($mv).css("width", Math.round(temp/ntrials*((1-80/1024)*100))+"%");
		$($sl_imgs).not("#checkimg"+checkN).hide();
		$("#checkimg"+(checkN)).show();
		$($sl).css("left", Math.round(temp/ntrials*((1-80/1024)*100)) + "%");
		curr_trial = temp;
		fallback = temp;
		curr_checkpoint = checkN+1;
	}
	this.displaytext = function(text){
		$("#text > p").text(text);
		$("#text").show();
		setTimeout(function(){$("#text").fadeOut('fast')},3000);
	}
	
}
