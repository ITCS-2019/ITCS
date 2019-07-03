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
              v-on:click="showSailorFormModal()">
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

    <!--Notifications-->
    <v-snackbar :color="snackbarConfig.color"
    :top="true"
    v-model="snackbar"
    dark>
      <v-icon color="white"
      class="mr-3">
        {{snackbarConfig.icon}}
      </v-icon>
      <div>
        {{snackbarConfig.message}}
      </div>
      <v-icon size="16"
      v-on:click="snackbar = false">
        mdi-close-circle
      </v-icon>
    </v-snackbar>

    <!--Training organization form modal-->
    <v-dialog v-model="sailorFormModal" persistent max-width="95%"
    v-on:keydown.esc="sailorFormModal = false">
      <v-card>
        <v-card-text>
          <SailorForm ref="sailorForm">
          </SailorForm>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="success" flat v-on:click="sailorFormModal = false">Вiдхилити</v-btn>
          <v-btn color="success" v-on:click="saveSailor">Зберегти</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
  import SailorForm from '@/components/forms/SailorForm.vue'

  export default {
    components: {
      SailorForm
    },

    data() {
      return {
        sailorFormModal: false,
        dataSource: [],
        snackbar: false,
        snackbarConfig: {
          color: null,
          icon: null,
          message: null
        },
        tableConfig: {
          dataSource: [],
          allowColumnReordering: false,
          allowColumnResizing: true,
          columnAutoWidth: false,
          showBorders: true,
          showRowLines: true,
          selection: {
            mode: (gUserRole === 'Інспектор') ? false : 'multiple',
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
            // let selected = (e.component._options.selection.mode === 'multiple') ? `, Вибрано: ${e.component.getSelectedRowKeys().length}` : '';
            //
            // e.component.option('pager.infoText', `Всього: ${trainigOrganisations.length}${selected}`);
          },
          onCellClick: function (e) {
            if (e.column.dataField && gUserRole !== 'Інспектор') {
              window.location.replace(`/mariner/trainigOrganisation/${e.data.organisation_name}`);
            }
            else if (gUserRole === 'Інспектор'
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

            // let selected = (e.component._options.selection.mode === 'multiple') ? `, Вибрано: ${e.component.getSelectedRowKeys().length}` : '';
            //
            // e.component.option('pager.infoText', `Всього: ${trainigOrganisations.length}${selected}`);
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
                              return organisation.organisation_id === ~~organisationId;
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
        }
      }
    },

    mounted() {

    },

    methods: {
      saveSailor() {
        let formData = {
          first_name_en: this.$refs.sailorForm.first_name_en,
          last_name_en: this.$refs.sailorForm.last_name_en,
          last_name_ukr: this.$refs.sailorForm.last_name_ukr,
          first_name_ukr: this.$refs.sailorForm.first_name_ukr,
          second_name_ukr: this.$refs.sailorForm.second_name_ukr,
          born: this.$refs.sailorForm.resetFormatDate(this.$refs.sailorForm.born),
          inn: this.$refs.sailorForm.inn,
          sex: this.$refs.sailorForm.sex,
          died: null
        };

        axios({
          method: 'post',
          url: `/mariner/api/sailors/`,
          data: formData
        })
                .then(res => {
                  this.loadGridData(true);
                  this.sailorFormModal = false;

                  this.snackbarConfig.icon = 'mdi-check-circle';
                  this.snackbarConfig.color = 'success';
                  this.snackbarConfig.message = 'Моряк успішно внесений!';
                  this.snackbar = true;
                })
                .catch((err) => {
                  console.log(err);
                  this.snackbarConfig.icon = 'mdi-alert-circle';
                  this.snackbarConfig.color = 'red';
                  this.snackbarConfig.message = err;
                  this.snackbar = true;
                });
      },

      showSailorFormModal() {
        this.sailorFormModal = true;
      },

      gridInited() {
        let grid = this.$refs.trainingOrganizationsGrid.tableInstance;
        //
        // this.loadGridData();
        //
        // if (this.$route.params.columns) {
        //   let columns = this.$route.params.columns;
        //
        //   columns.forEach((column) => {
        //     grid.beginUpdate();
        //     grid.columnOption(column.dataField, 'filterValue', column.filterValue);
        //     grid.endUpdate();
        //   });
        // }
        grid.endCustomLoading();
      },

      loadGridData(refresh = false) {
        axios.get(`/mariner/api/sailors/`)
          .then(res => {
            let sailors = res.data;

            sailors.forEach((sailor) => {
              this.dataSource.push({
                id: sailor.id,
                pib: {
                  first_name_ukr: sailor.first_name_ukr,
                  second_name_ukr: sailor.second_name_ukr,
                  last_name_ukr: sailor.last_name_ukr,
                  first_name_en: sailor.first_name_en,
                  last_name_en: 'last name',
                },
                sex: sailor.sex,
                born: sailor.born,
                inn: sailor.inn,
              });
            });

            let grid = this.$refs.sailorsGrid.tableInstance,
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
