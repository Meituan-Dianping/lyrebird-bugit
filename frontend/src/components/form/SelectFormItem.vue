<template>
  <FormItem :label="data.name">
    <div>
      <select class="ivu-select" v-model="formItemData">
        <option
          v-for="(option, index) in data.options"
          :key="index"
          :value="bindValue(option)"
        >{{option.name}}</option>
      </select>
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
    }
  },
  methods: {
    bindValue (option) {
      return option.id
    }
  }
}
</script>
