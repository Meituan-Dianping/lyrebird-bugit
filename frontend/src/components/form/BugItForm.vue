<template>
  <div>
    <div v-if="fields">
      <Form class="split-left-form" :label-width="80">
        <component
          :is="getFormComponentByData(index, field)"
          v-for="(field, index) in fields"
          :key="index"
          :data="field"
          :index="index"
        ></component>
        <AttachmentsList/>
      </Form>
      <Submit></Submit>
    </div>
    <AttachmentModal/>
  </div>
</template>

<script>
import InputFormItem from '@/components/form/InputFormItem.vue'
import SelectFormItem from '@/components/form/SelectFormItem.vue'
import CompoundTextAreaFormItem from '@/components/form/CompoundTextAreaFormItem.vue'
import AttachmentsList from '@/components/form/AttachmentsList.vue'
import AttachmentModal from '@/components/form/AttachmentModal.vue'
import Submit from '@/components/form/Submit.vue'

export default {
  components: {
    InputFormItem,
    SelectFormItem,
    CompoundTextAreaFormItem,
    AttachmentsList,
    AttachmentModal,
    Submit
  },
  computed: {
    fields() {
      return this.$store.state.form.templateDetail
    }
  },
  methods: {
    getFormComponentByData(index, field) {
      if (field.component === 'input') {
        return 'InputFormItem'
      } else if (field.component === 'select') {
        return 'SelectFormItem'
      } else if (field.component === 'compoundTextarea') {
        if (!this.$store.state.form.templateDetail[index].extraMsg) {
          this.$set(this.$store.state.form.templateDetail[index], 'extraMsg', [])
        }
        return 'CompoundTextAreaFormItem'
      }
      return 'InputFormItem'
    }
  }
}
</script>

<style less>
.split-left-form {
  height: calc(100vh - 52px - 32px - 5px);
  /* total:100vh
    form
    padding: 10px
    button: 32px
    padding: 10px
    */
  overflow-y: auto;
  overflow-x: auto;
  border-bottom: 1px solid #dcdee2;
  padding-right: 10px;
  white-space: nowrap;
}
.split-left-form .ivu-form-item {
  margin-bottom: 12px;
}
</style>
