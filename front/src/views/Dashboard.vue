<template>
  <v-container
    fill-height
    fluid
    grid-list-xl
  >
    <v-layout wrap>
      <v-flex v-bind:lg4="role === 'Адміністратор' ? true : false"
      v-bind:lg6="role === 'НТЗ' ? true : false"
      v-bind:md12="role === 'Адміністратор' ? true : false"
      v-bind:md6="role === 'НТЗ' ? true : false"
      sm12>
        <material-card color="green"
        class="pb-4"
        title="Напрямки Підготовки">
          <v-layout nowrap
          class="mt-2 pl-2 pr-2">
            <v-flex md12>
              <router-link to="/mariner/app/training-directions"
              class="c-link">
                <span class="font-weight-bold black--text">
                  Кількість Напрямків
                </span>
                <span class="font-weight-bold black--text">
                  - {{directionsCount}}
                </span>
              </router-link>
            </v-flex>
          </v-layout>
        </material-card>
      </v-flex>
      <v-flex v-bind:lg4="role === 'Адміністратор' ? true : false"
      v-bind:lg6="role === 'НТЗ' ? true : false"
      v-bind:md12="role === 'Адміністратор' ? true : false"
      v-bind:md6="role === 'НТЗ' ? true : false"
      sm12
      v-if="role === 'Адміністратор'">
        <material-card color="green"
        class="pb-4"
        title="НТЗ">
          <v-layout nowrap
          class="mt-2 pl-2 pr-2">
            <v-flex md12>
              <span class="font-weight-bold">
                Кількість НТЗ
              </span>
              <span class="font-weight-bold">
                - {{organisationsCount}}
              </span>
            </v-flex>
          </v-layout>
        </material-card>
      </v-flex>
      <v-flex v-bind:lg4="role === 'Адміністратор' ? true : false"
      v-bind:lg6="role === 'НТЗ' ? true : false"
      v-bind:md12="role === 'Адміністратор' ? true : false"
      v-bind:md6="role === 'НТЗ' ? true : false"
      sm12>
        <material-card color="green"
        class="pb-4"
        title="Сертифікати">
          <v-layout wrap
          class="mt-2 pl-2 pr-2">
            <v-flex md12>
              <router-link class="c-link"
              :to="{name: 'Certificates',
              params: {
                columns: [
                  {
                    dataField: 'status',
                    filterValue: 'Обробка'
                  }
                ]
              }}">
                <span class="font-weight-bold black--text">
                  Cертіфікатів в обробці
                </span>
                <span class="font-weight-bold black--text">
                  - {{certsInReviewCount}},
                </span>
              </router-link>
            </v-flex>
            <v-flex md12>
              <router-link class="c-link"
              :to="{name: 'Certificates',
                params: {
                  columns: [
                    {
                      dataField: 'status',
                      filterValue: 'Видан'
                    }
                  ]
                }
              }">
                <span class="font-weight-bold black--text">
                  Виданих сертіфікатів
                </span>
                <span class="font-weight-bold black--text">
                  - {{issuedCertCount}}
                </span>
              </router-link>
            </v-flex>
          </v-layout>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      issuedCertCount: 0,
      certsInReviewCount: 0,
      organisationsCount: 0,
      directionsCount: 0,
      role: gUserRole
    }
  },

  mounted() {
    axios.get(`/mariner/api/dashInfo/`)
      .then(res => {
        let dashInfo = res.data.dashInfo[0];

        if (this.role === 'Адміністратор') {
          this.organisationsCount = dashInfo.trainigOrganisations.length;
        }

        this.directionsCount = dashInfo.trainigDirectionsCount;
        this.certsInReviewCount = dashInfo.certsInReviewCount;
        this.issuedCertCount = dashInfo.certCount;
      })
      .catch((err) => {
        console.log(err);
      });
  },

  methods: {
  }
}
</script>
