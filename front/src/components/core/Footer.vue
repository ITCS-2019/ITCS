<template>
  <v-footer
    id="core-footer"
    absolute
    height="82"
  >
    <span class="font-weight-light copyright">
      &copy;
      {{ (new Date()).getFullYear() }}
      ITCS
    </span>
  </v-footer>
</template>

<script>
export default {
  data: () => ({

  })
}
</script>

<style>
#core-footer {
  z-index: 0;
}
</style>
