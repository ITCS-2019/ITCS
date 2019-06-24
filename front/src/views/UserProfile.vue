<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center>
      <v-flex md12>
        <material-card>
        </material-card>
        <material-card style="margin-top: 15px;">
          <OrganisationForm>
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
        userRole: gUserRole
      }
    },

    created() {

    },

    methods: {
      saveProfile() {

      }
    }
  }
</script>
