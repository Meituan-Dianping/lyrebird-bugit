<template>
  <div>
    <Row style="margin: 10px;" gutter="16">
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
          <Button @click="onSave" long type="info">
            <span>
              <b>Save</b>
            </span>
          </Button>
        </Tooltip>
      </i-col>
    </Row>
  </div>
</template>

<script>
export default {
  methods: {
    onSubmit () {
      this.$store.dispatch('submit')
    },
    onSave () {
      this.$store.dispatch('saveCache')
    }
  },
  computed: {
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
