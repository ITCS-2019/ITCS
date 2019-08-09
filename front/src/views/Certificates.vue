<!--TODO change certsGrid to grid-->
<!--TODO refactor gUserRole to vue data userRole-->
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
              <v-menu offset-y
              content-class="dropdown-menu"
              transition="slide-y-transition">
                <v-btn slot="activator"
                color="success"
                small>
                  <v-icon left>
                    mdi-printer
                  </v-icon>
                  <span class="font-weight-bold ml-1">
                    Друкувати
                  </span>
                </v-btn>
                <v-card>
                  <v-list dense>
                    <v-list-tile key="Table"
                    v-on:click="printGrid('certsGrid')">
                      <v-list-tile-title v-text="`Таблицю`"/>
                    </v-list-tile>
                    <v-list-tile key="Certificates"
                    v-on:click="e => exportGrid(true, 'PrintCerts')">
                      <v-list-tile-title v-text="`Обранi сертифiкати`"/>
                    </v-list-tile>
                  </v-list>
                </v-card>
              </v-menu>
            </div>

            <!--Grid btns row right side-->
            <div>
              <v-btn color="success" small :depressed="true"
              v-if="userRole !== 'Інспектор'"
              v-on:click="showCertFormModal(0)">
                <v-icon>
                  mdi-plus-box
                </v-icon>
                <span class="font-weight-bold ml-1">
                  Додати
                </span>
              </v-btn>
              <v-btn color="success" small :depressed="true"
              v-if="userRole !== 'Інспектор'"
              to="/mariner/app/import-certificate">
                <v-icon>
                  mdi-file-upload
                </v-icon>
                <span class="font-weight-bold ml-1">
                  Iмпортувати
                </span>
              </v-btn>
              <v-btn color="success"
              small
              v-if="certsCelected > 0"
              v-on:click="e => exportGrid(true, 'reqNumbers')">
                <v-icon>
                  mdi-download
                </v-icon>
                <span class="font-weight-bold ml-1">
                  Заява на номери
                </span>
              </v-btn>
              <v-btn color="success"
              small
              v-if="certsCelected > 0"
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
              v-if="certsCelected > 0"
              v-on:click="e => showModal('Видалити обранi сертифiкати?')"
              :depressed="true">
                <v-icon>
                  mdi-trash-can
                </v-icon>
                <span class="font-weight-bold ml-1">
                  Видалити
                </span>
              </v-btn>

              <v-menu offset-y
              content-class="dropdown-menu"
              transition="slide-y-transition">
                <v-btn slot="activator"
                color="success"
                class="v-btn--simple ma-0"
                simple small icon>
                  <v-icon>
                    mdi-settings
                  </v-icon>
                </v-btn>
                <v-card>
                  <v-list dense>
                    <v-list-tile key="saveTableConfig"
                    v-on:click="saveTableConfig()">
                      <v-list-tile-title v-text="`Зберегти конфiгурацiю таблицi`"/>
                    </v-list-tile>
                    <v-list-tile key="resetTableConfig"
                    v-on:click="resetTableConfig()">
                      <v-list-tile-title v-text="`Стандартна конфiгурацiя`"/>
                    </v-list-tile>
                  </v-list>
                </v-card>
              </v-menu>

            </div>
          </v-layout>

          <DxGrid :tableConfig="tableConfig"
          v-on:init="gridInited()"
          ref="certsGrid"/>
        </material-card>

        <!--Request for numbers blank-->
        <div id="pdf"></div>
        <div id="cert-pdf-wrap"></div>
        <RequestNumbersForm
        ref="reqNumForm"
        :certs="reqNumCerts">
        </RequestNumbersForm>
      </v-flex>
    </v-layout>

    <Loader :value="loader.show"
    :message="loader.message"
    :progressColor="loader.color">
    </Loader>

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

    <!--Modal dialog-->
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
  import Loader from '@/components/uiElements/Loader.vue'
  import RequestNumbersForm from '@/components/forms/RequestNumbersForm.vue'
  import jsPDF from 'jspdf'

  export default {
    components: {
      CertificateForm,
      RequestNumbersForm,
      Loader
    },

    data() {
      return {
        loader: {
          show: false,
          message: '',
          color: ''
        },
        reqNumCerts: [],
        userRole: gUserRole,
        certsCelected: 0,
        isSelectedCert: false,
        certId: 0,
        dialog: false,
        certFormModal: false,
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
            let certIDs = [],
                isAllIssued = true;

            if (rows.length > 0) {
              rows.forEach((row) => {
                certIDs.push(row.data.certificateId);
                if (row.data.status !== 'Видан') {
                  isAllIssued = false;
                }
              });

              if (this.exportType === 'PrintCerts') {
                this.saveCertPDF(certIDs);
              }
              else if (this.exportType === 'reqNumbers') {
                this.serializeReqNumGridData(certIDs, isAllIssued);
              }
              else {
                let element = document.createElement('a');

                element.setAttribute('href', `/mariner/api/exportToPrint/?exportType=${this.exportType}&certIDs=${certIDs.join(',')}`);
                element.setAttribute('target', '_blank');
                element.style.display = 'none';
                document.body.appendChild(element);
                element.click();
                document.body.removeChild(element);
              }
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
          onSelectionChanged: (e) => {
            let certsGrid = e.component,
                selected = (certsGrid._options.selection.mode === 'multiple') ? `, Вибрано: ${certsGrid.getSelectedRowKeys().length}` : '';

            this.certsCelected = certsGrid.getSelectedRowKeys().length;

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

              if (e.column.dataField
              && (e.data.status === 'Чернетка' || e.data.status === 'Видан' || e.data.status === 'Обробка')
              && gUserRole !== 'НТЗ') {
                _this.showCertFormModal(e.data.certificateId);
              } else if (e.column.dataField && e.data.status === 'Чернетка') {
                _this.showCertFormModal(e.data.certificateId);
              }
              else if (e.column.dataField) {
                _this.snackbarConfig.icon = 'mdi-alert-circle';
                _this.snackbarConfig.color = 'warning';
                _this.snackbarConfig.message = `Сертифiкати зi статусом "${e.data.status}" не можна редагувати!`;
                _this.snackbar = true;
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

    methods: {
      saveCertPDF(certIDs) {
        this.loader.show = true;
        this.loader.message = 'Формування файлiв..';
        this.loader.color = 'info';

        certIDs.forEach((id, i) => {
          axios.get(`/mariner/api/printCertificate/${id}/`)
            .then(res => {
              let element = document.createElement('div'),
                  PDFWrap = document.querySelector('#cert-pdf-wrap');

              element.innerHTML = res.data.split('<body>')[1].split('</body>')[0];

              PDFWrap.appendChild(element);

              html2canvas(PDFWrap.querySelector('#pdf-content'),
              {
                imageTimeout: 5000,
                useCORS: true
              })
                .then(canvas => {
                  document.getElementById('pdf').appendChild(canvas);
                  let img = canvas.toDataURL('image/png', 1.0);
                  let pdf = new jsPDF('portrait', 'mm', 'a6', true);
                  pdf.addImage(img, 'JPEG', 0, 0, 105, 296, undefined, 'FAST');
                  pdf.addPage();
                  pdf.addImage(img, 'JPEG', 0, -148, 105, 296, undefined, 'FAST');

                  if (i === (certIDs.length - 1))
                    this.loader.show = false;

                  pdf.save(`cert_${id}.pdf`);
                  document.getElementById('pdf').innerHTML = '';
                });
              PDFWrap.removeChild(element);
            })
            .catch((err) => {
              console.log(err);
            });
        });
      },

      serializeReqNumGridData(certIDs, isAllIssued = true) {
        this.reqNumCerts = [];

        if (isAllIssued) {
          certIDs.forEach((certID) => {
            let cert = this.dataSource.find(row => {
              return certID === row.certificateId
            });

            this.reqNumCerts.push(cert);
          });

          this.$refs.reqNumForm.updateGrid();
        }
        else {
          this.snackbarConfig.icon = 'mdi-alert-circle';
          this.snackbarConfig.color = 'red';
          this.snackbarConfig.message = 'Заявку на номери можна сформувати тiльки для виданих сертифiкатiв!';
          this.snackbar = true;
        }
      },

      resetTableConfig() {
        localStorage.removeItem('certGridConfig');
        this.snackbarConfig.icon = 'mdi-check-circle';
        this.snackbarConfig.color = 'success';
        this.snackbarConfig.message = 'Застосована стандартна конфiгурацiя таблицi!';
        this.snackbar = true;
      },

      saveTableConfig() {
        let grid = this.$refs.certsGrid.tableInstance,
            cols = grid._options.columns,
            certGridConfig = [];

        cols.forEach((col, i) => {
          certGridConfig.push({
            index: i,
            width: (grid.columnOption(col.dataField, 'width')) ? grid.columnOption(col.dataField, 'width') : false,
            sortOrder: (grid.columnOption(i, 'sortOrder')) ? grid.columnOption(i, 'sortOrder') : false
          });
        });

        localStorage.setItem('certGridConfig', JSON.stringify(certGridConfig));
        this.snackbarConfig.icon = 'mdi-check-circle';
        this.snackbarConfig.color = 'success';
        this.snackbarConfig.message = 'Конфiгурацiя таблицi збережена!';
        this.snackbar = true;
      },

      gridInited() {
        let grid = this.$refs.certsGrid.tableInstance;

        this.loadGridData();

        if (this.$route.params.columns) {
          let columns = this.$route.params.columns;

          columns.forEach((column) => {
            grid.beginUpdate();
            grid.columnOption(column.dataField, 'filterValue', column.filterValue);
            grid.endUpdate();
          });
        }

        if (localStorage.getItem('certGridConfig')) {
          let gridConfig = JSON.parse(localStorage.getItem('certGridConfig'));

          gridConfig.forEach((col) => {
            grid.columnOption(col.index, 'width', (col.width) ? col.width : undefined);
            grid.columnOption(col.index, 'sortOrder', (col.sortOrder) ? col.sortOrder : undefined);
          });
        }
      },

      loadGridData(refresh = false) {
        axios.get(`/mariner/api/tableCertificates/`)
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
                direction_level: cert.direction_level,
                direction_allow_functions: cert.direction_allow_functions,
                born: cert.born,
                certificateId: cert.id,
                certificateNumber: cert.certf_number,
                blankNumber: cert.form_number,
                issueDate: cert.date_of_issue,
                validDate: cert.valid_date,
                trainingDirection: cert.direction_title_cert,
                sailorId: cert.sailor_id,
                sailor: `${cert.first_name_ukr} ${cert.last_name_ukr}`,
                trainigOrganisation: cert.organisation_name_cert,
                status: status
              });
            });

            let certsGrid = this.$refs.certsGrid.tableInstance,
                selected = (certsGrid._options.selection.mode === 'multiple') ? `, Вибрано: ${certsGrid.getSelectedRowKeys().length}` : '';

            this.certsCelected = certsGrid.getSelectedRowKeys().length;
            certsGrid.option('dataSource', this.dataSource);
            certsGrid.option('pager.infoText', `Всього: ${certsGrid.option('dataSource').length}${selected}`);
            certsGrid.endCustomLoading();

            if (refresh) {
              certsGrid.refresh();
            }
          })
          .catch((err) => {
            console.log(err);
          });
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


        let formData2 = new FormData();

        formData2.append('first_name_en', this.$refs.certForm.first_name_en);
        formData2.append('last_name_en', this.$refs.certForm.last_name_en);
        formData2.append('last_name_ukr', this.$refs.certForm.last_name_ukr);
        formData2.append('first_name_ukr', this.$refs.certForm.first_name_ukr);
        formData2.append('second_name_ukr', this.$refs.certForm.second_name_ukr);
        formData2.append('born', this.$refs.certForm.resetFormatDate(this.$refs.certForm.born));
        formData2.append('sailorPhoto', this.$refs.certForm.logo.logo_pic);


        // let formData2 = {
        //   first_name_en: this.$refs.certForm.first_name_en,
        //   last_name_en: this.$refs.certForm.last_name_en,
        //   last_name_ukr: this.$refs.certForm.last_name_ukr,
        //   first_name_ukr: this.$refs.certForm.first_name_ukr,
        //   second_name_ukr: this.$refs.certForm.second_name_ukr,
        //   born: this.$refs.certForm.resetFormatDate(this.$refs.certForm.born),
        //   sailorPhoto: this.$refs.certForm.logo.logo_pic
        // };

        // console.log(formData2);

        axios({
          method: 'POST',
          url: `/mariner/api/uploadSailorPhoto/`,
          data: formData2,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
          .then(res => {
            console.log(res);
          })
          .catch((err) => {
            console.log(err);
          });






        if (gUserRole !== 'НТЗ') {
          formData['trainigOrganisation'] = this.$refs.certForm.training_organisation.value;
        }

        // axios({
        //   method: (this.certId === 0) ? 'POST' : 'PUT',
        //   url: `/mariner/api/certificates/${(this.certId === 0) ? '' : `${this.certId}/`}`,
        //   data: formData
        // })
        //   .then(res => {
        //     this.loadGridData(true);
        //     this.certFormModal = false;
        //
        //     this.snackbarConfig.icon = 'mdi-check-circle';
        //     this.snackbarConfig.color = 'success';
        //     this.snackbarConfig.message = (this.certId === 0)
        //                                     ? 'Сертифiкат успiшно створено!'
        //                                     : 'Сертифiкат успiшно вiдредаговано!';
        //     this.snackbar = true;
        //   })
        //   .catch((err) => {
        //     console.log(err);
        //   });
      },

      showCertFormModal(certId) {
        this.certId = certId;
        this.certFormModal = true;
        this.$nextTick(() => {
          this.$refs.certForm.loadFormData();
        });
      },

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
            grid = $grid = this.$refs[`${gridRef}`].tableInstance,
            mywindow = window.open('', 'PRINT', 'height=400,width=600');

        let printTable = `<table style="width: 100%; border-collapse: collapse;"><tr>`,
            cols = grid._options.columns,
            rows = grid.getVisibleRows();

        cols.forEach((col) => {
          if (col.visible !== false)
            printTable += `<th style="border: 1px solid black;">${col.caption}</th>`
        });

        printTable += '</tr>';

        rows.forEach((row) => {
          let cells = row.cells;

          printTable += '<tr>';
          cells.forEach((cell) => {
            if (cell.displayValue !== false)
              printTable += `<td style="border: 1px solid black; padding: 5px; font-size: 12px">${(cell.text === '') ? ' ' : cell.text}</td>`
          });
          printTable += '</tr>';
        });

        printTable += '</table>';

        mywindow.document.write('<html><head><title>' + document.title  + '</title>');
        mywindow.document.write('</head><body>');
        mywindow.document.write('<h1>' + document.title  + '</h1>');
        mywindow.document.write(printTable);
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