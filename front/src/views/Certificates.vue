<!--TODO change certsGrid to grid-->
<template>
  <v-container
    fill-height
    fluid
    grid-list-xl
    pt-0
  >
    <v-layout
      justify-center
      wrap
    >
      <v-flex
        md12
      >
        <material-card>
          <v-layout id="grid-controls"
          justify-space-between
          wrap>

            <!--Grid btns row left side-->
            <div>
              <v-menu offset-y
              content-class="dropdown-menu"
              transition="slide-y-transition">
                <v-btn slot="activator"
                color="success"
                small>
                  <v-icon left>
                    mdi-file-excel
                  </v-icon>
                  <span class="font-weight-bold ml-1">
                    Excel
                  </span>
                </v-btn>
                <v-card>
                  <v-list dense>
                    <v-list-tile key="all"
                    v-on:click="e => exportGrid(false, 'XLSExp')">
                      <v-list-tile-title v-text="`Експортувати все`"/>
                    </v-list-tile>
                    <v-list-tile key="checked"
                    v-on:click="e => exportGrid(true, 'XLSExp')">
                      <v-list-tile-title v-text="`Експортувати обране`"/>
                    </v-list-tile>
                  </v-list>
                </v-card>
              </v-menu>
              <v-menu offset-y
              content-class="dropdown-menu"
              transition="slide-y-transition">
                <v-btn slot="activator"
                color="success"
                small>
                  <v-icon left>
                    mdi-file-pdf
                  </v-icon>
                  <span class="font-weight-bold ml-1">
                    PDF
                  </span>
                </v-btn>
                <v-card>
                  <v-list dense>
                    <v-list-tile key="all"
                    v-on:click="e => exportGrid(false, 'PdfExp')">
                      <v-list-tile-title v-text="`Експортувати все`"/>
                    </v-list-tile>
                    <v-list-tile key="checked"
                    v-on:click="e => exportGrid(true, 'PdfExp')">
                      <v-list-tile-title v-text="`Експортувати обране`"/>
                    </v-list-tile>
                  </v-list>
                </v-card>
              </v-menu>
              <v-btn color="success" small
              v-on:click="printGrid('certsGrid')">
                <v-icon>
                  mdi-printer
                </v-icon>
                <span class="font-weight-bold ml-1">
                  Друкувати
                </span>
              </v-btn>
            </div>

            <!--Grid btns row right side-->
            <div>
              <v-btn color="success"
              small
              v-on:click="handleCerts">
                <v-icon>
                  mdi-file-move
                </v-icon>
                <span class="font-weight-bold ml-1">
                  В обробку
                </span>
              </v-btn>
              <v-btn color="warning"
              small
              v-on:click="e => showModal('Видалити обранi сертифiкати?')"
              class="ml-1"
              :depressed="true">
                <v-icon>
                  mdi-trash-can
                </v-icon>
                <span class="font-weight-bold ml-1">
                  Видалити
                </span>
              </v-btn>
            </div>
          </v-layout>

          <DxGrid :tableConfig="tableConfig" ref="certsGrid"/>
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

    <!--Modal-->
    <v-dialog v-model="modal" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">
          Пiдтвердiть дiю
        </v-card-title>
        <v-card-text>
          {{modalConfig.message}}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1"
          flat
          v-on:click="removeCerts">
            Так
          </v-btn>
          <v-btn color="red darken-1"
          flat
          v-on:click="modal = false">
            Нi
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      modal: false,
      modalConfig: {
        message: null
      },
      snackbar: false,
      snackbarConfig: {
        color: null,
        icon: null,
        message: null
      },
      exportType: null,
      clickDelay: undefined,
      dataSource: [],
      tableConfig: {
        dataSource: [],
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
        rowAlternationEnabled: true,
        customizeExportData: (cols, rows) => {
          let certIDs = [];

          if (rows.length > 0) {
            rows.forEach((row) => {
              certIDs.push(row.data.certificateId);
            });

            let element = document.createElement('a');
            element.setAttribute('href', `/mariner/api/exportToPrint/?exportType=${this.exportType}&certIDs=${certIDs.join(',')}`);
            element.setAttribute('target', '_blank');
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
          }
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
          let certsGrid = e.component,
              selected = (certsGrid._options.selection.mode === 'multiple') ? `, Вибрано: ${certsGrid.getSelectedRowKeys().length}` : '';

          certsGrid.option('pager.infoText', `Всього: ${certsGrid.option('dataSource').length}${selected}`);
        },
        onCellClick: (e) => {
          let certsGrid = e.component,
              _this = this;

          function initialClick() {
            certsGrid.clickCount = 1;
            certsGrid.clickKey = e.key;
            certsGrid.clickDate = new Date();
            _this.clickDelay = setTimeout(() => {
              if (e.column.dataField) {
                if (e.row.isSelected) {
                  certsGrid.deselectRows([e.key]);
                }
                else {
                  certsGrid.selectRows([e.key], true);
                }
              }
            }, 300);
          }

          function doubleClick() {
            clearTimeout(_this.clickDelay);
            certsGrid.clickCount = 0;
            certsGrid.clickKey = 0;
            certsGrid.clickDate = null;
            switch (e.column.dataField) {
              case 'certificateNumber':
                window.location.replace(`/mariner/editCertification/${e.data.certificateId}`);
                return;
              case 'sailor':
                window.location.replace(`/mariner/sailor/${e.data.sailorId}`);
                return;
              case 'trainigOrganisation':
                window.location.replace(`/mariner/trainigOrganisation/${e.data.trainigOrganisation}`);
                return;
            }

            if (e.column.dataField) {
              window.location.replace(`/mariner/editCertification/${e.data.certificateId}`);
            }
          }

          if ((!certsGrid.clickCount) || (certsGrid.clickCount != 1) || (certsGrid.clickKey != e.key) ) {
            initialClick();
          }
          else if (certsGrid.clickKey == e.key) {
            if (((new Date()) - certsGrid.clickDate) <= 300) {
              doubleClick();
            }
            else {
              initialClick();
            }
          }
        },
        onContentReady: (e) => {
          function changePage(page) {
            e.component.pageIndex(page);
          }

          let $customPagination = $('.custom-pagination.custom-pagination--grid'),
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
              $appendedPagination = $('.custom-pagination.custom-pagination--grid', $gridToolbar);

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
            dataField: 'certificateId',
            visible: false,
            allowExporting: false
          },
          {
            dataField: 'certificateNumber',
            caption: '№ Сертифіката',
            allowEditing: false,
            allowFiltering: true,
          },
          {
            dataField: 'blankNumber',
            caption: '№ Бланку',
            allowEditing: false,
            allowFiltering: true,
          },
          {
            dataField: 'issueDate',
            caption: 'Дата видачі',
            dataType: 'date',
            allowEditing: false,
            format: 'dd.MM.yyyy',
          },
          {
            dataField: 'validDate',
            caption: 'Дійсний до',
            dataType: 'date',
            allowEditing: false,
            format: 'dd.MM.yyyy',
          },
          {
            dataField: 'certificateNumberGenerated',
            caption: '№ сертифіката(сген.)',
            allowEditing: false,
            visible: false
          },
          {
            dataField: 'trainingDirection',
            caption: 'Напрямок підготовки',
            allowEditing: false,
            allowFiltering: true,
          },
          {
            dataField: 'sailorId',
            visible: false,
          },
          {
            dataField: 'sailor',
            caption: 'Моряк',
            allowEditing: false,
            allowFiltering: true,
          },
          {
            dataField: 'trainigOrganisation',
            caption: 'НТЗ',
            allowEditing: false,
            allowFiltering: true,
            visible: gUserRole !== 'НТЗ',
          },
          {
            dataField: 'status',
            caption: 'Статус',
            allowEditing: false,
          }
        ]
      }
    }
  },

  mounted() {
    axios.get(`/mariner/api/certificates/`)
      .then(res => {
        let certs = res.data.certificates;

        certs.forEach((cert) => {
          let status;

          switch (cert.status) {
            case 0:
              status = 'Чернетка';
              break;
            case 1:
              status = 'Обробка';
              break;
            case 2:
              status = 'Видан';
              break;
            case 3:
              status = 'Анульований';
              break;
          }

          this.dataSource.push({
            certificateId: cert.id,
            certificateNumber: cert.certf_number,
            blankNumber: cert.form_number,
            issueDate: cert.date_of_issue,
            validDate: cert.valid_date,
            trainingDirection: cert.training_direction.direction_title,
            sailorId: cert.sailor_id,
            sailor: `${cert.first_name_ukr} ${cert.last_name_ukr}`,
            trainigOrganisation: cert.trainigOrganisation_name,
            status: status
          });
        });

        let certsGrid = this.$refs.certsGrid.tableInstance,
            selected = (certsGrid._options.selection.mode === 'multiple') ? `, Вибрано: ${certsGrid.getSelectedRowKeys().length}` : '';

        certsGrid.option('dataSource', this.dataSource);
        certsGrid.option('pager.infoText', `Всього: ${certsGrid.option('dataSource').length}${selected}`);
        certsGrid.endCustomLoading();
      })
      .catch((err) => {
        console.log(err);
      });
  },

  methods: {
    showModal(message = false) {
      let grid = this.$refs.certsGrid.tableInstance,
          selectedRows = grid.getSelectedRowsData();

      this.modalConfig.message = message;

      if (selectedRows.length > 0) {
        let isInvalidData = false;

        selectedRows.some((row) => {
          if (row.status !== 'Чернетка') {
            isInvalidData = true;
            return true;
          }
        });

        if (!isInvalidData) {
          this.modal = true;
        }
        else {
          this.snackbarConfig.icon = 'mdi-alert-circle';
          this.snackbarConfig.color = 'red';
          this.snackbarConfig.message = 'Можливо видаляти тiльки сертифiкати зi статусом "Чернетка"!';
          this.snackbar = true;
        }
      }
      else {
        this.snackbarConfig.icon = 'mdi-alert-circle';
        this.snackbarConfig.color = 'red';
        this.snackbarConfig.message = 'Не вибрано жодного сертифiката!';
        this.snackbar = true;
      }
    },

    removeCerts() {
      let grid = this.$refs.certsGrid.tableInstance,
          selectedRows = grid.getSelectedRowsData(),
          sendRows = [];

      this.modal = false;

      selectedRows.some((row) => {
        sendRows.push(row.certificateId);
      });

      axios.get(`/mariner/api/removeDraftCerts/`,
      {
        params: {
          certIDs: sendRows.join(',')
        }
      })
        .then(res => {
          if (!res.error) {
            this.snackbarConfig.icon = 'mdi-check-circle';
            this.snackbarConfig.color = 'success';
            this.snackbarConfig.message = 'Сертифiкати успiшно видаленi!';
            this.snackbar = true;

            // change status in grid without reload
            let i = this.dataSource.length;

            while (i--) {
              if (sendRows.includes(this.dataSource[i].certificateId)) {
                this.dataSource.splice(i, 1);
              }
            }
            grid.refresh();
          }
          else {
            this.snackbarConfig.icon = 'mdi-alert-circle';
            this.snackbarConfig.color = 'red';
            this.snackbarConfig.message = res.error_message;
            this.snackbar = true;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    handleCerts() {
      let grid = this.$refs.certsGrid.tableInstance,
          selectedRows = grid.getSelectedRowsData();

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
          axios.get(`/mariner/api/changeToReviewStatus/`,
          {
            params: {
              certIDs: sendRows.join(',')
            }
          })
            .then(res => {
              if (!res.error) {
                this.snackbarConfig.icon = 'mdi-check-circle';
                this.snackbarConfig.color = 'success';
                this.snackbarConfig.message = 'Сертифiкати успiшно вiдправленi в обробку!';
                this.snackbar = true;

                // change status in grid without reload
                this.dataSource.forEach((dataItem) => {
                  if (sendRows.includes(dataItem.certificateId)) {
                    dataItem.status = 'Обробка';
                  }
                });
                grid.refresh();
              }
              else {
                this.snackbarConfig.icon = 'mdi-alert-circle';
                this.snackbarConfig.color = 'red';
                this.snackbarConfig.message = res.error_message;
                this.snackbar = true;
              }
            })
            .catch((err) => {
              console.log(err);
            });
        }
        else {
          this.snackbarConfig.icon = 'mdi-alert-circle';
          this.snackbarConfig.color = 'red';
          this.snackbarConfig.message = 'Змiнити статус на "Обробка" можливо тiльки для сертифiкатiв зi статусом "Чернетка"!';
          this.snackbar = true;
        }
      }
      else {
        this.snackbarConfig.icon = 'mdi-alert-circle';
        this.snackbarConfig.color = 'red';
        this.snackbarConfig.message = 'Не вибрано жодного сертифiката!';
        this.snackbar = true;
      }
    },

    exportGrid(isSelection, exportType) {
      let grid = this.$refs.certsGrid.tableInstance;

      this.exportType = exportType;
      grid.exportToExcel((typeof isSelection === 'boolean') ? isSelection : false);
    },

    printGrid(gridRef) {

      // TODO: Refactor to pure js
      let $grid = this.$refs[`${gridRef}`].tableInstance._$element,
          $head = $('.dx-datagrid-headers', $grid),
          $rows = $('.dx-datagrid-rowsview', $grid),
          mywindow = window.open('', 'PRINT', 'height=400,width=600');

      mywindow.document.write('<html><head><title>' + document.title  + '</title>');
      mywindow.document.write('</head><body >');
      mywindow.document.write('<h1>' + document.title  + '</h1>');
      mywindow.document.write(`${$head.html()}${$rows.html()}`);
      mywindow.document.write('</body></html>');

      mywindow.document.close();
      mywindow.focus();

      mywindow.print();
      mywindow.close();

      return true;
    }
  }
}
</script>
