<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <v-form>
          <v-container py-0>
            <v-layout wrap>
              <v-flex xs12 md2>
                <v-text-field label="Серiя паспорту"
                prepend-inner-icon="mdi-passport"
                mask="AA"
                v-on:blur="getSailor"
                v-model="passport_serie"/>
              </v-flex>
              <v-flex xs12 md4>
                <v-text-field label="Номер паспорту"
                prepend-inner-icon="mdi-passport"
                v-model="passport_number"
                mask="## ## ##"
                v-on:blur="getSailor"/>
              </v-flex>
              <v-flex xs12 md6>
                <v-text-field label="ІПН"
                v-model="inn"
                mask="#### #### ####"/>
              </v-flex>
            </v-layout>
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
                <v-select v-model="sex"
                :items="sexItems"
                label="Стать"
                item-text="caption"
                item-value="value">
                </v-select>
              </v-flex>
            </v-layout>
          </v-container>
        </v-form>
      </v-flex>
    </v-layout>

    <!--Notifications-->
    <v-snackbar :color="iSnackbarConfig.color"
                :top="true"
                v-model="iSnackbar"
                dark>
      <v-icon color="white"
              class="mr-3">
        {{iSnackbarConfig.icon}}
      </v-icon>
      <div>
        {{iSnackbarConfig.message}}
      </div>
      <v-icon size="16"
      v-on:click="iSnackbar = false">
        mdi-close-circle
      </v-icon>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  name: 'EditSailor',

  data() {
    return {
      iSnackbar: false,
      iSnackbarConfig: {
        color: null,
        icon: null,
        message: null
      },
      trainingApi: {
        schema: 'https://',
        host: 'dev.itcs.app/api/1.0.0',
        auth: {
          credentials: {
            email: 'traininginstitutionservice@staging.com',
            password: 'traininginstitutionservicepass'
          },
          token: ''
        }
      },
      useTrainingAPI: true,

      // TODO: refactor to one object
      minValidDate: new Date().toISOString().substr(0, 10),
      passport_serie: '',
      passport_number: '',
      inn: null,
      first_name_ukr: null,
      last_name_ukr: null,
      second_name_ukr: null,
      last_name_en: null,
      first_name_en: null,
      born: null,
      birthdayDatepicker: false,
      sex: null,
      sexItems: [
        {
          caption: 'Чоловiк',
          value: 0
        },
        {
          caption: 'Жiнка',
          value: 1
        }
      ],
      bornNotFormatted: null
    }
  },

  watch: {
    birthdayDatepicker(val) {
      val && setTimeout(() => (this.$refs.birthdayPicker.activePicker = 'YEAR'))
    },

    bornNotFormatted(val) {
      this.born = this.formatDate(this.bornNotFormatted)
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
    },

    passport_serie(val) {
      let regExp = /[^a-zA-Zа-щА-ЩЬьЮюЯяЇїІіЄєҐґ]/g;

      this.$nextTick(() => {
        if (val) {
          let newVal = val.replace(regExp, '').toUpperCase();

          this.$set(this, 'passport_serie', newVal);
        }
      });
    },
    passport_number(val) {
      let regExp = /[^0-9]/g;

      this.$nextTick(() => {
        if (val) {
          let newVal = val.replace(regExp, '');

          this.$set(this, 'passport_number', newVal);
        }
      });
    }
  },

  mounted() {
    this.getTestToken();
  },

  methods: {
    getTestToken() {
      // const token = window.axios.defaults.headers.common['X-CSRFToken'];
      // delete window.axios.defaults.headers.common['X-CSRFToken'];
      axios.post(`${this.trainingApi.schema}${this.trainingApi.host}/authentication/signin`, this.trainingApi.auth.credentials).then(res => {
        // window.axios.defaults.headers.common['X-CSRFToken'] = token;
        console.log(res);
        // this.trainingApi.auth.token =
      }).catch((err) => {
        console.log(err.response);
      });
    },
    getSailor() {
      if (!this.certId && this.passport_serie.length === 2 && this.passport_number.length === 6) {
        let params = {
            passport: {
                seriesAndNumber: `${this.passport_serie}${this.passport_number}`
            }
        };
        // const token = window.axios.defaults.headers.common['X-CSRFToken'];
        // delete window.axios.defaults.headers.common['X-CSRFToken'];
        // window.axios.defaults.headers.common['X-CSRFToken'] = this.trainingApi.auth.token;
        axios.get(`${this.trainingApi.schema}${this.trainingApi.host}/seafarers?conditions=${encodeURIComponent(JSON.stringify(params))}`).then(res => {
            // window.axios.defaults.headers.common['X-CSRFToken'] = token;
            console.log('api data:');
            console.log(res);
            this.useTrainingAPI = false;
            let passportData = res.data[0].passport;
            this.first_name_en = passportData.fullName.name.en;
            this.last_name_en = passportData.fullName.surname.en;
            this.first_name_ukr = passportData.fullName.name.ua;
            this.last_name_ukr = passportData.fullName.surname.ua;
            this.second_name_ukr = passportData.fullName.patronymic.ua;
            this.born = `${~~passportData.birthdate.day > 9 ? passportData.birthdate.day : `0${passportData.birthdate.day}`}.${~~passportData.birthdate.month > 9 ? passportData.birthdate.month : `0${passportData.birthdate.month}`}.${passportData.birthdate.year}`;
            this.inn = res[0].individualTaxpayerNumber;
            this.sex = res[0].passportData.sex.ua === 'чоловічий' ? 0 : 1;
            this.snackbarConfig.icon = 'mdi-check-circle';
            this.snackbarConfig.color = 'success';
            this.snackbarConfig.message = `Данi про моряка успiшно завантаженi!`;
            this.snackbar = true;
            // let logPayload = {
            //     message: encodeURIComponent(JSON.stringify(res)),
            //     date: new Date(),
            //     action_username: gUserName
            // };
        }).catch((err) => {
            console.log(err.response);
            if (err.response.status === 404) {
                console.log('in error!');
                this.snackbarConfig.icon = 'mdi-alert-circle';
                this.snackbarConfig.color = 'warning';
                this.snackbarConfig.message = `Данi про моряка не знайденi!`;
                this.snackbar = true;
            }
        });

        //   return axios.post(`/mariner/api/marilogger/`, logPayload)
        // }).then(res => {
        //   console.log(res);
        // }).catch((err) => {
        //   console.log(err.response);
        //   this.snackbarConfig.icon = 'mdi-alert-circle';
        //   this.snackbarConfig.color = 'warning';
        //   this.snackbarConfig.message = `Данi про моряка не знайденi!`;
        //   this.snackbar = true;
        // });
      }
    },

    saveBirthday(date) {
      this.$refs.birthdayDatepicker.save(date)
    },

    resetFormatDate(date) {
      if (!date) return null

      const [day, month, year] = date.split('.')
      return `${year}-${month}-${day}`
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
    }
  }
}
</script>
