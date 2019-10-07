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
              <v-flex xs12 md12
              :align-self-end="true">
                <CropImgUpload ref="photoUpload"
                :editable="(currentStatus === 1 || currentStatus === 2) ? false : true"
                :status="currentStatus">
                </CropImgUpload>
              </v-flex>
            </v-layout>

            <v-layout wrap>
              <v-flex xs12 md2>
                <v-text-field label="Серiя паспорту"
                prepend-inner-icon="mdi-passport"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                v-model="passport_serie"
                mask="AA"
                v-on:blur="getSailor"/>
              </v-flex>
              <v-flex xs12 md4>
                <v-text-field label="Номер паспорту"
                prepend-inner-icon="mdi-passport"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                v-model="passport_number"
                mask="## ## ##"
                v-on:blur="getSailor"/>
              </v-flex>
              <v-flex xs12 md6>
                <v-text-field label="ІПН"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                v-model="inn"
                mask="#### #### ####"/>
              </v-flex>
            </v-layout>

            <v-layout wrap>
              <v-flex xs12 md4>
                <v-combobox v-model="last_name_ukr"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                :items="lastNames"
                label="Прiзвище"
                append-icon=""
                v-on:change="lastNameEdited = true"
                v-on:blur="lastNameEdited = false">
                </v-combobox>
              </v-flex>
              <v-flex xs12 md4>
                <v-combobox v-model="first_name_ukr"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                :items="firstNames"
                label="Iм'я"
                append-icon=""
                v-on:input="firstNameEdited = true"
                v-on:blur="firstNameEdited = false">
                </v-combobox>
              </v-flex>
              <v-flex xs12 md4>
                <v-combobox v-model="second_name_ukr"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                :items="secondNames"
                label="По батькові"
                append-icon="">
                </v-combobox>
              </v-flex>
            </v-layout>
            <v-layout wrap>
              <v-flex xs12 md4
              :align-self-end="true">
                <v-text-field label="Name"
                prepend-inner-icon="mdi-web"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                v-model="first_name_en"/>
              </v-flex>
              <v-flex xs12 md4
              :align-self-end="true">
                <v-text-field label="Surname"
                prepend-inner-icon="mdi-web"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                v-model="last_name_en"/>
              </v-flex>
              <v-flex xs12 md4
              :align-self-end="true">
                <v-menu ref="birthdayDatepicker"
                :disabled="(currentStatus === 1 || currentStatus === 2) ? true : false"
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
                    prepend-inner-icon="mdi-calendar-range"
                    mask="##.##.####"
                    v-on:keyup="birthdayDatepicker = false"
                    v-on:blur="validateBorn"
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
            </v-layout>

            <v-layout wrap>
              <v-flex xs12 md6>
                <v-menu v-model="issueDatepicker"
                :disabled="(currentStatus === 1 || currentStatus === 2) ? true : false"
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
                    mask="##.##.####"
                    v-on:keyup="issueDatepicker = false"
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
                :disabled="(currentStatus === 1 || currentStatus === 2) ? true : false"
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
                    mask="##.##.####"
                    v-on:keyup="validDatepicker = false"
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
              <v-flex xs12 md6
              v-if="~~certId === 0 && userRole !== 'НТЗ'">
                <v-combobox v-model="training_organisation"
                :items="organisations"
                label="Навчально-Тренувальний Заклад"
                item-text="caption"
                item-value="value"
                ></v-combobox>
              </v-flex>
              <v-flex xs12
              :md6="(~~certId === 0 && userRole !== 'НТЗ') ? true : false">
                <v-combobox v-model="training_direction"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
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
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
                v-model="form_number"/>
              </v-flex>
              <v-flex xs12 md4>
                <v-text-field label="Номер сертифікату"
                :readonly="(currentStatus === 1 || currentStatus === 2) ? true : false"
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
          </v-container>
        </v-form>
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
  </v-container>
</template>

<script>
import CropImgUpload from '@/components/uiElements/UploadImgCrop.vue'

