<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <material-card>
          <OrganisationForm ref="organisationForm">
          </OrganisationForm>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import OrganisationForm from '@/components/forms/TrainingOrganisation.vue'

  export default {
    components: {
      OrganisationForm
    },

    data() {
      return {

      }
    },

    methods: {

    }
  }
</script>
