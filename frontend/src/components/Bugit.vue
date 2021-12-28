<template>
  <div class="bugit-split">
    <Split v-model="split">
      <div slot="left">
        <BugTemplateSelector></BugTemplateSelector>
        <BugItForm></BugItForm>
      </div>
      <div slot="right">
        <bugit-devices></bugit-devices>
        <bugit-extra></bugit-extra>
      </div>
    </Split>
  </div>
</template>

<script>
import BugTemplateSelector from '@/components/BugTemplateSelector.vue'
import BugItForm from '@/components/form/BugItForm.vue'
import BugitDevices from '@/components/BugitDevices.vue'
import BugitExtra from '@/components/BugitExtra.vue'

export default {
  components: {
    BugTemplateSelector,
    BugItForm,
    BugitDevices,
    BugitExtra
  },
  data () {
    return {
      metaKey: false,
      split: 0.4
    }
  },
  created () {
    this.$bus.$on('message', this.displayMessage)
    this.$bus.$on('msg.success', this.successMessage)
    this.$bus.$on('msg.info', this.infoMessage)
    this.$bus.$on('msg.error', this.errorMessage)
  },
  mounted () {
    document.addEventListener('keydown', this.onKeyDown)
    document.addEventListener('keyup', this.onKeyUp)
  },
  methods: {
    onKeyDown (event) {
      if (event.key === 'Meta') {
        this.metaKey = true
      } else if (event.key === 's') {
        if (this.metaKey) {
          window.event.preventDefault()
          this.$store.dispatch('saveCache')
        }
      } else if (event.key === 'Enter' && this.$store.state.form.shownDraftNameModal) {
        this.$store.dispatch('saveCache')
      }
    },
    onKeyUp (event) {
      if (event.key === 'Meta') {
        this.metaKey = false
      }
    },
    successMessage (msg) {
      this.$Message.success({
        content: msg,
        duration: 3,
        closable: true
      })
    },
    infoMessage (msg) {
      this.$Message.info({
        content: msg,
        duration: 3,
        closable: true
      })
    },
    errorMessage (msg) {
      this.$Message.error({
        content: msg,
        duration: 0,
        closable: true
      })
    },
    displayMessage (data) {
      if (data.hasOwnProperty('code')) {
        if (data.code === 1000) {
          this.$Message.success({
            content: data.message,
            duration: 10,
            closable: true
          })
        } else if (data.code === 3000) {
          this.$Message.error({
            content: data.message,
            duration: 0,
            closable: true
          })
        } else {
          this.$Message.error({
            content: data.message,
            duration: 0,
            closable: true
          })
        }
      } else {
        this.$Message.info({
          content: data,
          duration: 3,
          closable: true
        })
      }
    }
  }
}
</script>

<style scoped>
.bugit-split {
  height: 100vh;
}
</style>
