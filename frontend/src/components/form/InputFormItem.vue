<template>
  <FormItem :required="isRequired">
    <template v-slot:label>
      <FormItemLabel :label="data.name"/>
    </template>
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
import FormItemLabel from '@/components/form/FormItemLabel.vue'

export default {
  components: {
    FormItemLabel
  },
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
      if (!this.data) {
        return ''
      }
      return this.data.placeholder ? this.data.placeholder : this.data.name
    },
    isRequired () {
      return Boolean(this.data.required)
    }
  }
}
</script>
