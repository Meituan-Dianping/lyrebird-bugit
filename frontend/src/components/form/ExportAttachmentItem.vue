<template>
  <span class="attachment-item">
      <template v-if="editMode">
        <span class="attachment-name">
          <Input style="padding-right:3px" v-model="baseName" size="small" type="text">
            <span slot="append">.{{extensionName}}</span>
          </Input>
        </span>
        <span class="attachment-actions">
          <Tooltip content="Preview" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-open"
             style="margin-right:2px"
             @click="displayAttach"
             />
          </Tooltip>
          <Tooltip content="Save" placement="top">
            <Button
             type="text"
             size="small"
             icon="md-checkmark"
             style="margin-right:2px"
             @click="saveName"
             />
          </Tooltip>
          <Tooltip content="Cancel" placement="top">
            <Button
              size="small"
              type="text"
              icon="md-close"
              @click="cancelRename"
              />
          </Tooltip>
        </span>
      </template>
      <template v-else>
        <span class="attachment-name">
          <Tooltip :content="name" placement="top" max-width="500">
              <Icon type="md-attach" /> {{name}}
          </Tooltip>
        </span>
        <span class="attachment-actions">
          <Tooltip content="Preview" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-open"
             style="margin-right:2px"
             @click="displayAttach"
             />
          </Tooltip>
          <Tooltip content="Rename" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-create"
             style="margin-right:2px"
             @click="rename"
             />
          </Tooltip>
          <Tooltip content="Delete" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-trash"
             @click="deleteAttach"
             />
          </Tooltip>
        </span>
      </template>
  </span>
</template>

<script>
export default {
  props: ['exportAttachment', 'index'],
  data () {
    return {
      'baseName': this.exportAttachment.name,
      'extensionName': this.exportAttachment.attachmentType
    }
  },
  computed: {
    name () {
      return `${this.baseName}.${this.extensionName}`
    },
    editMode: {
      get () {
        return this.$store.state.form.exportAttachmentList[this.index].editMode
      },
      set (val) {
        this.$store.commit('setExportAttachmentEditMode', {
          index: this.index,
          mode: val
        })
      }
    }
  },
  methods: {
    deleteAttach () {
      this.$store.commit('deleteExportAttachment', this.index)
    },
    displayAttach () {
      this.$bus.$emit('displayAttach', this.exportAttachment)
    },
    rename () {
      this.editMode = true
    },
    cancelRename () {
      this.baseName = this.exportAttachment.name
      this.editMode = false
    },
    saveName () {
      this.$store.dispatch('renameExportAttachment', {
        index: this.index,
        baseName: this.baseName,
        extensionName: this.extensionName
      })
    }
  }
}
</script>
