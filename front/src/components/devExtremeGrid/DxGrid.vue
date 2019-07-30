<template>
    <div>
        <div class="custom-pagination custom-pagination--grid" style="display: none;"
        v-if="showPagination">
            <button class="custom-pagination__btn custom-pagination__btn--first-page">
                Перша
            </button>
            <button class="custom-pagination__btn custom-pagination__btn--prev">
                &laquo;
            </button>
            <select name="certificates-select" class="custom-pagination__select">
            </select>
            <button class="custom-pagination__btn custom-pagination__btn--next">
                &raquo;
            </button>
            <button class="custom-pagination__btn custom-pagination__btn--last-page">
                Остання
            </button>
        </div>
        <div :id="`${gridID}`" class="dx-selection-disabled"></div>
    </div>
</template>

<script>
window.$ = window.jQuery = require('jquery')
window.JSZip = require('jszip')
require('devextreme/dist/js/dx.all.js')
import ukMessages from '@/components/devExtremeGrid/uk.json'

export default {
    name: 'DxGrid',
    props: {
        tableConfig: {
            type: Object,
            required: false,
            default: () => {}
        },
        pagination: {
          type: Boolean,
          required: false,
          default: true
        },
        id: {
          type: String,
          required: false,
          default: 'dev-extreme-grid'
        }
    },
    data(){
        return {
            tableInstance: null,
            showPagination: true,
            gridID: 'dev-extreme-grid'
        }
    },
    mounted() {
        this.showPagination = this.pagination;
        this.gridID = this.id;

        var _this = this;
        $(function(){
            DevExpress.localization.loadMessages(ukMessages);
            DevExpress.localization.locale('ru-RU');
            _this.$nextTick(() => {
                _this.tableInstance = $(`#${_this.gridID}`).dxDataGrid(_this.tableConfig).dxDataGrid('instance');
                _this.tableInstance.beginCustomLoading();
                _this.$emit('init')
            })
        });
    }
}
</script>
