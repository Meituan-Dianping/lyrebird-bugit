<template>
  <FormItem :label="data.name" :required="isRequired">
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
    isRequired(){
      if(this.data.required){
        return this.data.required
      }else{
        return false
      }
    },
    placeholder () {
      if (this.data) {
        return this.data.name
      } else {
        return ''
      }
    }
  }
}
</script>
