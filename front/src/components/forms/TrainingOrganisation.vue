<template>
    <v-form>
        <v-container py-0>
            <v-layout wrap>
                <v-flex xs12 md6>
                    <img :src="logo.url" height="150" v-if="logo.url"/>
                    <v-text-field label="Завантажити лого"
                    v-on:click="pickLogo"
                    v-model="logo.name"
                    prepend-inner-icon="mdi-paperclip">
                    </v-text-field>
                    <input  type="file"
                    style="display: none"
                    ref="logo"
                    accept="image/*"
                    v-on:change="onLogoPicked">
                </v-flex>
                <v-flex xs12 md6>
                    <img :src="certBackground.url" height="150" v-if="certBackground.url"/>
                    <v-text-field label="Завантажити фон сертифiката"
                    v-on:click="pickCertBack"
                    v-model="certBackground.name"
                    prepend-inner-icon="mdi-paperclip">
                    </v-text-field>
                    <input  type="file"
                    style="display: none"
                    ref="certBack"
                    accept="image/*"
                    v-on:change="onCertBackPicked">
                </v-flex>
            </v-layout>
            <v-tabs fixed-tabs>
                <v-tab v-for="lang in langs"
                :key="lang.lang">
                    {{lang.lang}}
                </v-tab>
                <v-tab-item
                v-for="lang in langs"
                :key="lang.lang">
                    <v-layout wrap>
                        <v-flex md12>
                            <v-text-field :label="(lang.lang === 'Українська') ? 'Назва НТЗ' : 'Training organization name'"
                            v-model="lang.organization_name"
                            :readonly="(userRole === 'НТЗ') ? true : false"/>
                        </v-flex>
                        <v-flex xs12 md6>
                            <v-text-field :label="(lang.lang === 'Українська') ? 'Адреса' : 'Address'"
                            v-model="lang.mail_adress"/>
                        </v-flex>
                        <v-flex xs12 md6>
                            <v-text-field label="Код НТЗ"
                            v-model="organization.organisation_id"
                            :readonly="(userRole === 'НТЗ') ? true : false"/>
                        </v-flex>
                    </v-layout>
                </v-tab-item>
            </v-tabs>
            <v-layout wrap>
                <v-flex md12
                >
                    <v-select v-model="selectedDirections"
                    :disabled="(userRole === 'НТЗ') ? true : false"
                    :items="directions"
                    label="Напрямки підготовки"
                    item-text="caption"
                    item-value="value"
                    chips
                    multiple>
                        <template v-slot:prepend-item>
                            <v-list-tile ripple
                            v-on:click="toggle">
                                <v-list-tile-action>
                                    <v-icon :color="selectedDirections.length > 0 ? 'indigo darken-4' : ''">
                                        {{ icon }}
                                    </v-icon>
                                </v-list-tile-action>
                                <v-list-tile-content>
                                    <v-list-tile-title>Вибрати всi</v-list-tile-title>
                                </v-list-tile-content>
                            </v-list-tile>
                            <v-divider class="mt-2"></v-divider>
                        </template>
                    </v-select>
                </v-flex>
                <v-flex xs12 md4>
                    <v-text-field label="№ Договору"
                    :readonly="(userRole === 'НТЗ') ? true : false"
                    v-model="organization.contract_number"/>
                </v-flex>
                <v-flex xs12 md4
                v-if="userRole !== 'НТЗ'">
                    <v-menu v-model="activatedDatepicker"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    max-width="290px"
                    min-width="290px">
                        <template v-slot:activator="{ on }">
                            <v-text-field v-model="activated"
                            label="Дата активацi"
                            prepend-inner-icon="mdi-calendar-range"
                            readonly
                            v-on="on">
                            </v-text-field>
                        </template>
                        <v-date-picker v-model="activatedNotFormatted"
                        no-title
                        locale="uk"
                        :max="new Date().toISOString().substr(0, 10)"
                        v-on:input="selectActivated">
                        </v-date-picker>
                    </v-menu>
                </v-flex>
                <v-flex xs12 md4
                v-if="userRole !== 'НТЗ'">
                    <v-menu v-model="activeTillDatepicker"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    max-width="290px"
                    min-width="290px">
                        <template v-slot:activator="{ on }">
                            <v-text-field v-model="activeTill"
                            label="Активна до"
                            prepend-inner-icon="mdi-calendar-range"
                            readonly
                            v-on="on">
                            </v-text-field>
                        </template>
                        <v-date-picker v-model="activeTillNotFormatted"
                        no-title
                        locale="uk"
                        :min="minActiveTillDate"
                        v-on:input="selectActiveTill">
                        </v-date-picker>
                    </v-menu>
                </v-flex>
                <v-flex md12>
                    <v-text-field label="Телефони(строки роздiляються ';')"
                    v-model="organization.phone1"/>
                </v-flex>
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="Телефон"-->
                    <!--v-model="organization.phone1"-->
                    <!--mask="(###) ### - ## - ##"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="Додатковий телефон"-->
                    <!--v-model="organization.phone2"-->
                    <!--mask="(###) ### - ## - ##"/>-->
                <!--</v-flex>-->
                <v-flex xs12 md6>
                    <v-text-field label="E-mail"
                    v-model="organization.orgnisation_email"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Сайт"
                    v-model="organization.site_link"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="№ Р/рахунок"
                    v-model="organization.checking_number"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Назва банку"
                    v-model="organization.bank_name"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="МФО"
                    v-model="organization.mfo"
                    mask="### ###"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="ЄДРПОУ"
                    v-model="organization.okpo"
                    mask="## ## ## ##"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="ІПН"
                    v-model="organization.inn"
                    mask="#### #### ####"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="№ свiдоцтва ПДВ"
                    v-model="organization.nds_number"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="ПIБ керiвника"
                    v-model="organization.head_full_name"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Посада керiвника"
                    v-model="organization.head_position"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="ПIБ Бухгалтера"
                    v-model="organization.accountant_full_name"/>
                </v-flex>
            </v-layout>
            <v-layout wrap>
                <v-flex xs12
                text-xs-right>
                    <!--<v-btn class="mx-0"-->
                    <!--v-on:click="$router.go(-1)"-->
                    <!--color="success"-->
                    <!--flat>-->
                        <!--Вiдхилити-->
                    <!--</v-btn>-->
                    <v-btn class="mx-0 font-weight-light ml-1"
                    v-on:click="(userRole === 'НТЗ') ? saveOrganisationInfo() : saveOrganisation()"
                    color="success">
                        Зберегти
                    </v-btn>
                </v-flex>
            </v-layout>
        </v-container>

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
    </v-form>
