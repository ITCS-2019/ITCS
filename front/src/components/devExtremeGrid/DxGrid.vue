<template>
    <div>
        <div class="custom-pagination custom-pagination--grid" style="display: none;">
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
        <div id="dev-extreme-grid"></div>
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
        }
    },
    data(){
        return {
            tableInstance: null
        }
    },
    mounted(){
        var _this = this
        $(function(){
            // DevExpress.localization.locale('ru');
            DevExpress.localization.loadMessages(ukMessages);
            DevExpress.localization.locale('ru-RU');
            _this.$nextTick(() => {
                _this.tableInstance = $('#dev-extreme-grid').dxDataGrid(_this.tableConfig).dxDataGrid('instance');
                _this.tableInstance.beginCustomLoading();
                _this.$emit('init')
            })
        });
    }
}
</script>
