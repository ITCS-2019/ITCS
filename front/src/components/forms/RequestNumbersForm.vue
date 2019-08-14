<template>
  <div id="req-num-form"
  class="c-pdf-a4"
  v-if="downloadingFile">
    <div class="c-pdf-a4__row c-pdf-a4__row--flex c-pdf-a4__row--justify-end">
      <div class="c-pdf-a4__row-block c-pdf-a4__row-block--align-right">
        <div class="c-pdf-a4__text">
          Додаток №01
        </div>
        <div class="c-pdf-a4__text">
          До договору №___/{{currYear}}-НТЗ
        </div>
        <div class="c-pdf-a4__text">
          про надання послуг з реєстрації документів моряків України
        </div>
        <div class="c-pdf-a4__text">
          та їх внесення у Єдиний державний реєстр документів моряків
        </div>
        <div class="c-pdf-a4__text">
          від &laquo;___&raquo; _____________ {{currYear}} р.
        </div>
      </div>
    </div>
    <div class="c-pdf-a4__row c-pdf-a4__row--margin-top-35 c-pdf-a4__row--flex c-pdf-a4__row--justify-center">
      <div class="c-pdf-a4__row-block">
        <div class="c-pdf-a4__text c-pdf-a4__text--align-center c-pdf-a4__text--italic c-pdf-a4__text--font-weight-700">
          <b>
            На бланку Замовника
          </b>
        </div>
      </div>
    </div>
    <div class="c-pdf-a4__row c-pdf-a4__row--margin-top-20">
      <div class="c-pdf-a4__text">
        Вих. № ________________________
      </div>
      <div class="c-pdf-a4__text">
        вiд ___________________________
      </div>
    </div>
    <div class="c-pdf-a4__row c-pdf-a4__row--margin-top-12 c-pdf-a4__row--flex c-pdf-a4__row--justify-end">
      <div class="c-pdf-a4__row-block c-pdf-a4__row-block--align-right">
        <div class="c-pdf-a4__text c-pdf-a4__text--italic c-pdf-a4__text--font-weight-700">
          <b>
            Iнспекції з питань підготовки та
          </b>
        </div>
        <div class="c-pdf-a4__text c-pdf-a4__text--italic c-pdf-a4__text--font-weight-700">
          <b>
            дипломування моряків
          </b>
        </div>
      </div>
    </div>
    <div class="c-pdf-a4__row c-pdf-a4__row--margin-top-12">
      <div class="c-pdf-a4__text">
        Відповідно до договору № _______________ -НТЗ від_________ р. просимо нaдати реєстраційний номер для
        подальшого внесення до єдиного Державного реєстру документів моряків інформацію про свідоцтва (сертифікати),
        які видаються
      </div>
      <br>
      <div class="c-pdf-a4__text c-pdf-a4__text--font-weight-700 c-pdf-a4__text--align-center">
        <b>
          {{trainingOrganisation}}
        </b>
      </div>
      <hr>
      <div class="c-pdf-a4__text c-pdf-a4__text--italic c-pdf-a4__text--align-center">
        <sup>
          (назва НТЗ або його вiдокремленного пiдроздiлу)
        </sup>
      </div>
      <div class="c-pdf-a4__text c-pdf-a4__text--margin-top-10">
        Після закінчення відповідних курсів відповідно до даних таблиці 1:
      </div>
      <div class="c-pdf-a4__text c-pdf-a4__text--margin-top-10 c-pdf-a4__text--font-weight-700 c-pdf-a4__text--align-right">
        <b>
          Таблиця 1
        </b>
      </div>
      <table class="c-table c-table--margin-top-24">
        <tr>
          <th class="c-table__cell">
            №
          </th>
          <th class="c-table__cell">
            ПIБ, дата народження
          </th>
          <th class="c-table__cell">
            Напрямок навчання
          </th>
          <th class="c-table__cell">
            Рiвень квалiфiкацiї
          </th>
          <th class="c-table__cell">
            Дозволенi рiвнi функцiй
          </th>
          <th class="c-table__cell">
            № бланку або внутрiшньої реєстрації
          </th>
          <th class="c-table__cell">
            Дата початку курсу
          </th>
          <th class="c-table__cell">
            Дата закiнення курсу
          </th>
          <th class="c-table__cell">
            Дата видачi
          </th>
          <th class="c-table__cell">
            Дiйсний до
          </th>
        </tr>
        <tr v-for="(cert, i) in reqCerts">
          <td class="c-table__cell c-table__cell--font-size-9">
            {{i + 1}}
          </td>
          <td class="c-table__cell c-table__cell--font-size-9">
            {{cert.sailor}}
            <br>
            {{formatDate(cert.born)}}
          </td>
          <td class="c-table__cell c-table__cell--font-size-9">
            {{cert.trainingDirection}}
          </td>
          <td class="c-table__cell c-table__cell--font-size-9">
            {{cert.direction_level}}
          </td>
          <td class="c-table__cell c-table__cell--font-size-9">
            {{cert.direction_allow_functions}}
          </td>
          <td class="c-table__cell c-table__cell--font-size-9">
            {{(cert.blankNumber) ? cert.blankNumber : '---'}}
          </td>
          <td class="c-table__cell c-table__cell--font-size-9">

          </td>
          <td class="c-table__cell c-table__cell--font-size-9">

          </td>
          <td class="c-table__cell c-table__cell--font-size-9">
            {{formatDate(cert.issueDate)}}
          </td>
          <td class="c-table__cell c-table__cell--font-size-9">
            {{formatDate(cert.validDate)}}
          </td>
        </tr>
      </table>
      <div class="c-pdf-a4__text c-pdf-a4__text--margin-top-24">
        Оплату гарантуемо у встановлений Договором строк.
      </div>
    </div>
    <br><br><br>
    <div class="c-pdf-a4__row">
      <table style="border: none;">
        <tr>
          <td style="text-align: center; border: none; border-top: 1px solid black;">
            <b>
              Посада
            </b>
          </td>
          <td style="text-align: center; border: none; border-top: 1px solid black;">
            <b>
              Пiдпис
            </b>
          </td>
          <td style="text-align: center; border: none; border-top: 1px solid black;">
            <b>
              П.I.Б.
            </b>
          </td>
        </tr>
      </table>
    </div>
    <br><br>
    <div class="c-pdf-a4__row">
      <table style="border: none;">
        <tr>
          <td style="text-align: center; border: none; border-top: 1px solid black;">
            <b>
              Вiд замовника
            </b>
          </td>
          <td style="text-align: center; border: none; border-top: 1px solid black;">
            <b>
              Вiд виконавця
            </b>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>

  import jsPDF from 'jspdf'

  export default {
    name: 'RequestNumbers',

    props: {
      certs: {
        type: Array,
        required: true
      }
    },

    data() {
      return {
        currYear: null,
        reqCerts: [],
        downloadingFile: false,
        trainingOrganisation: null
      }
    },

    mounted() {
      this.currYear = new Date().getFullYear();
    },

    methods: {
      updateGrid() {
        this.$nextTick(() => {
          this.reqCerts = this.certs;

          axios.get(`/mariner/api/organisations/`)
            .then(res => {
              this.trainingOrganisation = res.data.organisations.organisation_name;
              this.downloadFile();
            })
            .catch((err) => {
              console.log(err);
            });
        });

      },

      downloadFile() {
        this.downloadingFile = true;

        this.$nextTick(() => {
          let pageStyles = `.c-table {width: 100%;border-collapse: collapse;}.c-table.c-table--margin-top-24 {margin-top: 24px;}.c-table__cell {border: 1px solid black;text-align: center;font-size: 11px;padding: 0px 5px;}.c-table__cell.c-table__cell--font-size-9 {font-size: 9px;}.c-pdf-a4 {width: 210mm;min-height: 297mm;position: relative;background: white;}.c-pdf-a4__row.c-pdf-a4__row--flex {display: flex;flex-direction: row;flex-wrap: wrap;align-content: flex-start;align-items: flex-start;justify-content: flex-start;}.c-pdf-a4__row.c-pdf-a4__row--justify-end {justify-content: flex-end;}.c-pdf-a4__row.c-pdf-a4__row--justify-center {justify-content: center;}.c-pdf-a4__row.c-pdf-a4__row--justify-space-between {justify-content: space-between;}.c-pdf-a4__row.c-pdf-a4__row--margin-top-35 {margin-top: 35px;}.c-pdf-a4__row.c-pdf-a4__row--margin-top-55 {margin-top: 55px;}.c-pdf-a4__row.c-pdf-a4__row--margin-top-20 {margin-top: 20px;}.c-pdf-a4__row.c-pdf-a4__row--margin-top-12 {margin-top: 12px;}.c-pdf-a4__row.c-pdf-a4__row--bottom-footer {position: absolute;left: 15px;width: calc(100% - 30px);bottom: 0px;}.c-pdf-a4__row-block.c-pdf-a4__row-block--align-right {text-align: right;}.c-pdf-a4__row-block.c-pdf-a4__row-block--flex-1 {width: 20%;display: inline-block;color: red;}.c-pdf-a4__row-block.c-pdf-a4__row-block--margin-left-20 {margin-left: 20px;}.c-pdf-a4__text {font-size: 14px;}.c-pdf-a4__text.c-pdf-a4__text--italic {font-style: italic;}.c-pdf-a4__text.c-pdf-a4__text--font-weight-700 {font-weight: 700;}.c-pdf-a4__text.c-pdf-a4__text--font-size-20 {font-size: 20px;}.c-pdf-a4__text.c-pdf-a4__text--align-center {text-align: center;}.c-pdf-a4__text.c-pdf-a4__text--align-right {text-align: right;}.c-pdf-a4__text.c-pdf-a4__text--margin-top-24 {margin-top: 24px;}.c-pdf-a4__text.c-pdf-a4__text--margin-top-10 {margin-top: 10px;}.c-pdf-a4__text.c-pdf-a4__text--inline {display: inline-block;width: 40%;text-align: center;}`;

          var header = "<html xmlns:o='urn:schemas-microsoft-com:office:office' "+
                  "xmlns:w='urn:schemas-microsoft-com:office:word' "+
                  "xmlns='http://www.w3.org/TR/REC-html40'>"+
                  `<head><meta charset='utf-8'><title>Заява на номери</title><style>${pageStyles}</style></head><body>`;
          var footer = "</body></html>";
          var sourceHTML = header+document.getElementById("req-num-form").innerHTML+footer;

          var source = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(sourceHTML);
          var fileDownload = document.createElement('a');
          document.body.appendChild(fileDownload);
          fileDownload.href = source;
          fileDownload.download = 'request_certs_num_form.doc';
          fileDownload.click();
          document.body.removeChild(fileDownload);
        });
      },

      formatDate(date) {
        if (!date) return null

        const [year, month, day] = date.split('-')
        return `${day}.${month}.${year}`
      }
    }
  }
</script>