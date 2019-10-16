<template>
  <Form :label-width="80" class="split-left-template-selector">
    <FormItem label="template">
      <Select v-model="selectedTemplateIndex" filterable size="small" placeholder="Select template">
        <Option v-for="(template, index) in templates" :value="index" :key="index">{{template.name}}</Option>
      </Select>
    </FormItem>
  </Form>
</template>

<script>
export default {
  created() {
    this.$store.dispatch('loadTemplateList')
  },
  computed: {
    templates() {
      return this.$store.state.form.templates
    },
    selectedTemplateIndex: {
      get() {
        return this.$store.state.form.selectedTemplateIndex
      },
      set(val) {
        this.$store.dispatch('updateSelectedTemplateIndex', val)
      }
    }
  }
}
</script>

<style scoped>
.split-left-template-selector {
  padding-right: 10px;
  background-color: #f8f8f9;
}
.split-left-template-selector .ivu-form-item {
  margin-bottom: 0px;
  padding-bottom: 5px;
}
</style>