</template>

<script>
export default {
  name: 'TrainingorganizationInfo',
  props: {
    organizationData: {
      type: Object,
      required: false,
      default: () => {}
    }
  },

  data(){
    return {
      logo: {
        name: '',
        url: '',
        logo_pic: ''
      },
      certBackground: {
        name: '',
        url: '',
        certBg_pic: ''
      },

      isProfile: (this.$route.name === 'User Profile') ? true : false,
      certId: ~~this.$route.params.id,
      activeTillDatepicker: false,
      activeTillNotFormatted: null,
      activeTill: null,
      minActiveTillDate: null,
      activatedDatepicker: false,
      activatedNotFormatted: null,
      activated: null,
      snackbar: false,
      snackbarConfig: {
        color: null,
        icon: null,
        message: null
      },
      directionsFull: [],
      directions: [],
      selectedDirections: [],

      // TODO: rename organization to organisation
      organization: {
        organisation_id: null,
        organisation_name: null,
        organisation_name_eng: null,
        directions: [],
        mail_adress_ukr: null,
        mail_adress_eng: null,
        phone1: null,
        phone2: null,
        orgnisation_email: null,
        site_link: null,
        checking_number: null,
        bank_name: null,
        mfo: null,
        okpo: null,
        inn: null,
        nds_number: null,
        head_full_name: null,
        head_position: null,
        accountant_full_name: null,
        activated: null,
        active_till: null,
        contract_number: null
      },
      langs: [
        {
          lang: 'Українська',
          organization_name: null,
          mail_adress: null
        },
        {
          lang: 'Англiйська',
          organization_name: null,
          mail_adress: null
        }
      ],
      userRole: gUserRole
    }
  },

  computed: {
    selectAllDirections () {
      return this.selectedDirections.length === this.directions.length;
    },

    selectSomeDirections () {
      return this.selectedDirections.length > 0 && !this.selectAllDirections;
    },

    icon () {
      if (this.selectAllDirections) return 'mdi-close-box';
      if (this.selectSomeDirections) return 'mdi-minus-box';
      return 'mdi-checkbox-blank-outline';
    }
  },

  watch: {
    activatedNotFormatted(val) {
      this.activated = this.formatDate(val);
    },

    activeTillNotFormatted(val) {
      this.activeTill = this.formatDate(val);
    }
  },

  mounted() {
    this.loadDirections();

    if (this.isProfile || this.certId !== 0)
      this.loadOrganisation();
  },

  methods: {
    pickLogo () {
      this.$refs.logo.click();
    },

    onLogoPicked (e) {
      const files = e.target.files;

      if(files[0] !== undefined) {
        this.logo.name = files[0].name;
        if(this.logo.name.lastIndexOf('.') <= 0) {
          return;
        }

        const fr = new FileReader ();

        fr.readAsDataURL(files[0]);
        fr.addEventListener('load', () => {
          this.logo.url = fr.result;
          this.logo.logo_pic = files[0];
        })
      } else {
        this.logo.name = '';
        this.logo.logo_pic = '';
        this.logo.url = '';
      }
    },

    pickCertBack () {
      this.$refs.certBack.click();
    },

    onCertBackPicked (e) {
      const files = e.target.files;

      if(files[0] !== undefined) {
        this.certBackground.name = files[0].name;
        if(this.certBackground.name.lastIndexOf('.') <= 0) {
          return;
        }

        const fr = new FileReader ();

        fr.readAsDataURL(files[0]);
        fr.addEventListener('load', () => {
          this.certBackground.url = fr.result;
          this.certBackground.certBg_pic = files[0];
        })
      } else {
        this.certBackground.name = '';
        this.certBackground.certBg_pic = '';
        this.certBackground.url = '';
      }
    },

    loadOrganisation() {
      let route = (this.isProfile) ? `/mariner/api/organisations/` : `/mariner/api/organisations/${this.certId}`;

      axios.get(route)
        .then(res => {
          let organizationData = (this.isProfile) ? res.data.organisations : res.data,
              organisations = organizationData.directions;

          if (this.isProfile || this.certId !== 0)
            this.organization['id'] = organizationData.id;

          this.organization.accountant_full_name = organizationData.accountant_full_name;
          this.activatedNotFormatted = organizationData.activated;
          this.activeTillNotFormatted = organizationData.active_till;
          this.organization.bank_name = organizationData.bank_name;
          this.organization.checking_number = organizationData.checking_number;
          this.organization.head_full_name = organizationData.head_full_name;
          this.organization.head_position = organizationData.head_position;
          this.organization.inn = organizationData.inn;
          this.organization.mail_adress_eng = organizationData.mail_adress_eng;
          this.organization.mail_adress_ukr = organizationData.mail_adress_ukr;
          this.organization.mfo = organizationData.mfo;
          this.organization.nds_number = organizationData.nds_number;
          this.organization.okpo = organizationData.okpo;
          this.organization.organisation_id = organizationData.organisation_id;
          this.organization.organisation_name = organizationData.organisation_name;
          this.organization.organisation_name_eng = organizationData.organisation_name_eng;
          this.organization.orgnisation_email = organizationData.orgnisation_email;
          this.organization.phone1 = organizationData.phone1;
          this.organization.phone2 = organizationData.phone2;
          this.organization.site_link = organizationData.site_link;
          this.organization.contract_number = organizationData.contract_number;
          this.langs[0].organization_name = organizationData.organisation_name;
          this.langs[1].organization_name = organizationData.organisation_name_eng;
          this.langs[0].mail_adress = organizationData.mail_adress_ukr;
          this.langs[1].mail_adress = organizationData.mail_adress_eng;

          if (this.isProfile) {
            organizationData.directions.forEach((direction) => {
              this.directions.push({
                caption: direction.direction_title,
                value: direction.id
              });
            });
          }

          organisations.forEach((direction) => {
            this.selectedDirections.push({
              caption: direction.direction_title,
              value: direction.id
            });
          });

          if (this.isProfile) {
            this.organization.directions = organizationData.directions;
          }

          if (organizationData.logo_pic) {
            this.logo.url = organizationData.logo_pic;
            this.logo.name = this.logo.url.split('/').slice(-1)[0];
          }

          if (organizationData.certBg_pic) {
            this.certBackground.url = organizationData.certBg_pic;
            this.certBackground.name = this.certBackground.url.split('/').slice(-1)[0];
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    saveOrganisation() {
      if (this.certId !== 0)
        this.organization['id'] = this.certId;

      this.organization.organisation_name = this.langs[0].organization_name;
      this.organization.organisation_name_eng = this.langs[1].organization_name;
      this.organization.mail_adress_ukr = this.langs[0].mail_adress;
      this.organization.mail_adress_eng = this.langs[1].mail_adress;
      this.organization.activated = this.activatedNotFormatted;
      this.organization.active_till = this.activeTillNotFormatted;

      this.organization.directions = [];

      this.selectedDirections.forEach(directionId => {
        let directionFull = this.directionsFull.find(direction => {
          if (typeof directionId === 'object')
            return direction.id === directionId.value
          else
            return direction.id === directionId
        });

        this.organization.directions.push(directionFull);
      });

      let formData = new FormData();

      formData.append('logo_pic', this.logo.logo_pic);
      formData.append('certBg_pic', this.certBackground.certBg_pic);
      formData.append('orgID', this.certId);

      axios.post(`/mariner/api/uploadOrganisationLogo/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(res => {
          return axios({
            method: (this.certId === 0) ? 'POST' : 'PUT',
            url: `/mariner/api/organisations/${(this.certId === 0) ? '' : `${this.certId}/`}`,
            data: this.organization,
          })
        })
        .then(res => {
          this.$router.push('/mariner/app/training-organisations');
        })
        .catch((err) => {
          console.log(err);
        });
    },

    formatDate(date) {
      if (!date)
        return null;

      const [year, month, day] = date.split('-');
      return `${day}.${month}.${year}`;
    },

    selectActiveTill(date) {
        this.activeTillDatepicker = false;
    },

    selectActivated(date) {
        this.activatedDatepicker = false;
        this.minActiveTillDate = date;
        if (new Date(date).getTime() > new Date(this.activeTillNotFormatted).getTime()) {
            this.activeTill = null;
            this.activeTill = null;
        }
    },

    loadDirections() {
      if (!this.isProfile) {
        axios.get(`/mariner/api/directions/`)
          .then(res => {
            this.directionsFull = res.data.directions;

            this.directionsFull.forEach((direction) => {
              this.directions.push({
                caption: direction.direction_title,
                value: direction.id
              });
            });
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },

    toggle () {
      this.$nextTick(() => {
        if (this.selectAllDirections) {
          this.selectedDirections = []
        } else {
          this.selectedDirections = this.directions.slice()
        }
      })
    },

    saveOrganisationInfo() {
      this.organization.organisation_name = this.langs[0].organization_name;
      this.organization.organisation_name_eng = this.langs[1].organization_name;
      this.organization.mail_adress_ukr = this.langs[0].mail_adress;
      this.organization.mail_adress_eng = this.langs[1].mail_adress;

      axios.put(`/mariner/api/organisations/${this.organization.id}/`,
      this.organization)
        .then(res => {
          this.showNotification({
            icon: 'mdi-check-circle',
            color: 'success',
            message: 'Iнформацiя про НТЗ змiнено!'
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },

    showNotification(config = false) {
      if (config) {
        this.snackbarConfig.icon = config.icon;
        this.snackbarConfig.color = config.color;
        this.snackbarConfig.message = config.message;
        this.snackbar = true;
      }
    }
  }
}
</script>
