<template>
    <div id="dev-extreme-grid"></div>
</template>

<script>
window.$ = window.jQuery = require('jquery')
require('devextreme/dist/js/dx.all.js')

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
    created(){

    },
    mounted(){
        var _this = this
        $(function(){
            DevExpress.localization.locale('ru');
            _this.$nextTick(()=>{
                _this.tableInstance = $('#dev-extreme-grid').dxDataGrid(_this.tableConfig).dxDataGrid('instance');
            })
        });
    }
}
</script>
