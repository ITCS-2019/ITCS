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
                <v-flex xs12 md6>
                  <v-text-field label="Name"
                  prepend-inner-icon="mdi-web"
                  v-model="first_name_en"/>
                </v-flex>
                <v-flex xs12 md6>
                  <v-text-field label="Surname"
                  prepend-inner-icon="mdi-web"
                  v-model="last_name_en"/>
                </v-flex>
              </v-layout>
              <v-layout wrap>
                <v-flex xs12 md4>
                  <v-text-field label="Iм'я"
                  v-model="first_name_ukr"/>
                </v-flex>
                <v-flex xs12 md4>
                  <v-text-field label="Прiзвище"
                  v-model="last_name_ukr"/>
                </v-flex>
                <v-flex xs12 md4>
                  <v-text-field label="По батькові"
                  v-model="second_name_ukr"/>
                </v-flex>
              </v-layout>
              <v-layout wrap>
                <v-flex xs12 md6>
                  <v-menu ref="birthdayDatepicker"
                  v-model="birthdayDatepicker"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  min-width="290px">
                    <template v-slot:activator="{ on }">
                      <v-text-field v-model="born"
                      label="Дата народження"
                      readonly
                      prepend-inner-icon="mdi-calendar-range"
                      v-on="on">
                      </v-text-field>
                    </template>
                    <v-date-picker ref="birthdayPicker"
                    no-title
                    v-model="bornNotFormatted"
                    :max="new Date().toISOString().substr(0, 10)"
                    min="1950-01-01"
                    v-on:change="saveBirthday">
                    </v-date-picker>
                  </v-menu>
                </v-flex>
                <v-flex xs12 md6>
                  <v-text-field label="ІПН"
                  v-model="inn"
                  mask="#### #### ####"/>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex xs12 md6>
                  <v-menu v-model="issueDatepicker"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  max-width="290px"
                  min-width="290px">
                    <template v-slot:activator="{ on }">
                      <v-text-field v-model="date_of_issue"
                      label="Дата видачі"
                      prepend-inner-icon="mdi-calendar-range"
                      readonly
                      v-on="on">
                      </v-text-field>
                    </template>
                    <v-date-picker v-model="issueNotFormatted"
                    no-title
                    v-on:input="issueDatepicker = false">
                    </v-date-picker>
                  </v-menu>
                </v-flex>
                <v-flex xs12 md6>
                  <v-menu v-model="validDatepicker"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  max-width="290px"
                  min-width="290px">
                    <template v-slot:activator="{ on }">
                      <v-text-field v-model="valid_date"
                      label="Дійсний до"
                      prepend-inner-icon="mdi-calendar-range"
                      readonly
                      v-on="on">
                      </v-text-field>
                    </template>
                    <v-date-picker v-model="validNotFormatted"
                    no-title
                    v-on:input="validDatepicker = false">
                    </v-date-picker>
                  </v-menu>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex md12>
                  <v-combobox v-model="training_direction"
                  :items="directions"
                  label="Напрямок підготовки"
                  item-text="caption"
                  item-value="value"
                  ></v-combobox>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex xs12 md4>
                  <v-text-field label="Номер бланку документу"
                  mask="##########"
                  v-model="form_number"/>
                </v-flex>
                <v-flex xs12 md4>
                  <v-text-field label="Номер сертифікату"
                  v-model="certf_number"
                  mask="#####"/>
                </v-flex>
                <v-flex xs12 md4>
                  <v-select :items="statuses"
                  v-model="status"
                  label="Статус"
                  item-text="caption"
                  item-value="value">
                  </v-select>
                </v-flex>
              </v-layout>

              <v-layout wrap>
                <v-flex xs12
                text-xs-right>
                  <v-btn class="mx-0"
                  to="/certificates"
                  color="success"
                  flat>
                    Вiдхилити
                  </v-btn>
                  <v-btn class="mx-0 font-weight-light ml-1"
                  v-on:click="saveCertificate"
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
      inn: null,
      certf_number: null,
      first_name_ukr: null,
      last_name_ukr: null,
      second_name_ukr: null,
      form_number: null,
      last_name_en: null,
      first_name_en: null,
      born: null,
      bornNotFormatted: null,
      birthdayDatepicker: false,
      date_of_issue: null,
      issueNotFormatted: null,
      issueDatepicker: false,
      valid_date: null,
      validNotFormatted: null,
      validDatepicker: false,
      training_direction: null,
      directions: [],
      status: null,
      statuses: [
        {
          caption: 'Чернетка',
          value: 0
        },
        {
          caption: 'Обробка',
          value: 1
        },
        {
          caption: 'Видан',
          value: 2
        },
        {
          caption: 'Анульований',
          value: 3
        }
      ]
    }
  },

  watch: {
    birthdayDatepicker(val) {
      val && setTimeout(() => (this.$refs.birthdayPicker.activePicker = 'YEAR'))
    },

    bornNotFormatted(val) {
      this.born = this.formatDate(this.bornNotFormatted)
    },

    issueNotFormatted(val) {
      this.date_of_issue = this.formatDate(this.issueNotFormatted)
    },

    validNotFormatted(val) {
      this.valid_date = this.formatDate(this.validNotFormatted)
    }
  },

  created() {
    axios.get(`/mariner/api/directionsInfo/`)
      .then(res => {
        let directions = res.data.trainigDirections;

        console.log(directions);

        directions.forEach((direction) => {
          this.directions.push({
            caption: (gUserRole === 'НТЗ') ? direction.dirction_name : direction.direction_title,
            value: (gUserRole === 'НТЗ') ? direction.direction_id : direction.id
          });
        });
      })
      .catch((err) => {
        console.log(err);
      });
  },

  methods: {
    saveBirthday(date) {
      this.$refs.birthdayDatepicker.save(date)
    },

    saveIssue(date) {
      this.$refs.issueDatepicker.save(date)
    },

    saveValid(date) {
      this.$refs.validDatepicker.save(date)
    },

    saveCertificate() {
      let a = {
        first_name_en: this.first_name_en,
        last_name_en: this.last_name_en,
        last_name_ukr: this.last_name_ukr,
        first_name_ukr: this.first_name_ukr,
        second_name_ukr: this.second_name_ukr,
        born: this.born,
        inn: this.inn,
        date_of_issue: this.date_of_issue,
        valid_date: this.valid_date,
        training_direction: this.training_direction.value,
        form_number: this.form_number,
        certf_number: this.certf_number,
        status: this.status
      };

      console.log(a);
      axios.post(`/mariner/ajax/load-directions/`, a)
        .then(res => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
    },

    formatDate(date) {
      if (!date) return null

      const [year, month, day] = date.split('-')
      return `${day}.${month}.${year}`
    }
  }
}
</script>
