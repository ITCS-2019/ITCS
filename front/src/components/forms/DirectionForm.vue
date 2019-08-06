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
              <v-flex xs12 md6>
                <v-text-field label="Напрямок навчання"
                v-model="direction_title"/>
              </v-flex>
              <v-flex xs12 md6>
                <v-text-field label="Training direction"
                v-model="direction_title_eng"/>
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
              <v-flex xs12 md6>
                <v-textarea box
                rows="1"
                label="Видано на пiдставi"
                auto-grow
                v-model="regulationInfo">
                </v-textarea>
              </v-flex>
              <v-flex xs12 md6>
                <v-textarea box
                rows="1"
                label="Regulations(Eng.)"
                auto-grow
                v-model="regulationInfoEng">
                </v-textarea>
              </v-flex>
              <v-flex xs12 md6>
                <v-textarea box
                rows="1"
                label="Iнформацiя про закiнчення курсу"
                auto-grow
                v-model="infoText">
                </v-textarea>
              </v-flex>
              <v-flex xs12 md6>
                <v-textarea box
                rows="1"
                label="Complete cource info"
                auto-grow
                v-model="infoTextEng">
                </v-textarea>
              </v-flex>
              <v-flex xs12 md6>
                <v-textarea box
                rows="1"
                label="Iнформацiя про курс"
                auto-grow
                v-model="courseInfo">
                </v-textarea>
              </v-flex>
              <v-flex xs12 md6>
                <v-textarea box
                rows="1"
                label="Course info(Eng.)"
                auto-grow
                v-model="courseInfoEng">
                </v-textarea>
              </v-flex>
              <v-flex xs12 md6>
                <v-textarea box
                rows="1"
                label="Iнспекторська iнформацiя('<br>' - переход на наступний рядок)"
                auto-grow
                v-model="inspectionInfo">
                </v-textarea>
              </v-flex>
              <v-flex xs12 md6>
                <v-textarea box
                rows="1"
                label="Inspector info('<br>' breaks row)"
                auto-grow
                v-model="inspectionInfoEng">
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
      infoText: '',
      infoTextEng: '',
      regulationInfo: '',
      regulationInfoEng: '',
      courseInfo: '',
      courseInfoEng: '',
      inspectionInfo: '',
      inspectionInfoEng: '',
      direction_title: null,
      direction_title_eng: null,
      price_id: null,
      level: null,
      levelItems: ['Підтвердження', 'Отримання'],
      allow_functions: 'Не обрано',
      allowFunctionsItems: ['Не обрано', 'Управлiння', 'Експлуатація'],
    }
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
            this.direction_title_eng = direction.direction_title_eng;
            this.level = direction.level;
            this.price_id = direction.price_id;
            this.regulationInfo = direction.regulationInfo;
            this.regulationInfoEng = direction.regulationInfoEng;
            this.courseInfo = direction.courseInfo;
            this.courseInfoEng = direction.courseInfoEng;
            this.inspectionInfo = direction.inspectionInfo;
            this.inspectionInfoEng = direction.inspectionInfoEng;
            this.infoText = direction.infoText;
            this.infoTextEng = direction.infoTextEng;
          })
          .catch((err) => {
            console.log(err);
          });
      }
    }
  }
}
</script>
