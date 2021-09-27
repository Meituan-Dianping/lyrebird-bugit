<template>
  <div>
    <Row style="margin: 10px" :gutter="16">
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
          <Button @click="isShownDraftNameModal = true" long type="info">
            <span>
              <b>Draft</b>
            </span>
          </Button>
        </Tooltip>
      </i-col>
      <Modal
        v-model="isShownDraftNameModal"
        title="Create Draft"
      >
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
      // enterCacheName: false,
      shownDraftNameModal: false,
      shownDeleteModal: false,
      createName: 'Default',
      targetDeleteName: null
    }
  },
  mounted () {
    document.addEventListener('keydown', this.onKeyDown)
    document.addEventListener('keyup', this.onKeyUp)
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
    isShownDraftNameModal: {
      get () {
        return this.$store.state.form.isShownDraftNameModal
      },
      set (val) {
        this.$store.commit('setIsShownDraftNameModal', val)
      }
    }
  },
  methods: {
    onSubmit () {
      this.$store.dispatch('submit')
    },
    onSave () {
      this.$store.dispatch('saveCache', this.createName)
    },
    selectCacheName (name) {
      this.$store.dispatch('loadTemplate', name)
    },
    deleleDraft (template) {
      this.targetDeleteName = template.name
      this.shownDeleteModal = true
    },
    onKeyDown (event) {
      if (event.key === 'Meta') {
        this.metaKey = true
      } else if (event.key === 's') {
        if (this.metaKey) {
          window.event.preventDefault()
          this.isShownDraftNameModal = true
        }
      }
    },
    onKeyUp (event) {
      if (event.key === 'Meta') {
        this.metaKey = false
      }
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
