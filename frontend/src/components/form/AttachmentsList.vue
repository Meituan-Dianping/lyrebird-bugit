<template>
  <FormItem label="Attachments">
    <div v-if="attachments.length">
      <p v-for="(attachment, index) in attachments" :key="index" class="attachment-line">
        <AttachmentItem :attachment="attachment" :index="index"/>
      </p>
    </div>
    <div v-if="exportAttachments.length">
      <p v-for="(exportAttachment, index) in exportAttachments" :key="index" class="attachment-line">
        <ExportAttachmentItem :exportAttachment="exportAttachment" :index="index"/>
      </p>
    </div>
    <Upload
        multiple
        action="/plugins/bugit/api/attachments"
        :format="['jpg','jpeg','png','gif','bmp','wbmp','webp','tif','psd']"
        accept=".jpg,.jpeg,.png,.gif,.bmp,.wbmp,.webp,.tif,.psd"
        :show-upload-list="false"
      >
      <Tooltip
        placement="right"
        content="Support .jpg/.jpeg/.png/.gif/.bmp/.wbmp/.webp/.tif/.psd files"
        max-width="450"
      >
        <a><Icon type="md-add" /> Add attachments</a>
      </Tooltip>
    </Upload>
  </FormItem>
</template>

<script>
import AttachmentItem from '@/components/form/AttachmentItem.vue'
import ExportAttachmentItem from '@/components/form/ExportAttachmentItem.vue'

export default {
  components: {
    AttachmentItem,
    ExportAttachmentItem
  },
  created () {
    this.$io.on('attachments', this.addAttachment)
    this.$bus.$on('addExportAttachments', this.addExportAttachment)
    this.$store.dispatch('loadAttachment')
  },
  computed: {
    attachments () {
      return this.$store.state.form.attachmentsList
    },
    exportAttachments () {
      return this.$store.state.form.exportAttachmentList
    }
  },
  methods: {
    addAttachment () {
      this.$store.dispatch('loadAttachment')
    },
    addExportAttachment (exportAttachment) {
      this.$store.dispatch('addExportAttachment', exportAttachment)
    }
  }
}
</script>
<style>
.attachment-line {
  height: 32px !important;
}
.attachment-item {
  display: inline-flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 32px;
}
.attachment-name {
  display: flex !important;
  flex-direction: column;
  justify-content: center;
  width: 80%;
  height: 32px;
}
.attachment-name .ivu-tooltip {
  display: inline-flex;
}
.attachment-name .ivu-tooltip .ivu-tooltip-rel {
  width: -webkit-fill-available !important;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: keep-all;
  padding-right: 3px;
}
.attachment-actions {
  width: 20%;
  height: 32px;
  overflow: auto;
  justify-content: flex-end;
  display: flex;
  padding-right: 2px;
}
</style>
