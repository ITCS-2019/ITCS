<template>
  <v-toolbar
    id="core-toolbar"
    color="bg-info"
    flat
    prominent
  >
    <div class="v-toolbar-title">
      <v-toolbar-title
        class="tertiary--text font-weight-light"
      >
        <v-btn
          v-if="responsive"
          class="default v-btn--simple"
          dark
          icon
          @click.stop="onClickBtn"
        >
          <v-icon>mdi-view-list</v-icon>
        </v-btn>
        <span class="font-weight-bold">
          {{ title }}
        </span>
      </v-toolbar-title>
    </div>

    <v-spacer />
    <v-toolbar-items>
      <v-flex
        align-center
        layout
        py-2
      >
      </v-flex>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>

import {
  mapMutations
} from 'vuex'

export default {
  data: () => ({
    userRole: gUserRole,
    routeName: null,
    title: null,
    responsive: false,
    responsiveInput: false
  }),

  watch: {
    '$route' (val) {
      this.title = val.name
      this.routeName = val.name

      switch(val.name) {
        case 'Certificates':
          this.title = 'Сертифiкати'
          break
        case 'Dashboard':
          this.title = (gUserRole === 'НТЗ') ? organizationName.replace(/&quot;/g, `"`).replace(/&#39;/g, `'`) : 'Головна сторінка'
          break
        case 'Training Directions':
          this.title = 'Напрямки пiдготовки'
          break
        case 'Edit Certificate':
          this.title = 'Додати сертифiкат'
          break
        case 'Import Certificate':
          this.title = 'Iмпортувати сертифiкат'
          break
        case 'User Profile':
          this.title = 'Профiль'
          break
        case 'Sailors':
          this.title = 'Моряки'
          break
        case 'Training Organizations':
          this.title = 'Навчально-Тренувальні Заклади'
          break
      }
    }
  },

  mounted () {
    this.onResponsiveInverted()
    window.addEventListener('resize', this.onResponsiveInverted)
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.onResponsiveInverted)
  },

  methods: {
    ...mapMutations('app', ['setDrawer', 'toggleDrawer']),
    onClickBtn () {
      this.setDrawer(!this.$store.state.app.drawer)
    },
    onClick () {
      //
    },
    onResponsiveInverted () {
      if (window.innerWidth < 991) {
        this.responsive = true
        this.responsiveInput = false
      } else {
        this.responsive = false
        this.responsiveInput = true
      }
    }
  }
}
</script>

<style>
  #core-toolbar a {
    text-decoration: none;
  }
</style>
