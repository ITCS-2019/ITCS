<template>
    <div>
        <img alt="photo"
        style="width: 100px; height: 100px;"
        :src="imgDataUrl"
        v-if="imgDataUrl">
        <v-text-field label="Фото моряка"
        prepend-inner-icon="mdi-camera"
        :readonly="true"
        v-on:click="toggleShow"/>
        <my-upload field="img"
        v-on:crop-success="cropSuccess"
        v-model="show"
        :width="50"
        :height="50"
        img-format="png">
        </my-upload>
    </div>
</template>

<script>
  import myUpload from 'vue-image-crop-upload'

  export default {
    name: "CropImgUpload",
    data: function () {
      return {
        show: false,
        imgDataUrl: '',
        isNewPhoto: true
      }
    },

    components: {
      'my-upload': myUpload
    },

    methods: {
      toggleShow() {
        if (!this.show && this.isNewPhoto) {
          this.show = !this.show;
        }
      },

      cropSuccess(imgDataUrl, field){
        this.imgDataUrl = imgDataUrl;
      },

      showPic(imgUrl = '') {
        let photoArr = (imgUrl.length > 0) ? imgUrl.split('/') : undefined;

        this.isNewPhoto = true;
        this.imgDataUrl = imgUrl;

        if (photoArr && photoArr[photoArr.length - 1] !== 'no-photo-img.jpg') {
          this.isNewPhoto = false;
        }
      }
    }
  }
</script>
