<template>
    <v-form>
        <v-container py-0>
            <v-tabs fixed-tabs>
                <v-tab v-for="lang in organisation.langs"
                :key="lang.lang">
                    {{lang.lang}}
                </v-tab>
                <v-tab-item
                v-for="lang in organisation.langs"
                :key="lang.lang">
                    <v-layout wrap>
                        <v-flex xs12>
                            <v-text-field :label="(lang.lang === 'Українська') ? 'Назва НТЗ' : 'Training Organisation name'"
                            v-model="lang.organisation_name"/>
                            <v-text-field :label="(lang.lang === 'Українська') ? 'Адреса' : 'Address'"
                            v-model="lang.mail_adress"/>
                        </v-flex>
                    </v-layout>
                </v-tab-item>
            </v-tabs>
            <v-layout wrap>
                <v-flex xs12 md6>
                    <v-text-field label="Телефон"
                    v-model="organisation.phone1"
                    mask="(###)### - ## - ##"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Додатковий телефон"
                    v-model="organisation.phone1"
                    mask="(###)### - ## - ##"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="E-mail"
                    v-model="organisation.orgnisation_email"/>
                    <!--<v-text-field label="Email адреса"-->
                    <!--v-model="lang.organisation_name"-->
                    <!--prepend-inner-icon="mdi-email-outline"/>-->
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Сайт"
                    v-model="organisation.site_link"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="№ Р/рахунок"
                    v-model="organisation.checking_number"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Назва банку"
                    v-model="organisation.bank_name"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="МФО"
                    v-model="organisation.mfo"
                    mask="### ###"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="ЄДРПОУ"
                    v-model="organisation.okpo"
                    mask="## ## ## ##"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="ІПН"
                    v-model="organisation.inn"
                    mask="#### #### ####"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="№ свiдоцтва ПДВ"
                    v-model="organisation.nds_number"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="ПIБ керiвника"
                    v-model="organisation.head_full_name"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="Посада керiвника"
                    v-model="organisation.head_position"/>
                </v-flex>
                <v-flex xs12 md6>
                    <v-text-field label="ПIБ Бухгалтера"
                    v-model="organisation.accountant_full_name"/>
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
  name: 'TrainingOrganisationInfo',
  props: {
    organisationData: {
      type: Object,
      required: false,
      default: () => {}
    }
  },

  data(){
    return {
      organisation: {
        id: null,
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
        active_till: null,
        langs: [
          {
            lang: 'Українська',
            organisation_name: null,
            mail_adress: null
          },
          {
            lang: 'Англiйська',
            organisation_name: null,
            mail_adress: null
          }
        ]
      }
    }
  },

  mounted() {

  }
}
</script>
