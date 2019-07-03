$(function() {
    if ($('#training-organisations-main-grid').length > 0) {
        DevExpress.localization.locale('ru');

        // let organisationsInfo;

        var trainingOrganisationsMainGrid = $('#training-organisations-main-grid').dxDataGrid({
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
                loadPanel: {
                    shading: true,
                    shadingColor: 'rgba(255, 255, 255, .5)',
                    text: 'Завантаження...'
                },
                rowAlternationEnabled: true,
                onSelectionChanged: function(e) {
                    let selected = (e.component._options.selection.mode === 'multiple') ? `, Вибрано: ${e.component.getSelectedRowKeys().length}` : '';

                    e.component.option('pager.infoText', `Всього: ${trainigOrganisations.length}${selected}`);
                },
                onCellClick: function (e) {
                    if (e.column.dataField && !isInspector) {
                        window.location.replace(`/mariner/trainigOrganisation/${e.data.organisation_name}`);
                    }
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

                    e.component.option('pager.infoText', `Всього: ${trainigOrganisations.length}${selected}`);
                },
                columns: [
                    {
                        dataField: 'directions',
                        caption: 'Напрямки пiдготовки',
                        allowEditing: false,
                        allowFiltering: false,
                        cellTemplate: function(element, data) {
                            element.append(`<div class="c-cell__row">
                                                <span class="c-cell__text">
                                                </span>
                                                <span class="c-cell__amount">
                                                    В обробке
                                                </span>
                                                <span class="c-cell__amount">
                                                    Видано
                                                </span>
                                                <span class="c-cell__amount">
                                                    Всього
                                                </span>
                                                <span class="c-cell__amount">
                                                    Залишок
                                                </span>
                                                <span class="c-cell__amount">
                                                    Разом
                                                </span>
                                            </div>`);

                            trainingOrganisationsMainGrid.beginCustomLoading();

                            // Get training organisations/directions certs info
                            $.ajax({
                                url: organisationInfo,
                                method: 'GET',
                                dataType: 'json',
                                success: function (res) {
                                    let organisationsInfo = res.organisations;

                                    let directionsData = data.value,
                                        organisationId = data.data.id,
                                        expandedOrganisation = organisationsInfo.find(organisation => {
                                            return organisation.id === ~~organisationId;
                                        });

                                    directionsData.forEach((direction) => {
                                        let directionInfo = expandedOrganisation.organisation_directions.find(organisationDirection => {
                                            return organisationDirection.direction_id === ~~direction.directionId;
                                        });

                                        element.append(`<div class="c-cell__row">
                                                    <a class="c-cell__text" href="${direction.route}">
                                                        ${directionInfo.dirction_name}
                                                    </a>
                                                    <span class="c-cell__amount">
                                                        ${directionInfo.direction_reviewCertCount}
                                                    </span>
                                                    <span class="c-cell__amount">
                                                        ${directionInfo.direction_issuedCertCount}
                                                    </span>
                                                    <span class="c-cell__amount">
                                                        ${directionInfo.direction_reviewAndIssuedCertsCount}
                                                    </span>
                                                    <span class="c-cell__amount">
                                                        ${directionInfo.direction_certsLeftCount}
                                                    </span>
                                                    <span class="c-cell__amount">
                                                        ${directionInfo.direction_allCertsCount}
                                                    </span>
                                                </div>`);
                                    });
                                    trainingOrganisationsMainGrid.endCustomLoading();
                                }
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