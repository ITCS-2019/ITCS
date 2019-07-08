<template>
    <v-form>
        <v-container py-0>
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
                v-if="userRole !== 'НТЗ'">
                    <v-select v-model="selectedDirections"
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
                <v-flex xs12 md6
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
                            label="Дата видачі"
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
                <v-flex xs12 md6
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
                            label="Дата видачі"
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
                <v-flex xs12 md6>
                    <v-text-field label="Телефон"
                    v-model="organization.phone1"
                    mask="(###) ### - ## - ##"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Додатковий телефон"
                    v-model="organization.phone2"
                    mask="(###) ### - ## - ##"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="E-mail"
                    v-model="organization.orgnisation_email"/>
                    <!--<v-text-field label="Email адреса"-->
                    <!--v-model="lang.organization_name"-->
                    <!--prepend-inner-icon="mdi-email-outline"/>-->
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
                    v-on:click="saveOrganizationInfo"
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
      directions: [],
      selectedDirections: [],
      organization: {
        id: null,
        organisation_id: null,
        organisation_name: null,
        organisation_name_eng: null,
        mail_adress_ukr: null,
        mail_adress_eng: null,
        logo_pic: null,
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
        active_till: null
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
      return this.selectedDirections.length === this.directions.length
    },

    selectSomeDirections () {
      return this.selectedDirections.length > 0 && !this.selectAllDirections
    },

    icon () {
      if (this.selectAllDirections) return 'mdi-close-box'
      if (this.selectSomeDirections) return 'mdi-minus-box'
      return 'mdi-checkbox-blank-outline'
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

    // TODO: refactor to method
    axios.get(`/mariner/api/organisations/`)
      .then(res => {
        let organizationData = res.data.organisations;

        this.organization.id = organizationData.id;
        this.organization.organisation_name = organizationData.organisation_name;
        this.organization.organisation_name_eng = organizationData.organisation_name_eng;
        this.organization.mail_adress_ukr = organizationData.mail_adress_ukr;
        this.organization.mail_adress_eng = organizationData.mail_adress_eng;
        // this.organization.logo_pic = organizationData.logo_pic;
        this.organization.phone1 = organizationData.phone1;
        this.organization.phone2 = organizationData.phone2;
        this.organization.orgnisation_email = organizationData.orgnisation_email;
        this.organization.site_link = organizationData.site_link;
        this.organization.checking_number = organizationData.checking_number;
        this.organization.bank_name = organizationData.bank_name;
        this.organization.mfo = organizationData.mfo;
        this.organization.okpo = organizationData.okpo;
        this.organization.inn = organizationData.inn;
        this.organization.nds_number = organizationData.nds_number;
        this.organization.head_full_name = organizationData.head_full_name;
        this.organization.head_position = organizationData.head_position;
        this.organization.accountant_full_name = organizationData.accountant_full_name;
        this.organization.activated = organizationData.activated;
        this.organization.active_till = organizationData.active_till;
        this.langs[0].organization_name = organizationData.organisation_name;
        this.langs[1].organization_name = organizationData.organisation_name_eng;
        this.langs[0].mail_adress = organizationData.mail_adress_ukr;
        this.langs[1].mail_adress = organizationData.mail_adress_eng;
      })
      .catch((err) => {
        console.log(err);
      });
  },

  methods: {
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
      axios.get(`/mariner/api/directionsInfo/`)
        .then(res => {
          let directions = res.data.trainigDirections;

          directions.forEach((direction) => {
            this.directions.push({
              caption: direction.direction_title,
              value: direction.id
            });
          });
        })
        .catch((err) => {
          console.log(err);
        });
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

    saveOrganizationInfo() {
      this.organization.organisation_name = this.langs[0].organization_name;
      this.organization.organisation_name_eng = this.langs[1].organization_name;
      this.organization.mail_adress_ukr = this.langs[0].mail_adress;
      this.organization.mail_adress_eng = this.langs[1].mail_adress;

      axios.put(`/mariner/api/organisations/${this.organization.id}/`, this.organization)
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
