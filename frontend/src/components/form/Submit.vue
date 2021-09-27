<template>
  <div>
    <Row style="margin: 10px;" :gutter="16">
      <i-col span="18">
        <Button @click="onSubmit" long type="primary" :loading="submitLock">
          <span v-if="!submitLock">
            <b>Submit</b>
          </span>
          <span v-else>
            <b>Submitting Issue...</b>
          </span>
        </Button>
      </i-col>
      <i-col span="6">
        <Tooltip content="Save (⌘+s)" placement="top" :delay="500">
          <Button @click="shownDraftNameModal = true" long type="info">
            <span>
              <b>Draft</b>
            </span>
          </Button>
        </Tooltip>
      </i-col>
      <Modal v-model="shownDraftNameModal" title="Create Draft">
        <Row>
          <i-col span="3" align="right">
            <span>Name:</span>
          </i-col>
          <i-col span="18" offset="1">
            <Input v-model="createName" clearable size="small" />
          </i-col>
        </Row>
        <div slot="footer">
          <Button type="primary" long @click="onSave">Save</Button>
        </div>
      </Modal>
    </Row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      shownDeleteModal: false,
      targetDeleteName: null
    }
  },
  computed: {
    showDrop () {
      return this.$store.state.form.cacheNameList
    },
    cacheNameList () {
      return this.$store.state.form.cacheNameList
    },
    templates () {
      return this.$store.state.form.cacheNameList
    },
    submitLock () {
      return this.$store.state.form.submitLock
    },
    shownDraftNameModal: {
      get () {
        return this.$store.state.form.shownDraftNameModal
      },
      set (val) {
        this.$store.commit('setShownDraftNameModal', val)
      }
    },
    createName: {
      get () {
        return this.$store.state.form.createName
      },
      set (val) {
        this.$store.commit('setCreateName', val)
      }
    }
  },
  methods: {
    onSubmit () {
      this.$store.dispatch('submit')
    },
    onSave () {
      this.$store.dispatch('saveCache')
    },
    selectCacheName (name) {
      this.$store.dispatch('loadTemplate', name)
    }
  }
}
</script>

<style scoped>
.ivu-tooltip {
  display: inline-block;
  width: 100%;
}
</style>
