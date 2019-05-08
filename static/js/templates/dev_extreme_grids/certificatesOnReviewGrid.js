if ($('#certificates-on-review-grid').length > 0) {
    DevExpress.localization.locale('ru');

    var clickDelay,
        certificatesOnReviewGrid = $('#certificates-on-review-grid').dxDataGrid({
            dataSource: certifications,
            allowColumnReordering: false,
            allowColumnResizing: true,
            columnAutoWidth: false,
            showBorders: true,
            showRowLines: true,
            editing: {
                mode: "cell",
                allowUpdating: true
            },
            onCellPrepared: function (data) {
                if (data.isEditing) {
                    let editInput = data.cellElement.find('input')[0];

                    editInput.setSelectionRange(0, editInput.value.length);
                }
            },
            onRowUpdated: function(options) {
                $.ajax({
                    url: editCellRoute,
                    method: 'GET',
                    data: {
                        certID: options.key.certificateId,
                        certNumber: options.data.certificateNumber
                    },
                    dataType: 'json',
                    success: function (data) {
                    }
                });
            },
            selection: {
                mode: "multiple",
                showCheckBoxesMode: 'always'
            },
            paging: {
                enabled: true,
                pageSize: 10
            },
            pager: {
                showPageSizeSelector: true,
                allowedPageSizes: [10, 20, 50, 100],
                showInfo: true,
                visible: true
            },
            searchPanel: {
                visible: true,
                width: 240,
                placeholder: "Шукати..."
            },
            export: {
                enabled: false,
                fileName: "certificates",
                allowExportSelectedData: true
            },
            customizeExportData: function(cols, rows) {
                let certIDs = [],
                    $clickedItem = $('.dropdown-item--clicked', '#export-type-group'),
                    exportType = $clickedItem.attr('data-type');

                if (rows.length > 0) {
                    let specialty = rows[0].data.specialty,
                        isSameSpecialties = true;

                    rows.some((row) => {
                        if (row.data.specialty === specialty) {
                            certIDs.push(row.data.certificateId);
                        }
                        else {
                            isSameSpecialties = false;
                            return true;
                        }
                    });

                    if (isSameSpecialties) {
                        let element = document.createElement('a');
                        element.setAttribute('href', `${exportRoute}?exportType=${exportType}&certIDs=${certIDs.join(',')}`);
                        element.style.display = 'none';
                        document.body.appendChild(element);
                        element.click();
                        document.body.removeChild(element);
                    }
                    else {
                        $('#modal-text').html('Сертифiкати на вигрузку повиннi мати однаковi напрямки пiдготовки!');
                        $('#error-grid-popup').modal('show');
                    }
                }

                $clickedItem.removeClass('dropdown-item--clicked');
            },
            onFileSaving: function (e) {
                e.cancel = true;
            },
            headerFilter: {
                visible: true
            },
            filterRow: {
                visible: true,
                applyFilter: "auto"
            },
            hoverStateEnabled: true,
            wordWrapEnabled: true,
            columnAutoWidth: true,
            onSelectionChanged: function(e) {
                let selected = (e.component._options.selection.mode === 'multiple') ? `, Вибрано: ${e.component.getSelectedRowKeys().length}` : '';

                e.component.option('pager.infoText', `Всього: ${certifications.length}${selected}`);
            },
            onCellClick: function (e) {
                let component = e.component;

                function initialClick() {
                    component.clickCount = 1;
                    component.clickKey = e.key;
                    component.clickDate = new Date();
                    clickDelay = setTimeout(() => {
                        if (e.column.dataField && e.column.dataField !== 'certificateNumber') {
                            if (e.row.isSelected) {
                                certificatesOnReviewGrid.deselectRows([e.key]);
                            }
                            else {
                                certificatesOnReviewGrid.selectRows([e.key], true);
                            }
                        }
                    }, 300);
                }

                function doubleClick() {
                    clearTimeout(clickDelay);
                    component.clickCount = 0;
                    component.clickKey = 0;
                    component.clickDate = null;
                    switch (e.column.dataField) {
                        // case 'certificateNumber':
                        //     window.location.replace(`/mariner/editCertification/${e.data.certificateId}`);
                        //     return;
                        case 'sailor':
                            window.location.replace(`/mariner/sailor/${e.data.sailorId}`);
                            return;
                        case 'ntz':
                            window.location.replace(`/mariner/trainigOrganisation/${e.data.ntz}`);
                            return;
                    }

                    if (e.column.dataField && e.column.dataField !== 'certificateNumber') {
                        if (e.data) {
                            window.location.replace(`/mariner/editCertification/${e.data.certificateId}`);
                        }
                    }
                }

                if ((!component.clickCount) || (component.clickCount != 1) || (component.clickKey != e.key) ) {
                    initialClick();
                }
                else if (component.clickKey == e.key) {
                    if (((new Date()) - component.clickDate) <= 300) {
                        doubleClick();
                    }
                    else {
                        initialClick();
                    }
                }
            },
            onContentReady: function(e) {
                function changePage(page) {
                    e.component.pageIndex(page);
                }

                let $customPagination = $('.custom-pagination.custom-pagination--certificates'),
                    $select = $('.custom-pagination__select', $customPagination),
                    pageCount = e.component.pageCount(),
                    currentPage = e.component.pageIndex(),
                    $firstPageBtn = $('.custom-pagination__btn--first-page', $customPagination),
                    $lastPageBtn = $('.custom-pagination__btn--last-page', $customPagination),
                    $nextPageBtn = $('.custom-pagination__btn--next', $customPagination),
                    $prevPageBtn = $('.custom-pagination__btn--prev', $customPagination),
                    $gridToolbar = (e.element.find('.dx-toolbar-items-container').length > 0)
                        ? e.element.find('.dx-datagrid-header-panel .dx-toolbar-items-container')
                        : e.element.find('.dx-datagrid-header-panel'),
                    $appendedPagination = $('.custom-pagination.custom-pagination--certificates', $gridToolbar);

                if (pageCount > 1) {
                    $select.empty();
                    for (let i = 0; i < pageCount; i++) {
                        (i === currentPage)
                            ? $select.append(`<option selected="selected" value="${i}">${i + 1}</option>>`)
                            : $select.append(`<option value="${i}">${i + 1}</option>>`);
                    }

                    $appendedPagination.remove();
                    $gridToolbar.append($customPagination);

                    if (currentPage === 0) {
                        $firstPageBtn.attr('disabled', true);
                        $prevPageBtn.attr('disabled', true);
                    }
                    else {
                        $firstPageBtn.attr('disabled', false);
                        $prevPageBtn.attr('disabled', false);
                    }

                    if ((currentPage + 1) === pageCount) {
                        $lastPageBtn.attr('disabled', true);
                        $nextPageBtn.attr('disabled', true);
                    }
                    else {
                        $lastPageBtn.attr('disabled', false);
                        $nextPageBtn.attr('disabled', false);
                    }

                    $select.on('change', function() {changePage($(this).val(), pageCount)});
                    $firstPageBtn.on('click', function() {changePage(0, pageCount)});
                    $lastPageBtn.on('click', function() {changePage(pageCount - 1)});
                    $nextPageBtn.on('click', function() {changePage(currentPage + 1)});
                    $prevPageBtn.on('click', function() {changePage(currentPage - 1)});

                    $customPagination.fadeIn('fast');
                }

                let selected = (e.component._options.selection.mode === 'multiple') ? `, Вибрано: ${e.component.getSelectedRowKeys().length}` : '';

                e.component.option('pager.infoText', `Всього: ${certifications.length}${selected}`);
            },
            columns: [
                {
                    dataField: 'certificateId',
                    visible: false
                },
                {
                    dataField: 'certificateNumber',
                    caption: '№ Сертифіката',
                    allowEditing: true,
                    allowFiltering: true
                },
                {
                    dataField: 'formNumber',
                    caption: '№ Форми',
                    allowEditing: false,
                    allowFiltering: true
                },
                {
                    dataField: 'issueDate',
                    caption: 'Дата видачі',
                    dataType: 'date',
                    allowEditing: false,
                    format: 'dd.MM.yyyy'
                },
                {
                    dataField: 'specialty',
                    caption: 'Напрямок підготовки',
                    allowEditing: false,
                    allowFiltering: true
                },
                {
                    dataField: 'sailorId',
                    visible: false
                },
                {
                    dataField: 'sailor',
                    caption: 'Моряк',
                    allowEditing: false,
                    allowFiltering: true
                },
                {
                    dataField: 'status',
                    caption: 'Статус',
                    allowEditing: false
                }
            ]
        }).dxDataGrid('instance');
}