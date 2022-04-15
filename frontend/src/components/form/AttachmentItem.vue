<template>
  <span class="attachment-item">
      <template v-if="editMode">
        <span class="attachment-name">
          <Input style="padding-right:3px" v-model="baseName" size="small" type="text">
            <span slot="append">.{{extensionName}}</span>
          </Input>
        </span>
        <span class="attachment-actions">
          <Tooltip content="Click to preview" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-open"
             style="margin-right:2px"
             @click="displayAttach"
             >
            </Button>
          </Tooltip>
          <Tooltip content="Save new name" placement="top">
            <Button
             type="text"
             size="small"
             icon="md-checkmark"
             style="margin-right:2px"
             @click="saveName"
             >
            </Button>
          </Tooltip>
          <Tooltip content="Cancel" placement="top">
            <Button
              size="small"
              type="text"
              icon="md-close"
              @click="cancelRename"
              >
            </Button>
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
          <Tooltip content="Click to preview" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-open"
             style="margin-right:2px"
             @click="displayAttach"
             >
            </Button>
          </Tooltip>
          <Tooltip content="Rename" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-create"
             style="margin-right:2px"
             @click="rename"
             >
            </Button>
          </Tooltip>
          <Tooltip content="Delete" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-trash"
             @click="deleteAttach"
             >
            </Button>
          </Tooltip>
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
