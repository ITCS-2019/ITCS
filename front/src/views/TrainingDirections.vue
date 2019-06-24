<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <material-card>
          <DxGrid :tableConfig="tableConfig" ref="directionsGrid"/>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>

export default {
  data() {
    return {
      dataSource: [],
      tableConfig: {
        dataSource: [],
        allowColumnReordering: false,
        allowColumnResizing: true,
        columnAutoWidth: false,
        showBorders: true,
        showRowLines: true,
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
        rowAlternationEnabled: true,
        onSelectionChanged: function (e) {
          let grid = e.component,
                  selected = (grid._options.selection.mode === 'multiple') ? `, Вибрано: ${grid.getSelectedRowKeys().length}` : '';

          grid.option('pager.infoText', `Всього: ${certsGrid.option('dataSource').length}${selected}`);
        },
        onCellClick: function (data) {
          switch (data.column.dataField) {
            case 'status':
              let grid = data.component,
                  newStatus = (~~data.data.status === 0) ? 1 : 0;

              axios.get(`/mariner/api/changeTrainigDirectionStatus/`,
              {
                params: {
                  certID: data.data.id,
                  dirStatus: newStatus
                }
              })
                .then(res => {
                  let trainigDirections = grid.option('dataSource');

                  trainigDirections.some((direction) => {
                    if (~~direction.id === ~~data.data.id) {
                      direction.status = newStatus;
                    }
                  });
                  grid.option('dataSource', trainigDirections);
                })
                .catch((err) => {
                  console.log(err);
                });
              break;
          }
        },
        onContentReady: function (e) {
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
            } else {
              $firstPageBtn.attr('disabled', false);
              $prevPageBtn.attr('disabled', false);
            }

            if ((currentPage + 1) === pageCount) {
              $lastPageBtn.attr('disabled', true);
              $nextPageBtn.attr('disabled', true);
            } else {
              $lastPageBtn.attr('disabled', false);
              $nextPageBtn.attr('disabled', false);
            }

            $select.on('change', function () {
              changePage($(this).val(), pageCount)
            });
            $firstPageBtn.on('click', function () {
              changePage(0, pageCount)
            });
            $lastPageBtn.on('click', function () {
              changePage(pageCount - 1)
            });
            $nextPageBtn.on('click', function () {
              changePage(currentPage + 1)
            });
            $prevPageBtn.on('click', function () {
              changePage(currentPage - 1)
            });

            $customPagination.fadeIn('fast');
          }
        },
        columns: [
          {
            dataField: 'id',
            visible: false
          },
          {
            dataField: 'price_id',
            caption: 'Код',
            allowEditing: false,
            allowFiltering: true,
            sortOrder: 'asc',
            alignment: 'left'
          },
          {
            dataField: 'direction_title',
            caption: 'Напрямок підготовки',
            allowEditing: false,
            allowFiltering: true
          },
          {
            dataField: 'direction_reviewCertCount',
            caption: 'В обробцi',
            allowEditing: false,
            allowFiltering: true,
            alignment: 'left',
            visible: gUserRole === 'НТЗ',
          },
          {
            dataField: 'direction_issuedCertCount',
            caption: 'Видано',
            allowEditing: false,
            allowFiltering: true,
            alignment: 'left',
            visible: gUserRole === 'НТЗ',
          },
          {
            dataField: 'direction_reviewAndIssuedCertsCount',
            caption: 'Всього',
            allowEditing: false,
            allowFiltering: true,
            alignment: 'left',
            visible: gUserRole === 'НТЗ',
          },
          {
            dataField: 'allow_functions',
            caption: 'Рівень функцій',
            allowEditing: false,
            allowFiltering: true
          },
          {
            dataField: 'level',
            caption: 'Рівень кваліфікації',
            allowEditing: false,
            allowFiltering: true
          },
          {
            dataField: 'status',
            caption: 'Статус',
            allowEditing: false,
            allowFiltering: false,
            cssClass: 'center-vertical',
            alignment: 'left',
            cellTemplate: function (element, data) {
              element.append(`<div style="text-align: center; color: green;">
                                ${(~~data.value === 0) ? '&#10004;' : '&#x274C;'}
                            </div>`);
            }
          },
          {
            type: "buttons",
            width: 110,
            visible: gUserRole !== 'НТЗ',
            cssClass: 'center-vertical',
            buttons: [{
              hint: 'Редагувати',
              icon: 'edit',
              onClick: function (e) {
                window.location.replace(`/mariner/editDirection/${e.row.data.id}`);
              }
            }]
          }
        ]
      }
    }
  },

  mounted() {
    axios.get(`/mariner/api/directions/`)
      .then(res => {
        let directions = res.data.directions;

        directions.forEach((direction) => {
          this.dataSource.push({
            id: direction.id,
            price_id: direction.price_id,
            direction_title: direction.direction_title,
            direction_reviewCertCount: direction.direction_reviewCertCount,
            direction_issuedCertCount: direction.direction_issuedCertCount,
            direction_reviewAndIssuedCertsCount: direction.direction_reviewAndIssuedCertsCount,
            allow_functions: direction.allow_functions,
            level: direction.level,
            status: direction.status
          });
        });

        let grid = this.$refs.directionsGrid.tableInstance,
            selected = (grid._options.selection.mode === 'multiple') ? `, Вибрано: ${grid.getSelectedRowKeys().length}` : '';

        grid.option('dataSource', this.dataSource);
        grid.option('pager.infoText', `Всього: ${grid.option('dataSource').length}${selected}`);
        grid.endCustomLoading();
      })
      .catch((err) => {
        console.log(err);
      });
  }
}
</script>
