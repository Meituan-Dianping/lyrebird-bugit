<template>
  <FormItem label="Attachments">
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
import SnapshotItem from '@/components/form/SnapshotItem.vue'

export default {
  components: {
    AttachmentItem,
    SnapshotItem
  },
  data () {
    return {
      'illegalChars': [':', '/']
    }
  },
  created () {
    this.$io.on('attachments', this.addAttachment)
    this.$bus.$on('addAttachments', this.addAttachment)
    this.$bus.$on('addSnapshot', this.addSnapshot)
    this.$bus.$on('saveAttachmentName', this.saveAttachmentName)
    this.$bus.$on('saveSnapshotName', this.saveSnapshotName)
    this.$store.dispatch('loadAttachment')
  },
  computed: {
    attachments () {
      return this.$store.state.form.attachmentsList
    },
    snapshots () {
      return this.$store.state.form.snapshotList
    }
  },
  methods: {
    addAttachment () {
      this.$store.dispatch('loadAttachment')
    },
    addSnapshot (snapshot) {
      this.$store.commit('addSnapshot', snapshot)
    },
    isNameValid (name) {
      if (!name || name.trim().length === 0) {
        this.$bus.$emit('msg.error', 'Rename attachment error: file name cannot be empty')
        return false
      }
      for (const i in this.illegalChars) {
        if (name.indexOf(this.illegalChars[i]) > -1) {
          this.$bus.$emit('msg.error', `Rename attachment error: illegel character [${this.illegalChars[i]}] in file name.`)
          return false
        }
      }
      return true
    },
    isNameExists (name, sourceList, index) {
      for (let i in sourceList) {
        if (sourceList[i].name.toLowerCase() === name.toLowerCase() && i.toString() !== index.toString()) {
          this.$bus.$emit('msg.error', `Rename attachment to [${name}] fail: a file with the same name exists`)
          return true
        }
      }
      return false
    },
    saveAttachmentName (attachment, index, baseName, extensionName) {
      let fullname = `${baseName}.${extensionName}`
      let sourceList = this.$store.state.form.attachmentsList
      if (!this.isNameValid(baseName)) {
        return
      }
      if (this.isNameExists(fullname, sourceList, index)) {
        return
      }
      this.$store.dispatch('renameAttachment', {
        attachment: attachment,
        newName: fullname
      })
      this.$bus.$emit('msg.success', `Rename attachment to [${fullname}] success!`)
      this.$bus.$emit(`setAttachmentEditMode_${index}`, false)
    },
    saveSnapshotName (index, name) {
      if (!this.isNameValid(name)) {
        return
      }
      let sourceList = this.$store.state.form.snapshotList
      if (this.isNameExists(name, sourceList, index)) {
        return
      }
      this.$store.commit('renameSnapshot', {
        index: index,
        newName: name
      })
      this.$bus.$emit('msg.success', `Rename snapshot to [${name}] success!`)
      this.$bus.$emit(`setSnapshotEditMode_${index}`, false)
    }
  }
}
</script>
