<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <material-card>
          <v-layout id="grid-controls"
          justify-space-between
          wrap>

            <!--Grid btns row left side-->
            <div>
            </div>

            <!--Grid btns row right side-->
            <div>
              <v-btn color="success" small :depressed="true"
              to="/mariner/app/training-organisations/edit/0">
                <v-icon>
                  mdi-plus-box
                </v-icon>
                <span class="font-weight-bold ml-1">
                Додати
              </span>
              </v-btn>
            </div>
          </v-layout>
          <DxGrid :tableConfig="tableConfig"
          v-on:init="gridInited()"
          ref="trainingOrganizationsGrid"/>
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
          selection: {
            mode: (gUserRole === 'Інспектор' || gUserRole === 'Адміністратор') ? false : 'multiple',
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
          onCellClick: (e) => {
            if (typeof e.value !== 'boolean') {
              let grid = e.component,
                  key = grid.getKeyByRowIndex(e.rowIndex),
                  isExpanded = grid.isRowExpanded(key),
                  organisationId = (isExpanded) ? e.row.data.items[0].id : e.data.collapsedItems[0].id;

              window.vue.$router.push(`/mariner/app/training-organisations/${organisationId}`);
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
          },
          columns: [
            {
              dataField: 'directions',
              caption: 'Напрямки пiдготовки',
              allowEditing: false,
              allowFiltering: false,
              visible: (gUserRole === 'Інспектор' || gUserRole === 'Адміністратор'),
              cellTemplate: (element, data) => {
                let grid = data.component,
                    key = grid.getKeyByRowIndex(data.rowIndex),
                    isExpand = !grid.isRowExpanded(key);

                element.append(`<div class="c-cell__row c-cell__row--min-width-490">
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

                if (isExpand) {
                  let directions = [];

                  if (!data.data.directions || data.data.directions.length === 0) {
                    grid.beginCustomLoading();

                    // Get training organisations directions info
                    axios.get(`/mariner/api/organisationDirectionsStat/?orgID=${data.data.id}`)
                      .then(res => {
                        let resDirections = res.data.organisation_directions;

                        resDirections.forEach((direction) => {
                          directions.push({
                            direction_id: direction.direction_id,
                            dirction_name: direction.dirction_name,
                            direction_reviewCertCount: direction.direction_reviewCertCount,
                            direction_issuedCertCount: direction.direction_issuedCertCount,
                            direction_reviewAndIssuedCertsCount: direction.direction_reviewAndIssuedCertsCount,
                            direction_certsLeftCount: direction.direction_certsLeftCount,
                            direction_allCertsCount: direction.direction_allCertsCount
                          });
                        });

                        this.dataSource.some((row) => {
                          if (row.id === data.data.id) {
                            row['directions'] = directions;
                            grid.option('dataSource', this.dataSource);

                            return true;
                          }
                        });

                        grid.endCustomLoading();
                      })
                      .catch((err) => {
                        console.log(err);
                      });
                  }
                  else {
                    directions = data.data.directions;
                  }

                  directions.forEach((direction) => {
                    element.append(`<div class="c-cell__row">
                              <a class="c-cell__text c-cell__text--link" href="javascript:void(0);"
                              onclick="window.vue.$router.push('/mariner/app/training-organisations/edit/${direction.direction_id}')">
                                  ${direction.dirction_name}
                              </a>
                              <span class="c-cell__amount">
                                  ${direction.direction_reviewCertCount}
                              </span>
                              <span class="c-cell__amount">
                                  ${direction.direction_issuedCertCount}
                              </span>
                              <span class="c-cell__amount">
                                  ${direction.direction_reviewAndIssuedCertsCount}
                              </span>
                              <span class="c-cell__amount">
                                  ${direction.direction_certsLeftCount}
                              </span>
                              <span class="c-cell__amount">
                                  ${direction.direction_allCertsCount}
                              </span>
                          </div>`);
                  });
                }
              }
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
              visible: (gUserRole !== 'Інспектор' && gUserRole !== 'Адміністратор')
            },
            {
              dataField: 'organisation_name',
              caption: 'Назва НТЗ',
              allowEditing: false,
              allowFiltering: true,
              groupIndex: (gUserRole === 'Інспектор' || gUserRole === 'Адміністратор') ? 0 : false
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
                onClick: e => {
                  let organisationId = e.row.data.id;

                  window.vue.$router.push(`/mariner/app/training-organisations/edit/${organisationId}`)
                }
              }]
            }
          ]
        }
      }
    },

    mounted() {

    },

    methods: {
      gridInited() {
        this.loadGridData();
      },

      loadGridData(refresh = false) {
        axios.get(`/mariner/api/organisations/`)
          .then(res => {
            let organisations = res.data.organisations;

            this.dataSource = [];
            organisations.forEach((organisation) => {
              let organisationData = {
                    id: organisation.id,
                    organisation_id: organisation.organisation_id,
                    organisation_name: organisation.organisation_name,
                    activated: organisation.activated,
                    active_till: organisation.active_till
                  };

              this.dataSource.push(organisationData);
            });

            let grid = this.$refs.trainingOrganizationsGrid.tableInstance,
                selected = (grid._options.selection.mode === 'multiple') ? `, Вибрано: ${grid.getSelectedRowKeys().length}` : '';

            grid.option('dataSource', this.dataSource);
            grid.option('pager.infoText', `Всього: ${grid.option('dataSource').length}${selected}`);
            grid.endCustomLoading();

            if (refresh) {
              grid.refresh();
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    }
  }
</script>
