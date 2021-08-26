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
          <Button @click="enterCacheName = true" long type="info">
            <span>
              <b>Draft</b>
            </span>
          </Button>
        </Tooltip>
      </i-col>
      <Modal
          v-model="enterCacheName"
          title="Create"
          ok-text="OK"
          cancel-text="Cancel"
          @on-ok="onSave"
        >
          <Row>
            <Col span="3" align="right">
              <span>Name:</span>
            </Col>
            <Col span="18" offset="1">
              <Input v-model="createName" clearable size="small" />
            </Col>
          </Row>
        </Modal>
    </Row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      enterCacheName: false,
      shownDeleteModal: false,
      createName: '默认草稿' + new Date().getFullYear() + '-' + (new Date().getMonth()+1) + '-' + new Date().getDay() + ' ' + new Date().getHours() + ':' + new Date().getMinutes() + ':' + new Date().getSeconds(),
      targetDeleteName: null,
      // formatDate
    };
  },
  mounted () {
    document.addEventListener('keydown', this.onKeyDown)
    document.addEventListener('keyup', this.onKeyUp)
  },
  methods: {
    onSubmit() {
      this.$store.dispatch("submit");
    },
    onSave() {
      if(!this.createName || this.createName.trim().length === 0) { // 全空格
        this.$bus.$emit('msg.error', '草稿名称不能为空')
        return
      }
      this.$store.commit('setSelectedCache', this.createName) 
      console.log('onsave', this.createName)
      this.$store.dispatch("saveCache", this.createName)
      this.enterCacheName = false
    },
    onDelete() {
      this.cacheNameList[this.targetDelete]
      this.$store.dispatch("deleteCache",this.targetDeleteName)
      this.shownDeleteModal = false
    },
    selectCacheName(name) {
      this.$store.dispatch("loadTemplate",name);
    },
    deleleDraft(template) {
      this.targetDeleteName = template.name
      this.shownDeleteModal = true
    },
    onKeyDown (event) {
      if (event.key === 'Meta') {
        this.metaKey = true
      }
      else if (event.key == 's') {
        if (this.metaKey) {
          window.event.preventDefault()
          this.enterCacheName = true
        }
      }
    },
    onKeyUp (event) {
      if (event.key === 'Meta') {
        this.metaKey = false
      }
    }
  },
  computed: {
    showDrop() {
      return this.$store.state.form.cacheNameList
    },
    cacheNameList () {
      return this.$store.state.form.cacheNameList;
    },
    templates () {
      return this.$store.state.form.cacheNameList
    },
    submitLock () {
      return this.$store.state.form.submitLock
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
