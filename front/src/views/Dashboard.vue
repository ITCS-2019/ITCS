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
              <span class="font-weight-bold">
                Кількість Напрямків
              </span>
              <span class="font-weight-bold">
                - {{directionsCount}}
              </span>
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
              <span class="font-weight-bold">
                Cертіфікатів в обробці
              </span>
              <span class="font-weight-bold">
                - {{certsInReviewCount}},
              </span>
            </v-flex>
            <v-flex md12>
              <span class="font-weight-bold">
                Виданих сертіфікатів
              </span>
              <span class="font-weight-bold">
                - {{issuedCertCount}}
              </span>
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

        this.directionsCount = dashInfo.trainigDirectionsCount;
        this.organisationsCount = dashInfo.trainigOrganisations.length;
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
