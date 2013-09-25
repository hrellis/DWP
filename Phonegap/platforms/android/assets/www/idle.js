$(document).ready(function() {
			
			if(localStorage.appTime == null)
				{
					var appCounter = 0;
				}
			var idlecounter = 0;

			var idleInterval = setInterval("incrementIdleCounter()", 1000);
			
			$(this).mousemove(function(e) {
				
				idlecounter = 0;
			})
			$(this).keypress(function(e) {
				
				idlecounter = 0;
			});

		}); 

		function incrementIdleCounter()
		{
			idlecounter = idlecounter + 1;
			if(idlecounter < 600)
				{
				appCounter = appCounter + 1;
				console.log(appCounter);
				}
		}
