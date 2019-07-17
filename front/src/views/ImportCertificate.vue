<template>
  <v-container fill-height
  fluid
  grid-list-xl
  pt-0>
    <v-layout justify-center wrap>
      <v-flex md12>
        <material-card color="green"
        title="Зразки файлiв">
          <v-container py-0>
            <v-layout wrap>
              <v-flex xs12 md6>
                <v-btn color="blue"
                block
                outline
                :depressed="true"
                href="/media/Import-without-directions-Example.xls">
                  <v-icon>
                    mdi-file-download
                  </v-icon>
                  <span class="ml-1">
                    Зразок файла без напрямкiв
                  </span>
                </v-btn>
              </v-flex>
              <v-flex xs12 md6>
                <v-btn color="blue"
                block
                outline
                :depressed="true"
                href="/media/Import-with-directions-Example.xls">
                  <v-icon>
                    mdi-file-download
                  </v-icon>
                  <span class="ml-1">
                    Зразок файла з напрямками
                  </span>
                </v-btn>
              </v-flex>
            </v-layout>
          </v-container>
        </material-card>

        <material-card color="green"
        title="Завантажити сертифікати з файлу(з настройкою напрямкiв пiдготовки)">
          <v-form>
            <v-container py-0>
              <v-layout wrap>
                <v-flex md12>
                  <v-combobox v-model="directions"
                  :items="directionItems"
                  label="Напрямок підготовки"
                  item-text="caption"
                  item-value="value"
                  ></v-combobox>
                </v-flex>
              </v-layout>
              <v-layout wrap>
                <v-flex xs12 md12>
                  <upload-btn title="Завантажити сертифiкат"
                  block
                  :depressed="true"
                  :outline="true"
                  color="blue"
                  ref="uploadBtn"
                  v-on:file-update="updateFile"
                  labelClass="blue--text">
                    <template slot="icon-left">
                      <v-icon class="mr-1">
                        mdi-cloud-upload
                      </v-icon>
                    </template>
                  </upload-btn>
                </v-flex>
              </v-layout>
              <v-layout wrap>
                <v-flex xs12
                text-xs-right>
                  <v-btn class="mx-0"
                  to="/mariner/app/certificates"
                  color="success"
                  flat>
                    Вiдхилити
                  </v-btn>
                  <v-btn class="mx-0"
                  v-on:click="$refs.uploadBtn.clear()"
                  color="warning">
                    Скинути
                  </v-btn>
                  <v-btn class="mx-0 font-weight-light ml-1"
                  v-bind:disabled="(file === null || directions === null) ? true : false"
                  v-on:click="saveCertificate"
                  color="success">
                    Iмпортувати
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-form>
        </material-card>
      </v-flex>
    </v-layout>

    <!--Notifications-->
    <v-snackbar :color="snackbarConfig.color"
    :top="true"
    v-model="snackbar"
    dark>
      <v-icon color="white"
      class="mr-3">
        {{snackbarConfig.icon}}
      </v-icon>
      <div>
        {{snackbarConfig.message}}
      </div>
      <v-icon size="16"
      v-on:click="snackbar = false">
        mdi-close-circle
      </v-icon>
    </v-snackbar>

    <!--Modal dialog-->
    <v-dialog v-model="modal" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">
          Успix!
        </v-card-title>
        <v-card-text>
          {{modalConfig.message}}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1"
          flat
          v-on:click="goToCerts">
            Так
          </v-btn>
          <v-btn color="red darken-1"
          flat
          v-on:click="modal = false">
            Нi
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
  import UploadButton from 'vuetify-upload-button'

  export default {
    components: {
      'upload-btn': UploadButton
    },

    data() {
      return {
        file: null,
        directions: null,
        directionItems: [],
        modal: false,
        modalConfig: {
          message: null
        },
        snackbar: false,
        snackbarConfig: {
          color: null,
          icon: null,
          message: null
        }
      }
    },

    mounted() {
      axios.get(`/mariner/api/directions/`)
        .then((res) => {

          // Directions
          let directions = res.data.directions;

          directions.forEach((direction) => {
            this.directionItems.push({
              caption: direction.direction_title,
              value: direction.id
            });
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },

    methods: {
      goToCerts() {
        this.$router.push('Certificates');
      },

      updateFile(file) {
        (file)
          ? this.file = file
          : this.file = null;
      },

      saveCertificate() {
        let formData = new FormData();

        formData.append('file', this.file);
        formData.append('directions', this.directions.value);

        axios.post(`/mariner/uploadXLS/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
          .then(res => {
            this.$refs.uploadBtn.clear();
            this.file = null;
            this.directions = null;
            this.modalConfig.message = `Iмпорт проведено успiшно! Перейти на сторiнку "Сертифiкати?"`;
            this.modal = true;
          })
          .catch((err) => {
            console.log(err);
            this.snackbarConfig.icon = 'mdi-alert-circle';
            this.snackbarConfig.color = 'red';
            this.snackbarConfig.message = 'Помилка при iмпортуваннi! Перевiрте валiднiсть файлу або повiдомте IT спецiалiста!';
            this.snackbar = true;
          });
      }
    }
  }
</script>
