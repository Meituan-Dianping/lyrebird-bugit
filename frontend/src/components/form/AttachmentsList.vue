<template>
  <FormItem label="attachments">
    <div v-if="attachments.length">
      <p v-for="(attachment, index) in attachments" :key="index">
        <AttachmentItem :data="attachment" :index="index"/>
      </p>
    </div>
    <div v-if="snapshots.length">
      <p v-for="(snapshot, index) in snapshots" :key="index">
        <SnapshotItem :data="snapshot" :index="index"/>
      </p>
    </div>
    <div v-else-if="!attachments.length">
      <p style="color:#c5c8ce">No attachment</p>
    </div>
  </FormItem>
</template>

<script>
import AttachmentItem from '@/components/form/AttachmentItem.vue'
import SnapshotItem from '@/components/form/SnapshotItem.vue'

export default {
  components: {
    AttachmentItem,
    SnapshotItem
  },
  created() {
    this.$io.on('attachments', this.addAttachment)
    this.$bus.$on('addAttachments', this.addAttachment)
    this.$bus.$on('addSnapshot', this.addSnapshot)
    this.$store.dispatch('loadAttachment')
  },
  computed: {
    attachments() {
      return this.$store.state.form.attachmentsList
    },
    snapshots() {
      return this.$store.state.form.snapshotList
    }
  },
  methods: {
    addAttachment() {
      this.$store.dispatch('loadAttachment')
    },
    addSnapshot(snapshot) {
      this.$store.commit('addSnapshot', snapshot)
    }
  }
};
</script>
