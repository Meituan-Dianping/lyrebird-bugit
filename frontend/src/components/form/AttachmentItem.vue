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
          <Tooltip :content="attachment.name" placement="top" max-width="500">
              <Icon type="md-attach" /> {{attachment.name}}
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
          <template v-if="deleteMode">
            <Tooltip content="Delete" placement="top">
              <Button
              size="small"
              type="text"
              icon="md-trash"
              @click="deleteAttach"
              />
            </Tooltip>
          </template>
          <template v-else>
            <Tooltip placement="left">
              <Button
              size="small"
              type="text"
              icon="md-trash"
              disabled
              />
              <div slot="content">
                <p>Please delete this file from</p>
                <p>the description box above.</p>
              </div>
            </Tooltip>
          </template>
        </span>
      </template>
  </span>
</template>

<script>
export default {
  props: ['attachment', 'index'],
  data () {
    return {
      'baseName': this.attachment.name,
      'extensionName': ''
    }
  },
  computed: {
    editMode: {
      get () {
        return this.$store.state.form.attachmentsList[this.index].editMode
      },
      set (val) {
        this.$store.commit('setAttachmentEditMode', {
          index: this.index,
          mode: val
        })
      }
    },
    deleteMode: {
      get () {
        return this.$store.state.form.attachmentsList[this.index].deleteMode
      }
    }
  },
  methods: {
    deleteAttach () {
      this.$store.dispatch('removeAttachment', { id: this.attachment.id, index: this.index })
    },
    displayAttach () {
      this.$bus.$emit('displayAttach', this.attachment)
    },
    rename () {
      this.splitName()
      this.editMode = true
    },
    saveName () {
      this.$store.dispatch('renameAttachment', {
        index: this.index,
        baseName: this.baseName,
        extensionName: this.extensionName
      })
    },
    cancelRename () {
      this.editMode = false
    },
    splitName () {
      if (this.attachment.name.indexOf('.') > -1) {
        this.baseName = this.attachment.name.split('.').slice(0, -1).join('.')
        this.extensionName = String(this.attachment.name.split('.').slice(-1))
      }
    }
  }
}
</script>
