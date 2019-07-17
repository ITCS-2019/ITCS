<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <v-form>
          <v-container py-0>
            <v-layout wrap>
              <v-flex xs12 md12>
                <v-text-field label="Напрямок навчання"
                v-model="direction_title"/>
              </v-flex>
            </v-layout>
            <v-layout wrap>
              <v-flex xs12 md4>
                <v-text-field label="Код підготовки"
                v-model="price_id"/>
              </v-flex>
              <v-flex xs12 md4>
                <v-select :items="levelItems"
                v-model="level"
                label="Рівень кваліфікації">
                </v-select>
              </v-flex>
              <v-flex xs12 md4>
                <v-select :items="allowFunctionsItems"
                v-model="allow_functions"
                label="Дозволені рівні функцій">
                </v-select>
              </v-flex>
            </v-layout>
            <v-layout wrap>
              <v-flex xs12 md12>
                <v-textarea box
                label="Iнформацiя"
                auto-grow
                v-model="infoText">
                </v-textarea>
              </v-flex>
            </v-layout>
          </v-container>
        </v-form>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'EditTrainingDirection',
  props: {
    directionId: {
      type: Number,
      required: true
    }
  },

  data() {
    return {
      direction_title: null,
      price_id: null,
      level: null,
      levelItems: ['Підтвердження', 'Отримання'],
      allow_functions: 'Не обрано',
      allowFunctionsItems: ['Не обрано', 'Управлiння', 'Експлуатація'],
      infoText: ''
    }
  },

  mounted() {

  },

  methods: {
    clearFormData() {
      this.allow_functions = 'Не обрано';
      this.direction_title = '';
      this.level = null;
      this.price_id = null;
    },

    loadFormData() {
      if (this.directionId && this.directionId !== 0) {
        axios({
          method: 'GET',
          url: `/mariner/api/directions/${this.directionId}/`
        })
          .then(res => {
            let direction = res.data;
            this.allow_functions = direction.allow_functions;
            this.direction_title = direction.direction_title;
            this.level = direction.level;
            this.price_id = direction.price_id;
            this.infoText = direction.infoText;
          })
          .catch((err) => {
            console.log(err);
          });
      }
    }
  }
}
</script>
