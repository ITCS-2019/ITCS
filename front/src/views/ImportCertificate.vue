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
                <v-flex xs12 md12>
                  <upload-btn title="Завантажити сертифiкат"
                  block
                  :depressed="true"
                  :outline="true"
                  color="blue"
                  ref="uploadBtn"
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

      }
    },

    created() {

    },

    methods: {

    }
  }
</script>
