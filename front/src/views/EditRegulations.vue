<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <material-card>
          <RegulationForm ref="regulationForm">
          </RegulationForm>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import RegulationForm from '@/components/forms/Regulation.vue'

  export default {
    components: {
      RegulationForm
    },

    data() {
      return {

      }
    },

    methods: {

    }
  }
</script>
