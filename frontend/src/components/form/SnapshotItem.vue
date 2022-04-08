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
  created () {
    this.$bus.$on(`setSnapshotEditMode_${this.index}`, this.setEditMode)
  },
  methods: {
    deleteAttach (data) {
      this.$store.commit('deleteSnapshot', this.index)
    },
    displayAttach (data) {
      this.$bus.$emit('displayAttach', data)
    },
    rename () {
      this.setEditMode(true)
    },
    cancelRename () {
      this.name = this.data.name
      this.setEditMode(false)
    },
    setEditMode (status) {
      this.editMode = status
    },
    saveName (data) {
      this.$bus.$emit('saveSnapshotName', this.index, this.name)
    }
  }
}
</script>
