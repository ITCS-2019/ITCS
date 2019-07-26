<template>
    <v-form>
        <v-container py-0>
            <v-layout wrap>
                <v-flex md12>
                    <v-text-field label="Назва документу"
                    v-model="regulation.title"/>
                </v-flex>
                <v-flex xs6 md4>
                    <v-text-field label="Номер документу"
                    v-model="regulation.number"/>
                </v-flex>
                <v-flex xs6 md4>
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
                            <v-text-field v-model="activatedFormatted"
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


                    <!--<v-text-field label="Активний з"-->
                    <!--v-model="regulation.date_activation"/>-->
                </v-flex>
                <v-flex xs6 md4>
                    <v-text-field label="Статус"
                    v-model="regulation.status"/>
                </v-flex>
                <!--<v-flex xs12 md6-->
                <!--v-if="userRole !== 'НТЗ'">-->
                    <!--<v-menu v-model="activatedDatepicker"-->
                    <!--:close-on-content-click="false"-->
                    <!--:nudge-right="40"-->
                    <!--lazy-->
                    <!--transition="scale-transition"-->
                    <!--offset-y-->
                    <!--full-width-->
                    <!--max-width="290px"-->
                    <!--min-width="290px">-->
                        <!--<template v-slot:activator="{ on }">-->
                            <!--<v-text-field v-model="activated"-->
                            <!--label="Дата видачі"-->
                            <!--prepend-inner-icon="mdi-calendar-range"-->
                            <!--readonly-->
                            <!--v-on="on">-->
                            <!--</v-text-field>-->
                        <!--</template>-->
                        <!--<v-date-picker v-model="activatedNotFormatted"-->
                        <!--no-title-->
                        <!--locale="uk"-->
                        <!--:max="new Date().toISOString().substr(0, 10)"-->
                        <!--v-on:input="selectActivated">-->
                        <!--</v-date-picker>-->
                    <!--</v-menu>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6-->
                <!--v-if="userRole !== 'НТЗ'">-->
                    <!--<v-menu v-model="activeTillDatepicker"-->
                    <!--:close-on-content-click="false"-->
                    <!--:nudge-right="40"-->
                    <!--lazy-->
                    <!--transition="scale-transition"-->
                    <!--offset-y-->
                    <!--full-width-->
                    <!--max-width="290px"-->
                    <!--min-width="290px">-->
                        <!--<template v-slot:activator="{ on }">-->
                            <!--<v-text-field v-model="activeTill"-->
                            <!--label="Дата видачі"-->
                            <!--prepend-inner-icon="mdi-calendar-range"-->
                            <!--readonly-->
                            <!--v-on="on">-->
                            <!--</v-text-field>-->
                        <!--</template>-->
                        <!--<v-date-picker v-model="activeTillNotFormatted"-->
                        <!--no-title-->
                        <!--locale="uk"-->
                        <!--:min="minActiveTillDate"-->
                        <!--v-on:input="selectActiveTill">-->
                        <!--</v-date-picker>-->
                    <!--</v-menu>-->
                <!--</v-flex>-->
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
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="E-mail"-->
                    <!--v-model="organization.orgnisation_email"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="Сайт"-->
                    <!--v-model="organization.site_link"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="№ Р/рахунок"-->
                    <!--v-model="organization.checking_number"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="Назва банку"-->
                    <!--v-model="organization.bank_name"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="МФО"-->
                    <!--v-model="organization.mfo"-->
                    <!--mask="### ###"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="ЄДРПОУ"-->
                    <!--v-model="organization.okpo"-->
                    <!--mask="## ## ## ##"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="ІПН"-->
                    <!--v-model="organization.inn"-->
                    <!--mask="#### #### ####"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="№ свiдоцтва ПДВ"-->
                    <!--v-model="organization.nds_number"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="ПIБ керiвника"-->
                    <!--v-model="organization.head_full_name"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="Посада керiвника"-->
                    <!--v-model="organization.head_position"/>-->
                <!--</v-flex>-->
                <!--<v-flex xs12 md6>-->
                    <!--<v-text-field label="ПIБ Бухгалтера"-->
                    <!--v-model="organization.accountant_full_name"/>-->
                <!--</v-flex>-->
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
                    v-on:click="saveRegulation"
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
      logoName: '',
      logoUrl: '',
      certBackName: '',
      certBackUrl: '',
      activatedDatepicker: false,
      activatedFormatted: null,
      activatedNotFormatted: null,




      isProfile: (this.$route.name === 'User Profile') ? true : false,
      certId: ~~this.$route.params.id,
      activeTillDatepicker: false,
      activeTillNotFormatted: null,
      activeTill: null,
      minActiveTillDate: null,
      // activatedDatepicker: false,
      // activatedNotFormatted: null,
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

      regulation: {
        title: null,
        number: null,
        date_activation: null,
        status: null,
        text: null,
        pdf_file: null,
        user: null,
        prev_version: null,
        organisation: null,
        regulation_organization_link: null
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

  watch: {
    activatedNotFormatted(val) {
      this.activatedFormatted = this.formatDate(val);
    }
  },

  mounted() {

  },

  methods: {
    saveRegulation() {
      console.log(this.regulation);
    },

    formatDate(date) {
      if (!date)
        return null;

      const [year, month, day] = date.split('-');
      return `${day}.${month}.${year}`;
    },

    selectActivated(date) {
        this.activatedDatepicker = false;
        this.regulation.date_activation = date;
    }
  }
}
</script>
