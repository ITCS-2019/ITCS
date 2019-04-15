$(function() {
    function changeExportType() {
           let $btnsContainer = $(this).parent(),
               $btns = $('.btn-export', $btnsContainer);
           $btns.each(function() {
               $(this).removeClass('btn-primary');
               $(this).removeClass('btn-white');
           });
           $(this).addClass('btn-primary');
    }

    $('.btn-export').on('click', changeExportType)
});