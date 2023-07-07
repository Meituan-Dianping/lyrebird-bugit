<template>
  <FormItem :required="isRequired">
    <template v-slot:label>
      <FormItemLabel :label="data.name"/>
    </template>
    <div style="background:#eee;padding:10px">
      <RichTextEditor :data="data"></RichTextEditor>
      <div style="padding-top:10px;" v-for="(description, index) in data.extraMsg" :key="index">
        <MovableDescription :data="description" :index="index"/>
      </div>
    </div>
  </FormItem>
</template>

<script>
import MovableDescription from '@/components/form/MovableDescription.vue'
import FormItemLabel from '@/components/form/FormItemLabel.vue'
import RichTextEditor from '@/components/form/RichTextEditor.vue'

export default {
  props: ['data', 'index'],
  components: {
    MovableDescription,
    FormItemLabel,
    RichTextEditor
  },
  created () {
    this.$bus.$on('addMessage', this.addDesc)
  },
  beforeDestroy () {
    this.$bus.$off('addMessage')
  },
  methods: {
    addDesc (desc) {
      this.$store.commit('addExtraMsg', { index: this.index, value: desc })
    },
    deleteDesc (index) {
      this.$store.commit('deleteExtraMsg', { index, propsIndex: this.index })
    },
    sortDesc (index) {
      this.$store.dispatch('setExtraMsgUpward', { index, propsIndex: this.index })
    }
  },
  computed: {
    isRequired () {
      return Boolean(this.data.required)
    }
  }
}
</script>