export default {
  name: 'EditCertificate',
  props: {
    certId: {
      type: Number,
      required: true
    },
    lastNamesUkr: {
      type: Array,
      required: false,
      default: function() {
        return [];
      }
    },
    firstNamesUkr: {
      type: Array,
      required: false,
      default: function() {
        return [];
      }
    },
    secondNamesUkr: {
      type: Array,
      required: false,
      default: function() {
        return [];
      }
    }
  },

  components: {
    CropImgUpload
  },

  data() {
    return {
      nativeToken: window.axios.defaults.headers.common['X-CSRFToken'],
      testAPIToken: '',
      snackbar: false,
      snackbarConfig: {
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
      lastNameEdited: false,
      firstNameEdited: false,
      lastNames: [],
      firstNames: [],
      secondNames: [],
      test: '',
      currentStatus: null,
      userRole: gUserRole,

      // TODO: refactor to one object
      minValidDate: new Date().toISOString().substr(0, 10),
      passport_serie: '',
      passport_number: '',
      inn: null,
      certf_number: '',
      first_name_ukr: '',
      last_name_ukr: '',
      second_name_ukr: '',
      form_number: '',
      last_name_en: '',
      first_name_en: '',
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
      training_organisation: null,
      organisations: [],
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
    lastNamesUkr(val) {
      this.lastNames = [];
      this.lastNames = this.lastNames.concat(val);
    },

    firstNamesUkr(val) {
      this.firstNames = [];
      this.firstNames = this.firstNames.concat(val);
    },

    secondNamesUkr(val) {
      this.secondNames = [];
      this.secondNames = this.secondNames.concat(val);
    },

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
        if (val) {
          let newVal = this.capitalize(val.replace(regExp, ''));

          this.$set(this, 'first_name_en', newVal);
        }
      });
    },

    last_name_en(val) {
      let regExp = /[^[a-zA-Z\-\'\s]/g;

      this.$nextTick(() => {
        if (val) {
          let newVal = this.capitalize(val.replace(regExp, ''));

          this.$set(this, 'last_name_en', newVal);
        }
      });
    },

    first_name_ukr(val) {
      let regExp = /[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g;

      this.$nextTick(() => {
        if (val) {
          let newVal = this.capitalize(val.replace(regExp, ''));

          this.$set(this, 'first_name_ukr', newVal);

          if (this.firstNameEdited) {
            this.$set(this, 'first_name_en', this.translitToEn(newVal));
          }
        }
      });
    },

    second_name_ukr(val) {
      let regExp = /[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g;

      this.$nextTick(() => {
        if (val) {
          let newVal = this.capitalize(val.replace(regExp, ''));

          this.$set(this, 'second_name_ukr', newVal);
        }
      });
    },

    last_name_ukr(val) {
      let regExp = /[^а-щА-ЩЬьЮюЯяЇїІіЄєҐґ -/'/]/g;

      this.$nextTick(() => {
        if (val) {
          let newVal = this.capitalize(val.replace(regExp, ''));

          this.$set(this, 'last_name_ukr', newVal);

          if (this.lastNameEdited) {
              this.$set(this, 'last_name_en', this.translitToEn(newVal));
          }
        }
      });
    },

    form_number(val) {
      let regExp = /[^a-zA-Z0-9-///]/g;

      this.$nextTick(() => {
        if (val) {
          let newVal = val.replace(regExp, '');

          this.$set(this, 'form_number', newVal);
        }
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

  methods: {
    getCookie(name) {
        let value = "; " + document.cookie;
        let parts = value.split("; " + name + "=");
        if (parts.length === 2) return parts.pop().split(";").shift();
    },

    saveLog(user, method, route, payload, response) {
      let logPayload = {
        message: `Method: ${method};||***********|| Request: ${route};||***********|| Payload: ${payload};||***********|| Response: ${response}`,
        date: new Date(),
        action_username: user
      };

      axios.post(`/mariner/api/marilogger/`, logPayload).then(res => {
      }).catch((err) => {
        console.log(err.response);
      });
    },

    setTestToken(reauth = false) {
      return new Promise((resolve, reject) => {
        const token = localStorage.getItem('testApiToken');

        if (token && token.length > 0 && !reauth) {
          delete window.axios.defaults.headers.common['X-CSRFToken'];
          window.axios.defaults.headers.common['X-CSRFToken'] = token;
          resolve(token);
        } else {
          axios.post(`${this.trainingApi.schema}${this.trainingApi.host}/authentication/signin`, this.trainingApi.auth.credentials).then((res) => {
            if (res.data.token) {
              localStorage.setItem('testApiToken', res.data.token);
            }
            this.saveLog(gUserName, 'POST', `${this.trainingApi.schema}${this.trainingApi.host}/authentication/signin`, JSON.stringify(this.trainingApi.auth.credentials), JSON.stringify(res));
            delete window.axios.defaults.headers.common['X-CSRFToken'];
            window.axios.defaults.headers.common['X-CSRFToken'] = res.data.token;
            this.getSailor();
            resolve(res.data.token);
          }).catch((err) => {
            this.saveLog(gUserName, 'POST', `${this.trainingApi.schema}${this.trainingApi.host}/authentication/signin`, JSON.stringify(this.trainingApi.auth.credentials), err.response ? JSON.stringify(err.response) : err);
            reject(err.response ? err.response : err);
          });
        }
      });
    },

    setNativeToken() {
      window.axios.defaults.headers.common['X-CSRFToken'] = this.nativeToken;
    },

    async getSailor() {
      if (!this.certId && this.passport_serie.length === 2 && this.passport_number.length === 6) {
          await this.setTestToken();
          const params = {
            passport: {
              seriesAndNumber: `${this.passport_serie}${this.passport_number}`
            }
          };
          axios.get(`${this.trainingApi.schema}${this.trainingApi.host}/seafarers?conditions=${JSON.stringify(params)}`, {
            withCredentials: true,
          }).then(res => {
            this.setNativeToken();
            this.useTrainingAPI = false;
            let passportData = res.data[0].passport;
            this.sailorPhoto = res.data[0].photos[0];
            this.$refs.photoUpload.showPic(this.sailorPhoto);
            this.first_name_en = passportData.fullName.name.en;
            this.last_name_en = passportData.fullName.surname.en;
            this.first_name_ukr = passportData.fullName.name.ua;
            this.last_name_ukr = passportData.fullName.surname.ua;
            this.second_name_ukr = passportData.fullName.patronymic.ua;
            this.born = `${~~passportData.birthdate.day > 9 ? passportData.birthdate.day : `0${passportData.birthdate.day}`}.${~~passportData.birthdate.month > 9 ? passportData.birthdate.month : `0${passportData.birthdate.month}`}.${passportData.birthdate.year}`;
            this.inn = res[0].individualTaxpayerNumber;
            this.snackbarConfig.icon = 'mdi-check-circle';
            this.snackbarConfig.color = 'success';
            this.snackbarConfig.message = `Данi про моряка успiшно завантаженi!`;
            this.snackbar = true;
            this.saveLog(gUserName, 'GET', `${this.trainingApi.schema}${this.trainingApi.host}/seafarers?conditions=${JSON.stringify(params)}`, fasle, JSON.stringify(res));
          }).catch((err) => {
            this.setNativeToken();
            this.saveLog(gUserName, 'GET', `${this.trainingApi.schema}${this.trainingApi.host}/seafarers?conditions=${JSON.stringify(params)}`, false, err.response ? JSON.stringify(err.response) : err);
            if (err.response.status === 401) {
              this.setTestToken(true);
            } else {
              this.snackbarConfig.icon = 'mdi-alert-circle';
              this.snackbarConfig.color = 'warning';
              this.snackbarConfig.message = `Данi про моряка не знайденi!`;
              this.snackbar = true;
            }
          });
      }
    },
    validateBorn() {
        const [year, month, day] = this.resetFormatDate(this.born) ? this.resetFormatDate(this.born).split('-') : ['', '', ''];
        const born = new Date(year, month - 1, day);

        if ((new Date().getTime() - born.getTime() < 189302400000)
        || (born.getTime() < new Date().getTime() - 3155760000000)) {
            this.born = '';
        }
    },

    getSailorPhoto() {
      let photo = {
        dataURL: this.$refs.photoUpload.imgDataUrl,
        isNew: this.$refs.photoUpload.isNewPhoto
      };

      return photo;
    },

    loadFormData() {
      let requests = [axios.get(`/mariner/api/directions/`)];

      if (this.certId) {
        requests.push(axios.get(`/mariner/api/certificates/${this.certId}`));
      }
      else {
        requests.push(axios.get(`/mariner/api/organisations/`));
      }

      axios.all(requests)
        .then(axios.spread((directionsRes, res) => {

          // Directions
          let directions = directionsRes.data.directions;

          directions.forEach((direction) => {
            this.directions.push({
              caption: `${direction.direction_title} ( ${direction.allow_functions} / ${direction.level} )`,
              value: direction.id
            });
          });

          // Current certificate
          if (this.certId) {
            let cert = res.data;

            this.currentStatus = cert.status;

            switch(~~this.currentStatus) {
              case 0:
                this.statuses = [
                  {
                    caption: 'Чернетка',
                    value: 0
                  },
                  {
                    caption: 'Обробка',
                    value: 1
                  }
                ];
                break;
              case 1:
                this.statuses = [
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
                  }
                ];
                break;
              case 2:
                this.statuses = [
                  {
                    caption: 'Видан',
                    value: 2
                  },
                  {
                    caption: 'Анульований',
                    value: 3
                  }
                ];
                break;
            }

            if (this.currentStatus === 0 && this.userRole === 'НТЗ') {
              this.statuses = [
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
                }
              ];
            }

            if (this.currentStatus === 1 && this.userRole === 'Інспектор') {
              this.statuses = [
                {
                  caption: 'Обробка',
                  value: 1
                },
                {
                  caption: 'Чернетка',
                  value: 0
                }
              ];
            }

            if (this.currentStatus === undefined) {
              this.statuses = [
                {
                  caption: 'Чернетка',
                  value: 0
                }
              ];
            }

            this.passport_number = cert.passport_number;
            this.passport_serie = cert.passport_serie;
            this.born = this.formatDate(cert.born);
            this.certf_number = cert.certf_number;
            this.date_of_issue = this.formatDate(cert.date_of_issue);
            this.first_name_en = cert.first_name_en;
            this.last_name_en = cert.last_name_en;
            this.first_name_ukr = cert.first_name_ukr;
            this.form_number = cert.form_number;
            this.inn = cert.inn;
            this.last_name_ukr = cert.last_name_ukr;
            this.ntz_number = cert.ntz_number;
            this.second_name_ukr = cert.second_name_ukr;
            this.status = cert.status;
            this.sailorPhoto = cert.sailor.photo;
            this.training_direction = {
              caption: `${cert.training_direction.direction_title} ( ${cert.training_direction.allow_functions} / ${cert.training_direction.level} )`,
              value: cert.training_direction.id
            };
            if (this.userRole !== 'НТЗ') {
              this.training_organisation = {
                caption: cert.trainigOrganisation.organisation_name,
                value: cert.trainigOrganisation.id
              };
            }
            this.valid_date = this.formatDate(cert.valid_date);

            if (this.sailorPhoto) {
              this.$refs.photoUpload.showPic(this.sailorPhoto);
            }
          }

          // Organisations for select
          else {
            let organisations = res.data.organisations;

            if (this.userRole !== 'НТЗ') {
              organisations.forEach((organisation) => {
                this.organisations.push({
                  caption: organisation.organisation_name,
                  value: organisation.id
                });
              });
            }

            this.$refs.photoUpload.showPic('');
            this.passport_number = '';
            this.passport_serie = '';
            this.born = null;
            this.certf_number = null;
            this.date_of_issue = null;
            this.first_name_en = null;
            this.bornNotFormatted = null;
            this.issueNotFormatted = null;
            this.validNotFormatted = null;
            this.last_name_en = null;
            this.first_name_ukr = null;
            this.form_number = null;
            this.inn = null;
            this.last_name_ukr = null;
            this.ntz_number = null;
            this.second_name_ukr = '';
            this.status = 0;
            this.training_direction = null;
            this.training_organisation = null;
            this.valid_date = null;
          }
        }))
        .catch((err) => {
          console.log(err);
        });
    },

    saveBirthday(date) {
      this.$refs.birthdayDatepicker.save(date)
    },

    resetFormatDate(date) {
      if (!date) return null

      if (date.split('.').length > 1) {
        const [day, month, year] = date.split('.')
        return `${year}-${month}-${day}`
      }
      else {
          return `${date.substring(4,8)}-${date.substring(2,4)}-${date.substring(0,2)}`
      }
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
