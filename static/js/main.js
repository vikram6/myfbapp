$(document).ready(function() {
    // Make the current tab in the navbar active
    $('li.active').removeClass('active');
	$('a[href="' + location.pathname + '"]').closest('li').addClass('active');
});