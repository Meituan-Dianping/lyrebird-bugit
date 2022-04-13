<template>
  <FormItem>
    <Row>
      <template v-if="editMode">
        <Col span="20" class="attachment-col">
          <Input style="padding-right:10px" v-model="name" size="small" type="text" />
        </Col>
        <Col span="4">
          <Tooltip content="Save new snapshot name" placement="top">
            <a style="padding-right:5px" @click="saveName">Save</a>
          </Tooltip>
          <Tooltip content="Cancel" placement="top">
            <a @click="cancelRename">Cancel</a>
          </Tooltip>
        </Col>
      </template>
      <template v-else>
        <Col span="20">
          <Tooltip content="Click to preview" placement="top">
            <a style="padding-right:10px;color:#515a6e" @click="displayAttach">
              <Icon type="md-attach" /> {{name}}
            </a>
          </Tooltip>
        </Col>
        <Col span="4">
          <Tooltip content="Rename this snapshot" placement="top">
            <a style="padding-right:5px" @click="rename">Rename</a>
          </Tooltip>
          <Tooltip content="Delete" placement="top">
            <a @click="deleteAttach">Delete</a>
          </Tooltip>
        </Col>
      </template>
    </Row>
  </FormItem>
</template>

<script>
export default {
  props: ['snapshot', 'index'],
  data () {
    return {
      'name': this.snapshot.name
    }
  },
  computed: {
    editMode: {
      get () {
        return this.$store.state.form.snapshotList[this.index].editMode
      },
      set (val) {
        this.$store.commit('setSnapshotEditMode', {
          index: this.index,
          mode: val
        })
      }
    }
  },
  methods: {
    deleteAttach () {
      this.$store.commit('deleteSnapshot', this.index)
    },
    displayAttach () {
      this.$bus.$emit('displayAttach', this.snapshot)
    },
    rename () {
      this.editMode = true
    },
    cancelRename () {
      this.name = this.snapshot.name
      this.editMode = false
    },
    saveName () {
      this.$store.dispatch('renameSnapshot', {
        index: this.index,
        newName: this.name
      })
    }
  }
}
</script>
