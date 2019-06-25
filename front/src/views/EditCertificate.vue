<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <material-card>
          <v-form>
            <v-container py-0>
              <v-layout wrap>
                <v-flex xs12 md6>
                  <v-text-field label="Name"
                  prepend-inner-icon="mdi-web"
                  v-model="first_name_en"/>
                </v-flex>
                <v-flex xs12 md6>
                  <v-text-field label="Surname"
                  prepend-inner-icon="mdi-web"
                  v-model="last_name_en"/>
                </v-flex>
              </v-layout>
              <v-layout wrap>
                <v-flex xs12 md4>
                  <v-text-field label="Iм'я"
                  v-model="first_name_ukr"/>
                </v-flex>
                <v-flex xs12 md4>
                  <v-text-field label="Прiзвище"
                  v-model="last_name_ukr"/>
                </v-flex>
                <v-flex xs12 md4>
                  <v-text-field label="По батькові"
                  v-model="second_name_ukr"/>
                </v-flex>
              </v-layout>
              <v-layout wrap>
                <v-flex xs12 md6>
                  <v-menu ref="birthdayDatepicker"
                  v-model="birthdayDatepicker"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  min-width="290px">
                    <template v-slot:activator="{ on }">
                      <v-text-field v-model="born"
                      label="Дата народження"
                      readonly
                      prepend-inner-icon="mdi-calendar-range"
                      v-on="on">
                      </v-text-field>
                    </template>
                    <v-date-picker ref="birthdayPicker"
                    no-title
                    locale="uk"
                    v-model="bornNotFormatted"
                    :max="new Date(new Date().setFullYear(new Date().getFullYear() - 16)).toISOString().substr(0, 10)"
                    min="1950-01-01"
                    v-on:change="saveBirthday">
                    </v-date-picker>
                  </v-menu>
                </v-flex>
                <v-flex xs12 md6>
                  <v-text-field label="ІПН"
                  v-model="inn"
                  mask="#### #### ####"/>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex xs12 md6>
                  <v-menu v-model="issueDatepicker"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  max-width="290px"
                  min-width="290px">
                    <template v-slot:activator="{ on }">
                      <v-text-field v-model="date_of_issue"
                      label="Дата видачі"
                      prepend-inner-icon="mdi-calendar-range"
                      readonly
                      v-on="on">
                      </v-text-field>
                    </template>
                    <v-date-picker v-model="issueNotFormatted"
                    no-title
                    locale="uk"
                    :min="new Date().toISOString().substr(0, 10)"
                    :max="new Date(new Date().setDate(new Date().getDate() + 5)).toISOString().substr(0, 10)"
                    :allowed-dates="allowedIssueDates"
                    v-on:input="selectIssueDate">
                    </v-date-picker>
                  </v-menu>
                </v-flex>
                <v-flex xs12 md6>
                  <v-menu v-model="validDatepicker"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  max-width="290px"
                  min-width="290px">
                    <template v-slot:activator="{ on }">
                      <v-text-field v-model="valid_date"
                      label="Дійсний до"
                      prepend-inner-icon="mdi-calendar-range"
                      readonly
                      v-on="on">
                      </v-text-field>
                    </template>
                    <v-date-picker v-model="validNotFormatted"
                    :min="minValidDate"
                    no-title
                    locale="uk"
                    v-on:input="validDatepicker = false">
                    </v-date-picker>
                  </v-menu>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex md12>
                  <v-combobox v-model="training_direction"
                  :items="directions"
                  label="Напрямок підготовки"
                  item-text="caption"
                  item-value="value"
                  ></v-combobox>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex xs12 md4>
                  <v-text-field label="Номер бланку документу"
                  mask="##########"
                  v-model="form_number"/>
                </v-flex>
                <v-flex xs12 md4>
                  <v-text-field label="Номер сертифікату"
                  v-model="certf_number"
                  mask="#####"/>
                </v-flex>
                <v-flex xs12 md4>
                  <v-select :items="statuses"
                  v-model="status"
                  label="Статус"
                  item-text="caption"
                  item-value="value">
                  </v-select>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex xs12
                text-xs-right>
                  <v-btn class="mx-0"
                  to="/certificates"
                  color="success"
                  flat>
                    Вiдхилити
                  </v-btn>
                  <v-btn class="mx-0 font-weight-light ml-1"
                  v-on:click="saveCertificate"
                  color="success">
                    Зберегти
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-form>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>

