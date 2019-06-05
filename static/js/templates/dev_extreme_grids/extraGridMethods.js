'use strict';
$(function() {
    function handleCerts(grid) {
        let dxGrid = grid.dxDataGrid('instance'),
            selectedRows = dxGrid.getSelectedRowsData(),
            $modalText = $('.modal-text', '#error-grid-popup'),
            $modalDialogText = $('.modal-text', '#dialog-grid-popup');

        if (selectedRows.length > 0) {
            let isInvalidData = false,
                sendRows = [];
            selectedRows.some((row) => {
                if (row.status !== 'Чернетка') {
                    isInvalidData = true;
                    return true;
                }
                else {
                    sendRows.push(row.certificateId);
                }
            });

            if (!isInvalidData) {
                $modalDialogText.html('Вiдправити в обробку обранi сертифiкати?');

                $('#dialog-grid-popup').modal('show');
                $('#dialog-grid-popup').on('shown.bs.modal', function (e) {
                    $('.btn-accept', $(this)).on('click', function() {
                        $.ajax({
                            url: certOnHandle,
                            method: 'GET',
                            data: {
                                certIDs: sendRows.join(',')
                            },
                            dataType: 'json',
                            success: function (data) {
                                if (!data.error) {
                                    window.location.reload();
                                } else {
                                    $modalText.html(data.error_message);
                                    $('#error-grid-popup').modal('show');
                                }
                            }
                        });
                    });
                });
            }
            else {
                $modalText.html('Змiнити статус на "Обробка" можливо тiльки для сертифiкатiв зi статусом "Чернетка"!');
                $('#error-grid-popup').modal('show');
            }
        }
        else {
            $modalText.html('Не вибрано жодного сертифiката!');
            $('#error-grid-popup').modal('show');
        }
    }

    function removeCerts(grid) {
        let dxGrid = grid.dxDataGrid('instance'),
            selectedRows = dxGrid.getSelectedRowsData(),
            $modalErrorText = $('.modal-text', '#error-grid-popup'),
            $modalDialogText = $('.modal-text', '#dialog-grid-popup');

        if (selectedRows.length > 0) {
            let isInvalidData = false,
                sendRows = [];
            selectedRows.some((row) => {
                if (row.status !== 'Чернетка') {
                    isInvalidData = true;
                    return true;
                }
                else {
                    sendRows.push(row.certificateId);
                }
            });

            if (!isInvalidData) {
                $modalDialogText.html('Видалити обранi сертифiкати?');

                $('#dialog-grid-popup').modal('show');
                $('#dialog-grid-popup').on('shown.bs.modal', function (e) {
                    $('.btn-accept', $(this)).on('click', function() {
                        $.ajax({
                            url: certRemove,
                            method: 'GET',
                            data: {
                                certIDs: sendRows.join(',')
                            },
                            dataType: 'json',
                            success: function (data) {
                                if (!data.error) {
                                    window.location.reload();
                                }
                                else {
                                    $modalText.html(data.error_message);
                                    $('#error-grid-popup').modal('show');
                                }
                            }
                        });
                    })
                })
            }
            else {
                $modalErrorText.html('Можливо видаляти тiльки сертифiкати зi статусом "Чернетка"!');
                $('#error-grid-popup').modal('show');
            }
        }
        else {
            $modalErrorText.html('Не вибрано жодного сертифiката!');
            $('#error-grid-popup').modal('show');
        }
    }

    $('#handle-cert').on('click', function() {
        let grid = $('.c-dx-grid', $(this).closest('.ibox-content'));

        handleCerts(grid);
    });
    $('#remove-cert').on('click', function() {
        let grid = $('.c-dx-grid', $(this).closest('.ibox-content'));

        removeCerts(grid);
    });
});