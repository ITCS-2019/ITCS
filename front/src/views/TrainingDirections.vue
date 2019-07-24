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
              v-on:click="showCertFormModal(0)">
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
          ref="directionsGrid"/>
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

    <!--Certificate form modal-->
    <v-dialog v-model="directionFormModal" persistent max-width="95%"
    v-on:keydown.esc="directionFormModal = false">
      <v-card>
        <v-card-text>
          <DirectionForm :directionId="directionId"
          ref="directionForm">
          </DirectionForm>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="success" flat v-on:click="directionFormModal = false">Вiдхилити</v-btn>
          <v-btn color="success" v-on:click="saveDirection">Зберегти</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import DirectionForm from '@/components/forms/DirectionForm.vue'

export default {
  components: {
    DirectionForm
  },

  data() {
    return {
      snackbar: false,
      snackbarConfig: {
        color: null,
        icon: null,
        message: null
      },
      directionId: 0,
      directionFormModal: false,
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
              if (gUserRole === 'НТЗ') {
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
            type: "buttons",
            width: 110,
            visible: gUserRole !== 'НТЗ',
            cssClass: 'center-vertical',
            buttons: [{
              hint: 'Редагувати',
              icon: 'edit',
              onClick: (e) => {
                this.showCertFormModal(e.row.data.id);
              }
            }]
          }
        ]
      }
    }
  },

  methods: {
    loadGridData(refresh = false) {
      axios.get(`/mariner/api/directionsInfo/`)
        .then(res => {
          let directions = res.data.trainigDirections;

          this.dataSource = [];
          directions.forEach((direction) => {
            this.dataSource.push({
              id: (gUserRole === 'НТЗ') ? direction.direction_id : direction.id,
              price_id: direction.price_id,
              direction_title: (gUserRole === 'НТЗ') ? direction.dirction_name : direction.direction_title,
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

          if (refresh) {
            grid.refresh();
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    gridInited() {
      this.loadGridData();
    },

    showCertFormModal(directionId) {
      this.directionId = directionId;
      this.directionFormModal = true;
      this.$nextTick(() => {
        this.$refs.directionForm.clearFormData();
        this.$refs.directionForm.loadFormData();
      });
    },

    saveDirection() {
      let formData = {
        direction_title: this.$refs.directionForm.direction_title,
        price_id: this.$refs.directionForm.price_id,
        level: this.$refs.directionForm.level,
        allow_functions: this.$refs.directionForm.allow_functions,
        regulationInfo: this.$refs.directionForm.regulationInfo,
        regulationInfoEng: this.$refs.directionForm.regulationInfoEng,
        courseInfo: this.$refs.directionForm.courseInfo,
        courseInfoEng: this.$refs.directionForm.courseInfoEng,
        inspectionInfo: this.$refs.directionForm.inspectionInfo,
        inspectionInfoEng: this.$refs.directionForm.inspectionInfoEng
      };

      console.log(formData);

      axios({
        method: (this.directionId === 0) ? 'POST' : 'PUT',
        url: `/mariner/api/directions/${(this.directionId === 0) ? '' : `${this.directionId}/`}`,
        data: formData
      })
        .then(res => {
          this.loadGridData(true);
          this.directionFormModal = false;

          this.snackbarConfig.icon = 'mdi-check-circle';
          this.snackbarConfig.color = 'success';
          this.snackbarConfig.message = (this.certId === 0)
                  ? 'Сертифiкат успiшно створено!'
                  : 'Сертифiкат успiшно вiдредаговано!';
          this.snackbar = true;
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }
}
</script>
