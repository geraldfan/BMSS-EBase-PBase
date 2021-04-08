jQuery(document).ready(function () {
	/*
	
		OFF CANVAS - SIDEBAR TOGGLE
		
	*/
	
	jQuery('[data-toggle="offcanvas"]').click(function () {
    jQuery('.row-offcanvas').toggleClass('active');
  });
	
	/*
	
		MENU DROPDOWN - NEXT LEVEL HOVER
		
	*/
	
	jQuery(".dropdown").hover(function() { 
		jQuery(this).find('.dropdown-menu').first().stop(true, true).fadeIn("fast");
  }, function() { 
		jQuery(this).find('.dropdown-menu').first().stop(true, true).fadeOut("fast");
  });
	
	
	/* WINDOW RESIZE FUNCTION  */
	jQuery( window ).resize(function() {
		
		/*
			ABOVE 980px, Remove Off-Canvas Sidebar
		*/
		if(jQuery( window ).width() >= 980) {
			jQuery('body > div.nus-body-container').removeClass('active');
		}
		
	});

	/* SIDEBAR MENU DROPDOWN FUNCTION  */
	jQuery(".dropdown-toggle-link").click(function($) {
        jQuery(this).find('i').toggleClass("down-arrow");
        jQuery(this).parent().children('ul').toggleClass("open");
    });

	
	
});