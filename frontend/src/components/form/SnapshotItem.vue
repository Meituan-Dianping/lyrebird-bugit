<template>
  <FormItem>
    <Tooltip content="Click to preview" placement="top">
      <a style="padding-right:10px;color:#515a6e" @click="displayAttach(data)">{{data.name}}</a>
    </Tooltip>
    <Tooltip content="Delete this snapshot" placement="top">
      <a @click="deleteAttach(data)">delete</a>
    </Tooltip>
  </FormItem>
</template>

<script>
export default {
  props: ['data', 'index'],
  methods: {
    deleteAttach(data) {
      this.$store.commit('deleteSnapshot', this.index )
    },
    displayAttach(data) {
      this.$bus.$emit('displayAttach', data)
    }
  }
}
</script>
