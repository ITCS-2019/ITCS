$(function() {
    if ($('#training-organisations-main-grid').length > 0) {
        DevExpress.localization.locale('ru');

        let trainingOrganisationsMainGrid = $('#training-organisations-main-grid').dxDataGrid({
                dataSource: trainigOrganisations,
                allowColumnReordering: false,
                allowColumnResizing: true,
                columnAutoWidth: false,
                showBorders: true,
                showRowLines: true,
                selection: {
                    mode: (isInspector) ? false : 'multiple',
                    showCheckBoxesMode: 'always'
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
                    enabled: false,
                    fileName: "certificates",
                    allowExportSelectedData: true
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
                grouping: {
                    autoExpandAll: false,
                    expandMode: 'buttonClick'
                },
                onCellClick: function (e) {
                    if (e.column.dataField && !isInspector) {
                        window.location.replace(`/mariner/trainigOrganisation/${e.data.organisation_name}`);
                    }
                    // else if (isInspector && e.column.dataField && e.column.dataField !== 'organisation_name') {
                    else if (isInspector
                    && e.column.dataField
                    && e.column.dataField === 'organisation_name'
                    && typeof e.value !== 'boolean') {
                        let trainingOrganisationName = e.value.split('|')[0];
                        window.location.replace(`/mariner/trainigOrganisation/${trainingOrganisationName}`);
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
                            : e.element.find('.dx-datagrid-header-panel'),
                        appendedPagination = $('.custom-pagination.custom-pagination--certificates', $gridToolbar);

                    if (pageCount > 1) {
                        $select.empty();
                        for (let i = 0; i < pageCount; i++) {
                            (i === currentPage)
                                ? $select.append(`<option selected="selected" value="${i}">${i + 1}</option>>`)
                                : $select.append(`<option value="${i}">${i + 1}</option>>`);
                        }

                        appendedPagination.remove();
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
                        dataField: 'directions',
                        caption: 'Напрямки пiдготовки',
                        allowEditing: false,
                        allowFiltering: false,
                        cellTemplate: function(element, data) {
                            let directionsData = data.value;

                            directionsData.forEach((direction) => {
                                element.append(`<div class="c-cell__row">
                                                    <a class="c-cell__text" href="javascript:void(0);">
                                                        ${direction.directionName}
                                                    </a>
                                                    <span class="c-cell__amount">
                                                        ${direction.certAmount}
                                                    </span>
                                                </div>`);
                            });
                        },
                        visible: isInspector
                    },
                    {
                        dataField: 'organisation_id',
                        caption: 'Код НТЗ',
                        allowEditing: true,
                        allowFiltering: true,
                        cssClass: 'center-vertical'
                    },
                    {
                        dataField: 'organisation_name',
                        caption: 'Назва НТЗ',
                        allowEditing: false,
                        allowFiltering: true,
                        visible: !isInspector
                    },
                    {
                        dataField: 'organisation_name',
                        caption: 'Назва НТЗ',
                        allowEditing: false,
                        allowFiltering: true,
                        groupIndex: (isInspector) ? 0 : false
                    },
                    {
                        dataField: 'activated',
                        caption: 'Дати видачі',
                        dataType: 'date',
                        allowEditing: false,
                        format: 'dd.MM.yyyy',
                        cssClass: 'center-vertical'
                    },
                    {
                        dataField: 'active_till',
                        caption: 'Дійсний до',
                        dataType: 'date',
                        allowEditing: false,
                        format: 'dd.MM.yyyy',
                        cssClass: 'center-vertical'
                    },
                    {
                        type: "buttons",
                        width: 110,
                        cssClass: 'center-vertical',
                        buttons: [{
                            hint: 'Редагувати',
                            icon: 'edit',
                            onClick: function(e) {
                                if (isInspector) {
                                    let trainingOrganisationName = e.row.data.organisation_name.split('|')[0];

                                    window.location.replace(`/mariner/editTrainigOrganisation/${trainingOrganisationName}`);
                                }
                                else {
                                    window.location.replace(`/mariner/editTrainigOrganisation/${e.row.data.organisation_name}`);
                                }
                            }
                        }]
                    }
                ]
            }).dxDataGrid('instance');
    }
});