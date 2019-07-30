<template>
    <v-layout justify-center wrap>
      <v-flex md12>
        <DxGrid :tableConfig="tableConfig"
        :pagination="false"
        v-on:init="gridInited()"
        ref="requestNumGrid"/>
      </v-flex>
    </v-layout>
</template>

<script>

  export default {
    name: 'RequestNumbers',

    data() {
      return {
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
      gridInited() {

      }
    }
  }
</script>
