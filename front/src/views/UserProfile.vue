<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <material-card>
          <v-form>
            <v-container py-0>
              <v-layout wrap>
                <v-flex xs12
                v-if="userRole === 'НТЗ'">
                  <v-text-field label="Назва НТЗ"/>
                </v-flex>
                <v-flex xs12
                v-if="userRole !== 'НТЗ'">
                  <v-text-field label="Ім'я"/>
                </v-flex>
                <v-flex xs12
                v-if="userRole !== 'НТЗ'">
                  <v-text-field label="Прізвище"/>
                </v-flex>
                <v-flex xs12>
                  <v-text-field label="Email адреса"
                  prepend-inner-icon="mdi-email-outline"/>
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
                  v-on:click="saveProfile"
                  color="success">
                    Зберегти
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-form>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>

export default {
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
