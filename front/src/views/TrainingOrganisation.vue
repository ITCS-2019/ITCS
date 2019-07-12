<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <material-card>
          <div class="title font-weight-regular">
            {{organisationName}}
          </div>
          <div class="body-2 font-weight-regular mt-3">
            Діючи Напрямки Підготовки
          </div>
          <v-data-table :headers="headers"
          :items="directions"
          hide-actions
          class="elevation-1 mt-1">
            <template v-slot:items="props">
              <td>{{ props.item.directionId }}</td>
              <td class="text-xs-left">{{ props.item.direction_title }}</td>
              <td class="justify-center pl-2 pr-2">
                <v-edit-dialog large
                lazy
                v-on:save="e => setRangeNumbers(props.item.directionId, props.item.rangeNumStart, props.item.rangeNumEnd)"
                v-on:close="close">
                  <v-btn color="success"
                   small>
                    <v-icon left>
                      mdi-plus-box
                    </v-icon>
                    <span class="font-weight-bold ml-1">
                      Присвоїти номери
                    </span>
                  </v-btn>
                  <template v-slot:input>
                    <div class="mt-3 title">Додати номери</div>
                  </template>
                  <template v-slot:input>
                    <v-text-field v-model="props.item.rangeNumStart"
                    label="Початок діапазону"
                    single-line
                    autofocus
                    ></v-text-field>
                    <v-text-field v-model="props.item.rangeNumEnd"
                    label="Кінець діапазону"
                    single-line
                    ></v-text-field>
                  </template>
                </v-edit-dialog>
              </td>
            </template>
          </v-data-table>
        </material-card>

        <material-card class="mt-3">
          <div class="title font-weight-regular">
            Сертифікати на підтвердження
          </div>
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
                    mdi-numeric
                  </v-icon>
                  <span class="font-weight-bold ml-1">
                    Присвоїти номери
                  </span>
                </v-btn>
                <v-card>
                  <v-list dense>
                    <v-list-tile key="all"
                    v-on:click="e => exportGrid(false, 'Assign')">
                      <v-list-tile-title v-text="`Присвоїти всi`"/>
                    </v-list-tile>
                    <v-list-tile key="checked"
                    v-on:click="e => exportGrid(true, 'Assign')">
                      <v-list-tile-title v-text="`Присвоїти обраним`"/>
                    </v-list-tile>
                  </v-list>
                </v-card>
              </v-menu>
              <v-btn color="success" small
              v-on:click="e => newTab('http://registr-itcs.ddns.net/sidebar/Templates/RequestNumbCert')">
                <v-icon>
                  mdi-certificate
                </v-icon>
                <span class="font-weight-bold ml-1">
                  Замовлення сертифікатів
                </span>
              </v-btn>
              <v-menu offset-y
              content-class="dropdown-menu"
              transition="slide-y-transition">
                <v-btn slot="activator"
                color="success"
                small>
                  <v-icon left>
                    mdi-download
                  </v-icon>
                  <span class="font-weight-bold ml-1">
                    Вигрузка у Реєстр
                  </span>
                </v-btn>
                <v-card>
                  <v-list dense>
                    <v-list-tile key="all"
                    v-on:click="e => exportGrid(false, 'Register')">
                      <v-list-tile-title v-text="`Вигрузити всi`"/>
                    </v-list-tile>
                    <v-list-tile key="checked"
                    v-on:click="e => exportGrid(true, 'Register')">
                      <v-list-tile-title v-text="`Вигрузити обранi`"/>
                    </v-list-tile>
                  </v-list>
                </v-card>
              </v-menu>
              <v-btn color="success" small
              v-on:click="e => newTab('http://registr-itcs.ddns.net/sidebar/Templates/CertSeafarers')">
                <v-icon>
                  mdi-import
                </v-icon>
                <span class="font-weight-bold ml-1">
                  Імпорт до Реєстру
                </span>
              </v-btn>
              <v-menu offset-y
              content-class="dropdown-menu"
              transition="slide-y-transition">
                <v-btn slot="activator"
                color="success"
                small>
                  <v-icon left>
                    mdi-checkbox-marked-outline
                  </v-icon>
                  <span class="font-weight-bold ml-1">
                    Видати Сертифікати
                  </span>
                </v-btn>
                <v-card>
                  <v-list dense>
                    <v-list-tile key="all"
                    v-on:click="e => exportGrid(false, 'GiveCerts')">
                      <v-list-tile-title v-text="`Видати всi`"/>
                    </v-list-tile>
                    <v-list-tile key="checked"
                    v-on:click="e => exportGrid(true, 'GiveCerts')">
                      <v-list-tile-title v-text="`Видати обранi`"/>
                    </v-list-tile>
                  </v-list>
                </v-card>
              </v-menu>
              <v-btn color="success" small
              v-on:click="exportGrid(true, 'setCertsNumbers')">
              <v-icon>
                mdi-counter
              </v-icon>
              <span class="font-weight-bold ml-1">
                №-№
              </span>
            </v-btn>
            </div>
          </v-layout>
          <DxGrid :tableConfig="tableConfig"
          v-on:init="gridInited()"
          ref="certsOnReviewGrid"/>
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
    <v-dialog v-model="certFormModal" persistent max-width="95%"
    v-on:keydown.esc="certFormModal = false">
      <v-card>
        <v-card-text>
          <CertificateForm :certId="certId"
          ref="certForm">
          </CertificateForm>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="success" flat v-on:click="certFormModal = false">Вiдхилити</v-btn>
          <v-btn color="success" v-on:click="saveCert">Зберегти</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
  import CertificateForm from '@/components/forms/CertificateForm.vue'

  export default {
    components: {
      CertificateForm
    },

    data() {
      return {
        headers: [
          {
            text: 'ID',
            align: 'left',
            sortable: false,
            value: 'directionId'
          },
          {
            text: 'Напрямок Підготовки',
            align: 'left',
            sortable: false,
            value: 'direction_title'
          },
          {
            text: 'Сервiс',
            sortable: false,
            value: 'name',
          }
        ],
        directions: [],
        organisationName: null,
        exportType: null,
        snackbar: false,
        snackbarConfig: {
          color: null,
          icon: null,
          message: null
        },
        certFormModal: false,
        certId: 0,
        clickDelay: undefined,
        organisationId: this.$route.params.id,
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
          onCellPrepared: function (data) {
            if (data.isEditing) {
              let editInput = data.cellElement.find('input')[0];

              editInput.setSelectionRange(0, editInput.value.length);
            }
          },
          onRowUpdated: function(options) {
            $.ajax({
              url: '/mariner/api/changeCertNumber/',
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
          rowAlternationEnabled: true,
          customizeExportData: (cols, rows) => {
            let certIDs = [],
                _this= this;

            if (rows.length > 0) {

              // Assign certs
              if (_this.exportType === 'Assign') {
                rows.forEach(row => certIDs.push(row.data.certificateId));

                $.ajax({
                  url: '/mariner/api/giveCertNumber/',
                  method: 'GET',
                  data: {
                    certIDs: certIDs.join(',')
                  },
                  dataType: 'json',
                  success: function (res) {
                    if (!res.error) {
                      _this.snackbarConfig.icon = 'mdi-check-circle';
                      _this.snackbarConfig.color = 'success';
                      _this.snackbarConfig.message = `Номера було успiшно присвоєно!`;
                      _this.snackbar = true;
                    }
                    else {
                      _this.snackbarConfig.icon = 'mdi-alert-circle';
                      _this.snackbarConfig.color = 'red';
                      _this.snackbarConfig.message = `Виникла помилка при присвоєннi!`;
                      _this.snackbar = true;
                    }
                  }
                });
              }

              // Upload to register/issue certs
              if (_this.exportType === 'Register' || _this.exportType === 'GiveCerts') {
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

                  // TODO: Refactor Remove ifs
                  if (_this.exportType === 'Register') {
                    let element = document.createElement('a');
                    element.setAttribute('href', `/mariner/api/exportXLS?exportType=${_this.exportType}&certIDs=${certIDs.join(',')}`);
                    element.style.display = 'none';
                    document.body.appendChild(element);
                    element.click();
                    document.body.removeChild(element);
                  }
                  else {
                    axios.get(`/mariner/api/exportXLS?exportType=${_this.exportType}&certIDs=${certIDs.join(',')}`)
                      .then(res => {
                        _this.loadGridData(true);
                        _this.snackbarConfig.icon = 'mdi-check-circle';
                        _this.snackbarConfig.color = 'success';
                        _this.snackbarConfig.message = `Сертифiкати успiшно виданi!`;
                        _this.snackbar = true;
                      })
                      .catch((err) => {
                        console.log(err);
                      });
                  }
                }
                else {
                  _this.snackbarConfig.icon = 'mdi-alert-circle';
                  _this.snackbarConfig.color = 'warning';
                  _this.snackbarConfig.message = `Сертифiкати на вигрузку повиннi мати однаковi напрямки пiдготовки!`;
                  _this.snackbar = true;
                }
              }

              // Set Certificates range numbers
              if (_this.exportType === 'setCertsNumbers') {
                let isEmptyNumbers = true;

                rows.some((row) => {
                  if (row.data.certificateNumber === null || row.data.certificateNumber === '') {
                    certIDs.push(row.data.certificateId);
                  }
                  else {
                    isEmptyNumbers = false;
                    return true;
                  }
                });

                if (isEmptyNumbers) {
                  axios.get(`/mariner/api/setRangeNumbers/?certIDs=${certIDs.join(',')}`)
                    .then(res => {
                      _this.loadGridData(true);
                      _this.snackbarConfig.icon = 'mdi-check-circle';
                      _this.snackbarConfig.color = 'success';
                      _this.snackbarConfig.message = `Номера успiшно присвоєнi!`;
                      _this.snackbar = true;
                    })
                    .catch((err) => {
                      console.log(err);
                    });
                }
                else {
                  _this.snackbarConfig.icon = 'mdi-alert-circle';
                  _this.snackbarConfig.color = 'warning';
                  _this.snackbarConfig.message = `Номера сертифiкатiв повиннi бути пустими!`;
                  _this.snackbar = true;
                }
              }
            }
            else {
              _this.snackbarConfig.icon = 'mdi-alert-circle';
              _this.snackbarConfig.color = 'warning';
              _this.snackbarConfig.message = `Не обрано жодного сертифiката!`;
              _this.snackbar = true;
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
            let grid = e.component,
                selected = (grid._options.selection.mode === 'multiple') ? `, Вибрано: ${grid.getSelectedRowKeys().length}` : '';

            this.certsCelected = grid.getSelectedRowKeys().length;

            grid.option('pager.infoText', `Всього: ${grid.option('dataSource').length}${selected}`);
          },
          onCellClick: (e) => {
            let grid = e.component,
                _this = this;

            function initialClick() {
              grid.clickCount = 1;
              grid.clickKey = e.key;
              grid.clickDate = new Date();
              _this.clickDelay = setTimeout(() => {
                if (e.column.dataField && e.column.dataField !== 'certificateNumber') {
                  if (e.row.isSelected) {
                    grid.deselectRows([e.key]);
                  }
                  else {
                    grid.selectRows([e.key], true);
                  }
                }
              }, 300);
            }

            function doubleClick() {
              clearTimeout(_this.clickDelay);
              grid.clickCount = 0;
              grid.clickKey = 0;
              grid.clickDate = null;

              if (e.column.dataField && e.data.status === 'Чернетка') {
                _this.showCertFormModal(e.data.certificateId)
              } else if (e.column.dataField && e.data.status !== 'Чернетка') {
                _this.snackbarConfig.icon = 'mdi-alert-circle';
                _this.snackbarConfig.color = 'warning';
                _this.snackbarConfig.message = `Дозволено редагувати тiльки сертифiкати з статусом "Чернетка"!`;
                _this.snackbar = true;
              }
            }

            if ((!grid.clickCount) || (grid.clickCount != 1) || (grid.clickKey != e.key) ) {
              initialClick();
            }
            else if (grid.clickKey == e.key) {
              if (((new Date()) - grid.clickDate) <= 300) {
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
        },
      }
    },

    mounted() {
      this.loadOrganisation();
    },

    methods: {
      setRangeNumbers (directionId, startRange, endRange) {
        axios.post(`/mariner/api/ranger/`,
        {
          organisation_id: this.organisationId,
          direction_id: directionId,
          startRange: startRange,
          endRange: endRange
        })
          .then(res => {
            this.snackbarConfig.icon = 'mdi-check-circle';
            this.snackbarConfig.color = 'success';
            this.snackbarConfig.message = 'Номери присвоєно успiшно';
            this.snackbar = true;
          })
          .catch((err) => {
            console.log(err);
            this.snackbarConfig.icon = 'mdi-alert-circle';
            this.snackbarConfig.color = 'red';
            this.snackbarConfig.message = 'Помилка при присвоєннi!';
            this.snackbar = true;
          });
      },

      // TODO: Remove if don't needed
      close () {
        // console.log('Dialog closed')
      },

      loadOrganisation() {
        axios.get(`/mariner/api/organisations/${this.organisationId}`)
          .then(res => {
            let organisationInfo = res.data,
                directions = res.data.directions;

            this.organisationName = organisationInfo.organisation_name;

            this.directions = [];
            directions.forEach((direction) => {
              this.directions.push({
                directionId: direction.id,
                direction_title: direction.direction_title,
                rangeNumStart: null,
                rangeNumEnd: null
              });
            });
          })
          .catch((err) => {
            console.log(err);
          });
      },

      newTab(href) {
        let newTab = window.open(href, '_blank');

        newTab.focus();
      },

      exportGrid(isSelection, exportType) {
        let grid = this.$refs.certsOnReviewGrid.tableInstance;

        this.exportType = exportType;
        grid.exportToExcel((typeof isSelection === 'boolean') ? isSelection : false);
      },

      saveCert() {
        let formData = {
          first_name_en: this.$refs.certForm.first_name_en,
          last_name_en: this.$refs.certForm.last_name_en,
          last_name_ukr: this.$refs.certForm.last_name_ukr,
          first_name_ukr: this.$refs.certForm.first_name_ukr,
          second_name_ukr: this.$refs.certForm.second_name_ukr,
          born: this.$refs.certForm.resetFormatDate(this.$refs.certForm.born),
          inn: this.$refs.certForm.inn,
          date_of_issue: this.$refs.certForm.resetFormatDate(this.$refs.certForm.date_of_issue),
          valid_date: this.$refs.certForm.resetFormatDate(this.$refs.certForm.valid_date),
          training_direction: this.$refs.certForm.training_direction.value,
          form_number: this.$refs.certForm.form_number,
          certf_number: this.$refs.certForm.certf_number,
          status: this.$refs.certForm.status
        };

        axios({
          method: (this.certId === 0) ? 'POST' : 'PUT',
          url: `/mariner/api/certificates/${(this.certId === 0) ? '' : `${this.certId}/`}`,
          data: formData
        })
          .then(res => {
            this.loadGridData(true);
            this.certFormModal = false;

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
      },

      showCertFormModal(certId) {
        this.certId = certId;
        this.certFormModal = true;
        this.$nextTick(() => {
          this.$refs.certForm.loadFormData();
        });
      },

      gridInited() {
        this.loadGridData();
      },

      loadGridData(refresh = false) {
        axios.get(`/mariner/api/organisationCerts/${this.organisationId}`)
          .then(res => {
            let certs = res.data.certificates;

            this.dataSource = [];
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
                formNumber: cert.form_number,
                issueDate: cert.date_of_issue,
                specialty: cert.training_direction.direction_title,
                sailorId: cert.sailor.id,
                sailor: `${cert.sailor.last_name_ukr} ${cert.sailor.first_name_ukr}`,
                status: status,
              });
            });

            let grid = this.$refs.certsOnReviewGrid.tableInstance,
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
