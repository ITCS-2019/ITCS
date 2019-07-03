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
                        <v-flex xs12>
                            <v-text-field :label="(lang.lang === 'Українська') ? 'Назва НТЗ' : 'Training organization name'"
                            v-model="lang.organization_name"
                            :readonly="true"/>
                            <v-text-field :label="(lang.lang === 'Українська') ? 'Адреса' : 'Address'"
                            v-model="lang.mail_adress"/>
                        </v-flex>
                    </v-layout>
                </v-tab-item>
            </v-tabs>
            <v-layout wrap>
                <v-flex xs12 md6>
                    <v-text-field label="Телефон"
                    v-model="organization.phone1"
                    mask="(###)### - ## - ##"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Додатковий телефон"
                    v-model="organization.phone2"
                    mask="(###)### - ## - ##"/>
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
      snackbar: false,
      snackbarConfig: {
        color: null,
        icon: null,
        message: null
      },
      organization: {
        id: null,
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
      ]
    }
  },

  mounted() {
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
