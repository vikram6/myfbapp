$(document).ready(function() {
	$('#submitButton').click(function(){
		if (!$.trim($('#postContents').val())) {
			$('#postIsEmpty').show();
			return false;
		}
		else {
			$('#postIsEmpty').hide();
		}
	});
	
	$('#postContents').bind('input propertychange', function() {
		console.log(1);
		if (this.value) {
			$('#postIsEmpty').hide();
		}
	});
});