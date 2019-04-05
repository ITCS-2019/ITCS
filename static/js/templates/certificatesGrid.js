$(function() {
    function getCertificates() {
        $.get('mariner/api/allCerts/', function(data, status) {
            console.log('data---------------------');
            console.log(data);
            console.log('data---------------------');
        });
    }

    if ($('#certificates-grid').length > 0) {
        let certificates = [
            {
                certificateNumber: '122',
                blankNumber: '321',
                issueDate: '12-01-2019',
                specialty: 'Штурман',
                sailor: 'Рогов Василий Петрович',
                ntz: 'Вектор 21',
                status: 'Выдан'
            },
            {
                certificateNumber: '122',
                blankNumber: '321',
                issueDate: '12-01-2019',
                specialty: 'Штурман',
                sailor: 'Рогов Василий Петрович',
                ntz: 'Вектор 21',
                status: 'Чернетка'
            },
        ];

        let certificatesGrid = $('#certificates-grid').dxDataGrid({
            dataSource: certificates,
            allowColumnReordering: false,
            allowColumnResizing: true,
            columnAutoWidth: false,
            showBorders: true,
            showRowLines: true,
            editing: {
                mode: "cell",
                allowUpdating: true
            },
            selection: {
                mode: "multiple"
            },
            paging: {
                enabled: true,
                pageSize: 10
            },
            pager: {
                showPageSizeSelector: true,
                allowedPageSizes: [10, 20, 50, 100],
                showInfo: false
            },
            searchPanel: {
                visible: true,
                width: 240,
                placeholder: "Шукати..."
            },
            export: {
                enabled: true,
                fileName: "ntz",
                allowExportSelectedData: true
            },
            headerFilter: {
                visible: true
            },
            filterRow: {
                visible: true,
                applyFilter: "auto"
            },
            onRowClick: function (e) {
                let component = e.component;

                function initialClick() {
                    component.clickCount = 1;
                    component.clickKey = e.key;
                    component.clickDate = new Date();
                }

                function doubleClick() {
                    console.log('second click');
                    component.clickCount = 0;
                    component.clickKey = 0;
                    component.clickDate = null;
                }

                if ((!component.clickCount) || (component.clickCount != 1) || (component.clickKey != e.key) ) {
                    initialClick();
                }
                else if (component.clickKey == e.key) {
                    if (((new Date()) - component.clickDate) <= 300)
                        doubleClick();
                    else
                        initialClick();
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
                        ? e.element.find('.dx-toolbar-items-container')
                        : e.element.find('.dx-datagrid-header-panel');

                if (pageCount > 1) {
                    $select.empty();
                    for (let i = 0; i < pageCount; i++) {
                        (i === currentPage)
                            ? $select.append(`<option selected="selected" value="${i}">${i + 1}</option>>`)
                            : $select.append(`<option value="${i}">${i + 1}</option>>`);
                    }

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
            },
            columns: [
                {
                    dataField: 'certificateNumber',
                    caption: '№ Сертифіката',
                    width: 100,
                    allowEditing: true,
                    allowFiltering: false
                },
                {
                    dataField: 'blankNumber',
                    caption: '№ Бланку',
                    // width: 200,
                    allowEditing: false,
                    allowFiltering: false
                },
                {
                    dataField: 'issueDate',
                    caption: 'Дата видачі',
                    dataType: 'date',
                    // width: 200,
                    allowEditing: false,
                    allowFiltering: true
                },
                {
                    dataField: 'specialty',
                    caption: 'Напрямок підготовки',
                    // width: 200,
                    allowEditing: false,
                    allowFiltering: true
                },
                {
                    dataField: 'sailor',
                    caption: 'Моряк',
                    // width: 200,
                    allowEditing: false,
                    allowFiltering: true
                },
                {
                    dataField: 'ntz',
                    caption: 'НТЗ',
                    // width: 200,
                    allowEditing: false,
                    allowFiltering: false
                },
                {
                    dataField: 'status',
                    caption: 'Статус',
                    // width: 200,
                    allowEditing: false
                }
            ]
        }).dxDataGrid('instance');
    }
});