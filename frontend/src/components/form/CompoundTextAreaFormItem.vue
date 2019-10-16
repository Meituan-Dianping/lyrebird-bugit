<template>
  <FormItem :label="data.name">
    <div style="background:#eee;padding:10px">
      <Input
        type="textarea"
        v-model="data.value"
        :autosize="{minRows: 2, maxRows: 20}"
        placeholder="Enter your description..."
      />
      <div style="padding-top:10px;" v-for="(description, index) in data.extraMsg" :key="index">
        <MovableDescription :data="description" :index="index"/>
      </div>
    </div>
  </FormItem>
</template>

<script>
import MovableDescription from '@/components/form/MovableDescription.vue'

export default {
  props: ['data', 'index'],
  components: {
    MovableDescription
  },
  created() {
    this.$bus.$on('addMessage', this.addDesc)
  },
  methods: {
    addDesc(desc) {
      this.$store.commit('addExtraMsg', { index: this.index, value: desc })
    },
    deleteDesc(index) {
      this.$store.commit('deleteExtraMsg', { index, propsIndex: this.index })
    },
    sortDesc(index) {
      this.$store.dispatch('setExtraMsgUpward', { index, propsIndex: this.index })
    }
  }
}
</script>
