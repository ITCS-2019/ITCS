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
              v-if="userRole === 'Адміністратор'">
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
          ref="usersGrid"/>
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
      userRole: gUserRole,
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
        selection: {
          mode: "multiple",
          showCheckBoxesMode: 'always'
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

          grid.option('pager.infoText', `Всього: ${grid.option('dataSource').length}${selected}`);
        },
        onCellClick: function (e) {
            let grid = e.component,
                _this = this;

            function initialClick() {
                grid.clickCount = 1;
                grid.clickKey = e.key;
                grid.clickDate = new Date();
                _this.clickDelay = setTimeout(() => {
                    if (e.column.dataField) {
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
            dataField: 'username',
            caption: 'Логiн',
            allowEditing: false,
            allowFiltering: true,
          },
          {
            dataField: 'full_name',
            caption: 'ПIБ',
            allowEditing: false,
            allowFiltering: true,
          },
          {
            dataField: 'organization_name',
            caption: 'Органiзацiя',
            allowEditing: false,
            allowFiltering: true,
          },
          {
            dataField: 'is_active',
            caption: 'Активний',
            allowEditing: false,
            allowFiltering: true,
          }
        ]
      }
    }
  },

  methods: {
    loadGridData(refresh = false) {
      axios.get(`/mariner/api/users/`)
        .then(res => {
          let users = res.data.users;

          this.dataSource = [];
          users.forEach((user) => {
            this.dataSource.push({
              id: user.id,
              username: user.username,
              full_name: user.full_name,
              organization_name: user.profile.organization_name,
              is_active: (user.is_active) ? 'Так' : 'Нi'
            });
          });

          let grid = this.$refs.usersGrid.tableInstance,
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
        direction_title_eng: this.$refs.directionForm.direction_title_eng,
        price_id: this.$refs.directionForm.price_id,
        level: this.$refs.directionForm.level,
        allow_functions: this.$refs.directionForm.allow_functions,
        regulationInfo: this.$refs.directionForm.regulationInfo,
        regulationInfoEng: this.$refs.directionForm.regulationInfoEng,
        courseInfo: this.$refs.directionForm.courseInfo,
        courseInfoEng: this.$refs.directionForm.courseInfoEng,
        inspectionInfo: this.$refs.directionForm.inspectionInfo,
        inspectionInfoEng: this.$refs.directionForm.inspectionInfoEng,
        infoText: this.$refs.directionForm.infoText,
        infoTextEng: this.$refs.directionForm.infoTextEng
      };

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
