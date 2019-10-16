<template>
  <FormItem label="attachments">
    <div v-if="attachments.length">
      <p v-for="(attachment, index) in attachments" :key="index">
        <AttachmentItem :data="attachment" :index="index"/>
      </p>
    </div>
    <div v-else>
      <p style="color:#c5c8ce">No attachment</p>
    </div>
  </FormItem>
</template>

<script>
import AttachmentItem from '@/components/form/AttachmentItem.vue'

export default {
  components: {
    AttachmentItem
  },
  created() {
    this.$io.on('attachments', this.addAttachment)
    this.$bus.$on('addAttachments', this.addAttachment)
    this.$store.dispatch('loadAttachment')
  },
  computed: {
    attachments() {
      return this.$store.state.form.attachmentsList
    }
  },
  methods: {
    addAttachment() {
      this.$store.dispatch('loadAttachment')
    }
  }
};
</script>
