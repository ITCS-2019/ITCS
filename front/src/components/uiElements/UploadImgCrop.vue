<template>
    <div>
        <img alt="photo"
        style="width: 100px; height: 100px;"
        :src="imgDataUrl"
        v-if="imgDataUrl">
        <v-text-field label="Фото моряка"
        prepend-inner-icon="mdi-camera"
        :readonly="true"
        v-model="imgName"
        v-on:click="toggleShow"/>
        <my-upload field="img"
        v-on:crop-success="cropSuccess"
        v-model="show"
        :width="50"
        :height="50"
        :langType="`ua`"
        img-format="png">
        </my-upload>
    </div>
</template>

<script>
  import myUpload from 'vue-image-crop-upload'

  export default {
    name: "CropImgUpload",
    props: {
      editable: {
        type: Boolean,
        required: false,
        default: true
      },
      status: {
        type: Number,
        required: false,
      }
    },
    data: function () {
      return {
        show: false,
        imgDataUrl: '',
        isNewPhoto: true,
        imgName: ''
      }
    },

    components: {
      'my-upload': myUpload
    },

    methods: {
      toggleShow() {
        if ((!this.show && this.isNewPhoto && this.editable)
        || (!this.show && this.status === 0)) {
          this.show = !this.show;
        }
      },

      cropSuccess(imgDataUrl, field){
        this.imgDataUrl = imgDataUrl;
        this.isNewPhoto = true;
        this.imgName = `Iм'я файла буде сгенеровано автоматично`;
      },

      showPic(imgUrl = '') {
        let photoArr = (imgUrl.length > 0) ? imgUrl.split('/') : undefined;

        this.isNewPhoto = true;
        this.imgDataUrl = imgUrl;
        this.imgName = '';

        if (photoArr) {
          this.imgName = photoArr[photoArr.length - 1];
          if (photoArr[photoArr.length - 1] !== 'no-photo-img.jpg') {
            this.isNewPhoto = false;
          }
        }
      }
    }
  }
</script>
