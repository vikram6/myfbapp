$(document).ready(function() {
	// Make the datetime column sortable
	$.fn.dataTable.moment = function ( format, locale ) {
    var types = $.fn.dataTable.ext.type;
 
		// Add type detection
		types.detect.unshift( function ( d ) {
			return moment( d, format, locale, true ).isValid() ?
				'moment-'+format :
				null;
		} );
 
		// Add sorting method - use an integer for the sorting
		types.order[ 'moment-'+format+'-pre' ] = function ( d ) {
			return moment( d, format, locale, true ).unix();
		};
    };

	$.fn.dataTable.moment('MMM DD YYYY, HH:mm a');

	// Make the table a jquery datatable
    $('.table').DataTable({
	  paging: false,
	  searching: false,
	  order: [],
	  info: false
	});
});