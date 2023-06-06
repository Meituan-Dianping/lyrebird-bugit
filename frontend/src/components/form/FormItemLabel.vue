<template>
  <span class="form-item-label">
    {{  label  }}
  </span>
</template>

<script>
export default {
  props: {
    label: {
      type: String
    }
  }
}
</script>

<style>
.form-item-label {
  white-space: normal;
}
</style>
