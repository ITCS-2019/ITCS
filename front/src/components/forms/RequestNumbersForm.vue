<template>
  <div id="req-num-form"
  class="c-pdf-a4"
  v-if="downloadingPdf">
    <div id="pdf"></div>
    <v-flex md12 class="text-md-right">
      <div class="body-2">
        Додаток №01
      </div>
      <div class="body-2">
        До договору №___/{{currYear}}-НТЗ
      </div>
      <div class="body-2">
        про наданпя послуг з реєстрації докумснтів моряків Україи
      </div>
      <div class="body-2">
        та їх внсссиня у Єдииий державиий реєстр докумеитів моряків
      </div>
      <div class="body-2">
        від &laquo;___&raquo; _____________ {{currYear}} р.
      </div>
    </v-flex>
    <v-flex md12 class="text-md-center mt-4">
      <div class="body-1 font-italic font-weight-bold">
        На блаику Замовиика
      </div>
    </v-flex>
    <v-flex md12 class="text-md-left mt-2">
      <div class="body-2">
        Вих. № ________________________
      </div>
      <div class="body-2">
        вiд ___________________________
      </div>
    </v-flex>
    <v-flex md12 class="text-md-right">
      <div class="body-1 font-italic font-weight-bold">
        Iнспекції з питаиь підготовки та
      </div>
      <div class="body-1 font-italic font-weight-bold">
        дипломуваиия моряків
      </div>
    </v-flex>
    <v-flex md12 class="text-md-left">
      <div class="body-2" id="loh">
        Відповідно до договору № _______________ -НТЗ від_________ р. просимо нaдати реєстраційний номер для
        подальшого внесения до єдиного Державного реєстру документів моряків інформацію про свідоцтва (сертифікати),
        які видаються
      </div>
      <div class="body-2">
        &nbsp;
      </div>
      <hr>
      <div class="body-2 font-italic text-md-center">
        <sup>
          (назва НТЗ або його вiдокремленного пiдроздiлу)
        </sup>
      </div>
      <div class="body-2">
        Після закінчення відповідних курсів відповідно до даних таблиці 1:
      </div>
      <div class="body-2 font-weight-bold text-md-right">
        Таблиця 1
      </div>
      <table class="c-table mt-4">
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
      <div class="body-2 text-md-left mt-4">
        Оплату гарантуемо у встановлений Договором строк.
      </div>
    </v-flex>
    <v-layout justify-space-between
    wrap
    class="mt-4">
      <v-flex md4 class="text-md-left">
        <div class="body-2">
          &nbsp;
        </div>
        <hr>
        <div class="title text-md-center mt-1">
          <sup>
            Посада
          </sup>
        </div>
      </v-flex>
      <v-flex md4 class="text-md-left">
        <div class="body-2">
          &nbsp;
        </div>
        <hr>
        <div class="title text-md-center mt-1">
          <sup>
            Пiдпис
          </sup>
        </div>
      </v-flex>
      <v-flex md4 class="text-md-left">
        <div class="body-2">
          &nbsp;
        </div>
        <hr>
        <div class="title text-md-center mt-1">
          <sup>
            П.I.Б.
          </sup>
        </div>
      </v-flex>
    </v-layout>
    <v-layout class="c-bottom-footer">
      <v-flex md6 class="text-md-left">
        <div class="body-2">
          &nbsp;
        </div>
        <hr>
        <div class="title text-md-center mt-1">
          <sup>
            Вiд замовника
          </sup>
        </div>
      </v-flex>
      <v-flex md6 class="text-md-left">
        <div class="body-2">
          &nbsp;
        </div>
        <hr>
        <div class="title text-md-center mt-1">
          <sup>
            Вiд виконавця
          </sup>
        </div>
      </v-flex>
    </v-layout>
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
        downloadingPdf: false
      }
    },

    mounted() {
      this.currYear = new Date().getFullYear();
    },

    methods: {
      updateGrid() {
        this.$nextTick(() => {
          this.reqCerts = this.certs;
          this.downloadPDF();
        });

      },

      downloadPDF() {
        this.downloadingPdf = true;

        this.$nextTick(() => {
          html2canvas(document.querySelector('#req-num-form'),
          {
            imageTimeout: 5000,
            useCORS: true
          })
          .then(canvas => {
            document.getElementById('pdf').appendChild(canvas)
            let img = canvas.toDataURL('image/png')
            let pdf = new jsPDF('portrait', 'mm', 'a4')
            pdf.addImage(img, 'JPEG', 5, 5, 200, 287)
            pdf.save('relatorio-remoto.pdf')
            document.getElementById('pdf').innerHTML = ''
            this.downloadingPdf = false;
          });
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