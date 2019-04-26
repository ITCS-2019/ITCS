$(function() {
    $.getScript('/static/js/templates/dev_extreme_grids/certificatesGrid.js');
    $.getScript('/static/js/templates/dev_extreme_grids/certificatesOnReviewGrid.js');

    function printGrid(elemId) {
        let mywindow = window.open('', 'PRINT', 'height=400,width=600');

        mywindow.document.write('<html><head><title>' + document.title  + '</title>');
        mywindow.document.write('</head><body >');
        mywindow.document.write('<h1>' + document.title  + '</h1>');
        mywindow.document.write(document.getElementById(`${elemId}`).innerHTML);
        mywindow.document.write('</body></html>');

        mywindow.document.close();
        mywindow.focus();

        mywindow.print();
        mywindow.close();

        return true;
    }

    function exportGrid() {
        let isSelection = ($(this).attr('data-selection') === 'checked') ? true : false;

        $(this).addClass('dropdown-item--clicked');

        if ((typeof certificatesGrid !== 'undefined')) {
            certificatesGrid.exportToExcel(isSelection);
        }
        if ((typeof certificatesOnReviewGrid !== 'undefined')) {
            certificatesOnReviewGrid.exportToExcel(isSelection);
        }
    }

    $('#print-grid').on('click', function() {
        printGrid($(this).attr('data-grid-id'));
    });
    $('.dropdown-item--export').on('click', exportGrid);
});