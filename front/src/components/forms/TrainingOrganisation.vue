<template>
    <v-form>
        <v-container py-0>
            <v-tabs fixed-tabs>
                <v-tab v-for="lang in organisation.langs"
                :key="lang">
                    {{lang.lang}}
                </v-tab>

                <v-tab-item
                v-for="lang in organisation.langs"
                :key="lang">
                    <v-layout wrap>
                        <v-flex xs12>
                            {{lang.lang}}
                            <v-text-field label="Назва НТЗ"/>
                        </v-flex>
                        <v-flex xs12>
                            <v-text-field label="Email адреса"
                            prepend-inner-icon="mdi-email-outline"/>
                        </v-flex>
                    </v-layout>
                </v-tab-item>
            </v-tabs>
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
        logo: null,
        phones: [],
        email: null,
        langs: [
          {
            lang: 'Українська',
            head_name: null,
            head_position: null
          },
          {
            lang: 'Англiйська',
            director_name: null,
            head_position: null
          }
        ]
      }
    }
  },

  created() {

    },

  mounted() {

  }
}
</script>
