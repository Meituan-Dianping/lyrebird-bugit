<template>
  <FormItem>
    <Tooltip content="Click to preview" placement="top">
      <a style="padding-right:10px;color:#515a6e" @click="displayAttach(data)">
        <Icon type="md-attach" /> {{data.name}}
      </a>
    </Tooltip>
    <Tooltip content="Delete this attachment" placement="top">
      <a @click="deleteAttach(data)">delete</a>
    </Tooltip>
  </FormItem>
</template>

<script>
export default {
  props: ['data', 'index'],
  methods: {
    deleteAttach (data) {
      this.$store.dispatch('removeAttachment', { id: data.id, index: this.index })
    },
    displayAttach (data) {
      this.$bus.$emit('displayAttach', data)
    }
  }
}
</script>
