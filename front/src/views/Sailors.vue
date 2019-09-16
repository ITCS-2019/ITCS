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
          ref="sailorsGrid"/>
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

    <!--Sailor form modal-->
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
        onSelectionChanged: function(e) {
          let grid = e.component,
              selected = (grid._options.selection.mode === 'multiple') ? `, Вибрано: ${grid.getSelectedRowKeys().length}` : '';

          grid.option('pager.infoText', `Всього: ${grid.option('dataSource').length}${selected}`);
        },
        onCellClick: function (e) {
          // if (e.column.dataField) {
          //   window.location.replace(`/mariner/sailor/${e.data.id}`);
          // }
        },
        onRowClick: function (e) {
          let component = e.component;

          function initialClick() {
            component.clickCount = 1;
            component.clickKey = e.key;
            component.clickDate = new Date();
          }

          function doubleClick() {
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
            dataField: 'id',
            visible: false
          },
          {
            dataField: 'pib',
            caption: 'ПIБ',
            allowEditing: false,
            allowFiltering: false,
            cellTemplate: function(element, data) {
              element.append(`<div style="white-space: nowrap;">
                                            ${data.value.first_name_ukr} ${data.value.second_name_ukr} ${data.value.last_name_ukr}
                                        </div>
                                        <div style="white-space: nowrap;">
                                            ${data.value.first_name_en} ${data.value.last_name_en}
                                        </div>`);
            }
          },
          {
            dataField: 'sex',
            caption: 'Стать',
            allowEditing: false,
            allowFiltering: true,
            alignment: 'left'
          },
          {
            dataField: 'born',
            caption: 'Дата народження',
            dataType: 'date',
            allowEditing: false,
            format: 'dd.MM.yyyy',
          },
          {
            dataField: 'inn',
            caption: 'ИНН',
            allowEditing: false,
            allowFiltering: true
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
        passport_serie: this.$refs.sailorForm.passport_serie,
        passport_number: this.$refs.sailorForm.passport_number,
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
      let grid = this.$refs.sailorsGrid.tableInstance;

      this.loadGridData();

      if (this.$route.params.columns) {
        let columns = this.$route.params.columns;

        columns.forEach((column) => {
          grid.beginUpdate();
          grid.columnOption(column.dataField, 'filterValue', column.filterValue);
          grid.endUpdate();
        });
      }
    },

    loadGridData(refresh = false) {
      axios.get(`/mariner/api/sailors/`)
        .then(res => {
          let sailors = res.data;

          this.dataSource = [];
          sailors.forEach((sailor) => {
            this.dataSource.push({
              id: sailor.id,
              pib: {
                first_name_ukr: sailor.first_name_ukr,
                second_name_ukr: sailor.second_name_ukr,
                last_name_ukr: sailor.last_name_ukr,
                first_name_en: sailor.first_name_en,
                last_name_en: sailor.last_name_en,
              },
              sex: (sailor.sex === 0) ? 'Чол.' : 'Жiн.',
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
