/**
 * Created by slaven on 05/04/2017.
 */
/* DataTables */
$(document).ready(function(){
    var table = $('#myTable').DataTable(
        {
            responsive : true,
            "order": [],
            "columnDefs": [ {
                "targets": 'no-sort',
                "orderable": true,
                "searchable": true
            } ]
        }
    );
});

(function ($) {
    $(document).ready(function () {
        $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            $(this).parent().siblings().removeClass('open');
            $(this).parent().toggleClass('open');
        });
    });
})(jQuery);