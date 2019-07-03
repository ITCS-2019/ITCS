<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center>
      <v-flex md12>
        <material-card>
          <v-form>
            <v-container py-0>
              <v-layout wrap>
                <v-flex xs12 md6>
                  <v-text-field label="Логiн"
                  v-model="user.username"
                  :readonly="true"/>
                </v-flex>
                <v-flex xs12 md6>
                  <v-text-field label="ПIБ"
                  v-model="user.full_name"
                  :readonly="true"/>
                </v-flex>
                <v-flex xs12 md12>
                  <v-text-field label="Назва організації"
                  v-model="user.profile.organization_name"
                  :readonly="true"/>
                </v-flex>
              </v-layout>
              <v-layout wrap v-if="false">
                <v-flex xs12
                text-xs-right>
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
        <material-card style="margin-top: 15px;">
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
        userRole: gUserRole,
        user: {
          id: null,
          username: null,
          full_name: null,
          profile: {
            organization_name: null
          }
        }
      }
    },

    mounted() {
      axios.get(`/mariner/api/user/`)
        .then(res => {
          let userData = res.data.user;

          this.user.id = userData.id;
          this.user.username = userData.username;
          this.user.profile.organization_name = userData.profile.organization_name;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    methods: {
      saveProfile() {
        axios.put(`/mariner/api/users/${this.user.id}/`, this.user)
          .then(res => {

          })
          .catch((err) => {
            console.log(err);
          });
      }
    }
  }
</script>
