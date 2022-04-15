<template>
  <span class="attachment-item">
      <template v-if="editMode">
        <span class="attachment-name">
          <Input style="padding-right:10px" v-model="name" size="small" type="text" />
        </span>
        <span class="attachment-actions">
          <Tooltip content="Click to preview" placement="top">
            <Button
             size="small"
             type="text"
             icon="md-open"
             style="margin-right:2px"
             @click="displayAttach"
             />
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
          <Tooltip :content="name" placement="top" max-width="500">
              <Icon type="md-attach" /> {{name}}
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
