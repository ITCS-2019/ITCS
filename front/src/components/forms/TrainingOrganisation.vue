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
                            :readonly="false"/>
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
                    <v-btn class="mx-0"
                    v-on:click="$router.go(-1)"
                    color="success"
                    flat>
                        Вiдхилити
                    </v-btn>
                    <v-btn class="mx-0 font-weight-light ml-1"
                    v-on:click="saveOrganizationInfo"
                    color="success">
                        Зберегти
                    </v-btn>
                </v-flex>
            </v-layout>
        </v-container>
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
    axios.get(`/mariner/api/organisations/1`)
      .then(res => {
        let organisationData = res.data;

        this.organization.id = res.data.id;
        this.organization.organisation_name = res.data.organisation_name;
        this.organization.organisation_name_eng = res.data.organisation_name_eng;
        this.organization.mail_adress_ukr = res.data.mail_adress_ukr;
        this.organization.mail_adress_eng = res.data.mail_adress_eng;
        // this.organization.logo_pic = res.data.logo_pic;
        this.organization.phone1 = res.data.phone1;
        this.organization.phone2 = res.data.phone2;
        this.organization.orgnisation_email = res.data.orgnisation_email;
        this.organization.site_link = res.data.site_link;
        this.organization.checking_number = res.data.checking_number;
        this.organization.bank_name = res.data.bank_name;
        this.organization.mfo = res.data.mfo;
        this.organization.okpo = res.data.okpo;
        this.organization.inn = res.data.inn;
        this.organization.nds_number = res.data.nds_number;
        this.organization.head_full_name = res.data.head_full_name;
        this.organization.head_position = res.data.head_position;
        this.organization.accountant_full_name = res.data.accountant_full_name;
        this.organization.activated = res.data.activated;
        this.organization.active_till = res.data.active_till;
        this.langs[0].organization_name = res.data.organisation_name;
        this.langs[1].organization_name = res.data.organisation_name_eng;
        this.langs[0].mail_adress = res.data.mail_adress_ukr;
        this.langs[1].mail_adress = res.data.mail_adress_eng;
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

      console.log(this.organization);
      axios.put(`/mariner/api/organisations/${this.organization.id}/`, this.organization)
        .then(res => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }
}
</script>
