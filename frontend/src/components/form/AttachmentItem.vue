<template>
  <FormItem>
    <Row>
      <template v-if="editMode">
        <Col span="20" class="attachment-col">
          <Input style="padding-right:10px" v-model="baseName" size="small" type="text">
            <span slot="append">.{{extensionName}}</span>
          </Input>
        </Col>
        <Col span="4">
          <Tooltip content="Save new attachment name" placement="top">
            <a style="padding-right:5px" @click="saveName()">Save</a>
          </Tooltip>
          <Tooltip content="Cancel" placement="top">
            <a @click="cancelRename()">Cancel</a>
          </Tooltip>
        </Col>
      </template>
      <template v-else>
        <Col span="20">
          <Tooltip content="Click to preview" placement="top">
            <a style="padding-right:10px;color:#515a6e" @click="displayAttach()">
              <Icon type="md-attach" /> {{attachment.name}}
            </a>
          </Tooltip>
        </Col>
        <Col span="4">
          <Tooltip content="Rename this attachment" placement="top">
            <a style="padding-right:5px" @click="rename()">Rename</a>
          </Tooltip>
          <Tooltip content="Delete" placement="top">
            <a @click="deleteAttach()">Delete</a>
          </Tooltip>
        </Col>
      </template>
    </Row>
  </FormItem>
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
