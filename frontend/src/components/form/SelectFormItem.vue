<template>
  <FormItem :required="isRequired">
    <template v-slot:label>
      <FormItemLabel :label="data.name"/>
    </template>
    <div>
      <Select size="small" :clearable="!data.required" :multiple="data.multiple"
      v-model="formItemData" filterable :placeholder="placeholder">
        <Option
          v-for="(option, index) in data.options"
          :key="index"
          :value="option.id"
        >{{option.name}}</Option>
      </Select>
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
    isRequired () {
      return Boolean(this.data.required)
    },
    placeholder () {
      if (!this.data) {
        return ''
      }
      return this.data.placeholder ? this.data.placeholder : this.data.name
    }
  }
}
</script>
