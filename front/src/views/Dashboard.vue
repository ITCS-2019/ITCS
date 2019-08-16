<template>
  <v-container
    fill-height
    fluid
    grid-list-xl
  >
    <v-layout wrap>
      <v-flex v-bind:lg4="(role === 'Адміністратор' || role === 'Інспектор') ? true : false"
      v-bind:lg6="role === 'НТЗ' ? true : false"
      sm12>
        <material-card color="green"
        class="pb-4"
        title="Напрямки Підготовки">
          <v-layout nowrap
          class="mt-2 pl-2 pr-2">
            <v-flex md12>
              <router-link to="/mariner/app/training-directions"
              class="c-link">
                <span class="font-weight-bold black--text">
                  Кількість Напрямків
                </span>
                <span class="font-weight-bold black--text">
                  - {{directionsCount}}
                </span>
              </router-link>
            </v-flex>
          </v-layout>
        </material-card>
      </v-flex>
      <v-flex v-bind:lg4="(role === 'Адміністратор' || role === 'Інспектор') ? true : false"
      v-bind:lg6="role === 'НТЗ' ? true : false"
      sm12
      v-if="role === 'Адміністратор' || role === 'Інспектор'">
        <material-card color="green"
        class="pb-4"
        title="НТЗ">
          <v-layout nowrap
          class="mt-2 pl-2 pr-2">
            <v-flex md12>
              <router-link to="/mariner/app/training-directions"
              class="c-link">
                <span class="font-weight-bold black--text">
                  Кількість НТЗ
                </span>
                <span class="font-weight-bold black--text">
                  - {{organisationsCount}}
                </span>
              </router-link>
            </v-flex>
          </v-layout>
        </material-card>
      </v-flex>
      <v-flex v-bind:lg4="(role === 'Адміністратор' || role === 'Інспектор') ? true : false"
      v-bind:lg6="role === 'НТЗ' ? true : false"
      sm12>
        <material-card color="green"
        class="pb-4"
        title="Сертифікати">
          <v-layout wrap
          class="mt-2 pl-2 pr-2">
            <v-flex md12>
              <router-link class="c-link"
              :to="{name: 'Certificates',
              params: {
                columns: [
                  {
                    dataField: 'status',
                    filterValue: 'Обробка'
                  }
                ]
              }}">
                <span class="font-weight-bold black--text">
                  Cертіфікатів в обробці
                </span>
                <span class="font-weight-bold black--text">
                  - {{certsInReviewCount}},
                </span>
              </router-link>
            </v-flex>
            <v-flex md12>
              <router-link class="c-link"
              :to="{name: 'Certificates',
                params: {
                  columns: [
                    {
                      dataField: 'status',
                      filterValue: 'Видан'
                    }
                  ]
                }
              }">
                <span class="font-weight-bold black--text">
                  Виданих сертіфікатів
                </span>
                <span class="font-weight-bold black--text">
                  - {{issuedCertCount}}
                </span>
              </router-link>
            </v-flex>
          </v-layout>
        </material-card>
      </v-flex>

      <v-flex md12
      v-if="role !== 'НТЗ'">
        <material-card>
          <DxGrid :tableConfig="tableConfig"
          v-on:init="gridInited()"
          ref="certsOnAproveGrid"/>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      issuedCertCount: 0,
      certsInReviewCount: 0,
      organisationsCount: 0,
      directionsCount: 0,
      role: gUserRole,
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
        hoverStateEnabled: true,
        rowAlternationEnabled: true,
        onCellClick: (e) => {
          if (e.column.dataField === 'ntz') {
            window.vue.$router.push(`/mariner/app/training-organisations/${e.data.id}`);
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
            dataField: 'ntz',
            caption: 'НТЗ',
            allowEditing: true
          },
          {
            dataField: 'certificatesAmount',
            caption: 'До видачі',
            width: 200,
            allowEditing: false

          }
        ]
      }
    }
  },

  mounted() {

    // TODO: Make one request for all info
    axios.get(`/mariner/api/dashInfo/`)
      .then(res => {
        let dashInfo = res.data.dashInfo[0];

        if (this.role === 'Адміністратор') {
          this.organisationsCount = dashInfo.trainigOrganisations.length;
        }

        this.directionsCount = dashInfo.trainigDirectionsCount;
        this.certsInReviewCount = dashInfo.certsInReviewCount;
        this.issuedCertCount = dashInfo.certCount;
      })
      .catch((err) => {
        console.log(err);
      });
  },

  methods: {
    gridInited() {

      // TODO: Use this request for all info
      axios.get(`/mariner/api/dashInfoStat/`)
        .then(res => {
          let grid = this.$refs.certsOnAproveGrid.tableInstance,
              organisations = res.data.dashInfo[0].trainigOrganisations;

          this.dataSource = [];
          organisations.forEach((organisation) => {
            this.dataSource.push({
              id: organisation.id,
              certificatesAmount: organisation.organisation_allCertsInReviewCount,
              ntz: organisation.organisation_name
            })
          });

          let selected = (grid._options.selection.mode === 'multiple') ? `, Вибрано: ${grid.getSelectedRowKeys().length}` : '';

          grid.option('dataSource', this.dataSource);
          grid.option('pager.infoText', `Всього: ${grid.option('dataSource').length}${selected}`);
          grid.endCustomLoading();
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }
}
</script>
