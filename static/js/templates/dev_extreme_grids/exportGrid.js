$(function() {
    function changeExportType() {
           let $btnsContainer = $(this).parent(),
               $btns = $('.btn-export', $btnsContainer);
           $btns.each(function() {
               $(this).removeClass('btn-primary');
               $(this).addClass('btn-white');
           });
           $(this).addClass('btn-primary');
           $(this).removeClass('btn-white');
    }

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

    $('.btn-export').on('click', changeExportType);
    $('#print-grid').on('click', function() {
        printGrid($(this).attr('data-grid-id'));
    });
});