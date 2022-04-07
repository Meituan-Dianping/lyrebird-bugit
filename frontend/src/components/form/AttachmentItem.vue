<template>
  <FormItem>
    <Row>
      <template v-if="editMode">
        <Col span="20">
          <Input style="padding-right:10px" v-model="baseName" size="small" type="text">
            <span slot="append">.{{ext}}</span>
          </Input>
        </Col>
        <Col span="4">
          <Tooltip content="Save new attachment name" placement="top">
            <a style="padding-right:5px" @click="saveName(data)">Save</a>
          </Tooltip>
          <Tooltip content="Cancel" placement="top">
            <a @click="cancelRename()">Cancel</a>
          </Tooltip>
        </Col>
      </template>
      <template v-else>
        <Col span="20">
          <Tooltip content="Click to preview" placement="top">
            <a style="padding-right:10px;color:#515a6e" @click="displayAttach(data)">
              <Icon type="md-attach" /> {{data.name}}
            </a>
          </Tooltip>
        </Col>
        <Col span="4">
          <Tooltip content="Rename this attachment" placement="top">
            <a style="padding-right:5px" @click="rename(data)">Rename</a>
          </Tooltip>
          <Tooltip content="Delete" placement="top">
            <a @click="deleteAttach(data)">Delete</a>
          </Tooltip>
        </Col>
      </template>
    </Row>
  </FormItem>
</template>

<script>
export default {
  props: ['data', 'index'],
  data () {
    return {
      'editMode': false,
      'baseName': this.data.name,
      'ext': ''
    }
  },
  methods: {
    deleteAttach (data) {
      this.$store.dispatch('removeAttachment', { id: data.id, index: this.index })
    },
    displayAttach (data) {
      this.$bus.$emit('displayAttach', data)
    },
    rename () {
      this.splitName()
      this.editMode = true
    },
    saveName (data) {
      if (!this.baseName || this.baseName.trim().length === 0) {
        this.$bus.$emit('msg.error', '文件名不能为空')
        return
      }
      if (this.baseName.indexOf('/') > -1 || this.baseName.indexOf(':') > -1){
        this.$bus.$emit('msg.error', '文件名包含非法字符')
        return
      }
      this.$store.dispatch('renameAttachment', {
        attachment: data,
        newName: this.baseName + '.' + this.ext
      })
      this.editMode = false
    },
    cancelRename () {
      this.editMode = false
    },
    splitName () {
      if (this.data.name.indexOf('.') > -1) {
        this.baseName = this.data.name.split('.').slice(0, -1).join('.')
        this.ext = String(this.data.name.split('.').slice(-1))
      }
    }
  }
}
</script>
