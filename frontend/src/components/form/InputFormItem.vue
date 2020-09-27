<template>
  <FormItem :label="data.name" :required="isRequired">
    <div>
      <input
        type="text"
        :placeholder="placeholder"
        class="ivu-input ivu-input-small"
        v-model="formItemData"
      >
    </div>
  </FormItem>
</template>

<script>
export default {
  props: ['data', 'index'],
  computed: {
    formItemData: {
      get () {
        return this.$store.state.form.templateDetail[this.index].value
      },
      set (val) {
        const index = this.index
        this.$store.commit('setFormData', { index, value: val })
      }
    },
    placeholder () {
      if (this.data) {
        return this.data.name
      } else {
        return ''
      }
    },
    isRequired(){
      return Boolean(this.data.required)
    }
  }
}
</script>