export default {
  data() {
    return {
      minValidDate: new Date().toISOString().substr(0, 10),
      inn: null,
      certf_number: null,
      first_name_ukr: null,
      last_name_ukr: null,
      second_name_ukr: null,
      form_number: null,
      last_name_en: null,
      first_name_en: null,
      born: null,
      bornNotFormatted: null,
      birthdayDatepicker: false,
      date_of_issue: null,
      issueNotFormatted: null,
      issueDatepicker: false,
      valid_date: null,
      validNotFormatted: null,
      validDatepicker: false,
      training_direction: null,
      directions: [],
      status: null,
      statuses: [
        {
          caption: 'Чернетка',
          value: 0
        },
        {
          caption: 'Обробка',
          value: 1
        },
        {
          caption: 'Видан',
          value: 2
        },
        {
          caption: 'Анульований',
          value: 3
        }
      ]
    }
  },

  watch: {
    birthdayDatepicker(val) {
      val && setTimeout(() => (this.$refs.birthdayPicker.activePicker = 'YEAR'))
    },

    bornNotFormatted(val) {
      this.born = this.formatDate(this.bornNotFormatted)
    },

    issueNotFormatted(val) {
      this.date_of_issue = this.formatDate(this.issueNotFormatted)
    },

    validNotFormatted(val) {
      this.valid_date = this.formatDate(this.validNotFormatted)
    },

    first_name_en(val) {
      let regExp = /[^[a-zA-Z\-\'\s]/g;

      this.$nextTick(() => {
        let newVal = this.capitalize(val.replace(regExp, ''));

        this.$set(this, 'first_name_en', newVal);
      });
    },

    last_name_en(val) {
      let regExp = /[^[a-zA-Z\-\'\s]/g;

      this.$nextTick(() => {
        let newVal = this.capitalize(val.replace(regExp, ''));

        this.$set(this, 'last_name_en', newVal);
      });
    },

    first_name_ukr(val) {
      let regExp = /[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g;

      this.$nextTick(() => {
        let newVal = this.capitalize(val.replace(regExp, ''));

        this.$set(this, 'first_name_ukr', newVal);
        this.$set(this, 'first_name_en', this.translitToEn(newVal));
      });
    },

    second_name_ukr(val) {
      let regExp = /[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g;

      this.$nextTick(() => {
        let newVal = this.capitalize(val.replace(regExp, ''));

        this.$set(this, 'second_name_ukr', newVal);
      });
    },

    last_name_ukr(val) {
      let regExp = /[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g;

      this.$nextTick(() => {
        let newVal = this.capitalize(val.replace(regExp, ''));

        this.$set(this, 'last_name_ukr', newVal);
        this.$set(this, 'last_name_en', this.translitToEn(newVal));
      });
    }
  },

  mounted() {
    let requests = [axios.get(`/mariner/api/directions/`)];

    if (this.$route.params.id && this.$route.params.id !== 'new') {
      requests.push(axios.get(`/mariner/api/certificates/${this.$route.params.id}`));
    }

    axios.all(requests)
      .then(axios.spread((directionsRes, certRes) => {

        // Directions
        let directions = directionsRes.data.directions;

        directions.forEach((direction) => {
          this.directions.push({
            caption: direction.direction_title,
            value: direction.id
          });
        });

        // Current direction
        let cert = certRes.data;

        this.born = this.formatDate(cert.born);
        this.certf_number = cert.certf_number;
        this.date_of_issue = this.formatDate(cert.date_of_issue);
        this.first_name_en = cert.first_name_en;
        this.first_name_ukr = cert.first_name_ukr;
        this.form_number = cert.form_number;
        this.inn = cert.inn;
        this.last_name_ukr = cert.last_name_ukr;
        this.ntz_number = cert.ntz_number;
        this.second_name_ukr = cert.second_name_ukr;
        this.status = cert.status;
        this.training_direction = {
          caption: cert.training_direction.direction_title,
          value: cert.training_direction.id
        };
        this.valid_date = this.formatDate(cert.valid_date);
      }))
      .catch((err) => {
        console.log(err);
      });
  },

  methods: {
    saveBirthday(date) {
      this.$refs.birthdayDatepicker.save(date)
    },

    resetFormatDate(date) {
      if (!date) return null

      const [day, month, year] = date.split('.')
      return `${year}-${month}-${day}`
    },

    saveCertificate() {
      let formData = {
        first_name_en: this.first_name_en,
        last_name_en: this.last_name_en,
        last_name_ukr: this.last_name_ukr,
        first_name_ukr: this.first_name_ukr,
        second_name_ukr: this.second_name_ukr,
        born: this.resetFormatDate(this.born),
        inn: this.inn,
        date_of_issue: this.resetFormatDate(this.date_of_issue),
        valid_date: this.resetFormatDate(this.valid_date),
        training_direction: this.training_direction.value,
        form_number: this.form_number,
        certf_number: this.certf_number,
        status: this.status
      };

      let certId = (this.$route.params.id && this.$route.params.id === 'new') ? '' : this.$route.params.id;

      axios.post(`/mariner/api/certificates/${certId}`, formData)
        .then(res => {
          this.$router.push('/mariner/app/certificates');
        })
        .catch((err) => {
          console.log(err);
        });
    },

    formatDate(date) {
      if (!date) return null

      const [year, month, day] = date.split('-')
      return `${day}.${month}.${year}`
    },

    capitalize(str) {
      return str.toLowerCase()
              .split('-')
              .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
              .join('-')
              .split(' ')
              .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
              .join(' ');
    },

    translitToEn(str, target) {
      let ua = {
            'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'g',
            'д': 'd',
            'е': 'e',
            'є': 'ie',
            'ж': 'zh',
            'з': 'z',
            'и': 'y',
            'і': 'i',
            'ї': 'i',
            'к': 'k',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': 'u',
            'ф': 'f',
            'х': 'kh',
            'ц': 'ts',
            'ч': 'ch',
            'ш': 'sh',
            'щ': 'shch',
            'ы': 'y',
            'э': 'e',
            'ю': 'iu',
            'я': 'ia'
          },
          translited = [];

      if (str.length > 0) {
        str = str.replace(/й/g, 'i').replace(/Й/g, 'Y').replace(/Є/g, 'Ye').replace(/Ї/g, 'Yi').replace(/Ю/g, 'Yu').replace(/Я/g, 'Ya').replace(/[ъь]+/g, '');

        for (let i = 0; i < str.length; ++i) {
          translited.push(
                  ua[ str[i] ]
                  || ua[ str[i].toLowerCase() ] == undefined && str[i]
                  || ua[ str[i].toLowerCase() ].replace(/^(.)/, function ( match ) { return match.toUpperCase() })
          );
        }

        return translited.join('');
      }
      else {
        return '';
      }
    },

    allowedIssueDates: val => ![0, 6].includes(new Date(val).getDay()),

    selectIssueDate(date) {
      this.issueDatepicker = false;

      this.minValidDate = date;
      this.validNotFormatted = new Date(new Date(date).setFullYear(new Date(date).getFullYear() + 5)).toISOString().substr(0, 10);
    }
  }
}
</script>
