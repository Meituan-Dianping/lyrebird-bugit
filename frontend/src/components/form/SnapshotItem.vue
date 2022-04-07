<template>
  <FormItem>
    <Row>
      <template v-if="editMode">
        <Col span="20">
          <Input style="padding-right:10px" v-model="name" size="small" type="text" />
        </Col>
        <Col span="4">
          <Tooltip content="Save new snapshot name" placement="top">
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
              <Icon type="md-attach" /> {{name}}
            </a>
          </Tooltip>
        </Col>
        <Col span="4">
          <Tooltip content="Rename this snapshot" placement="top">
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
      'name': this.data.name
    }
  },
  methods: {
    deleteAttach (data) {
      this.$store.commit('deleteSnapshot', this.index)
    },
    displayAttach (data) {
      this.$bus.$emit('displayAttach', data)
    },
    rename () {
      this.editMode = true
    },
    saveName (data) {
      if (!this.name || this.name.trim().length === 0) {
        this.$bus.$emit('msg.error', '文件名不能为空')
        return
      }
      if (this.name.indexOf('/') > -1 || this.name.indexOf(':') > -1) {
        this.$bus.$emit('msg.error', '文件名包含非法字符')
        return
      }
      let snapshotList = this.$store.state.form.snapshotList
      for (let i in snapshotList) {
        if (snapshotList[i].name.toLowerCase() === this.name.toLowerCase()) {
          if (i.toString() !== this.index.toString()) {
            this.$bus.$emit('msg.error', '重命名失败，存在同名Snapshot [' + this.name + ']')
          } else {
            this.editMode = false
          }
          return
        }
      }
      this.$store.commit('renameSnapshot', {
        index: this.index,
        newName: this.name
      })
      this.editMode = false
    },
    cancelRename () {
      this.name = this.data.name
      this.editMode = false
    }
  }
}
</script>
