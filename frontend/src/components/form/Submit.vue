<template>
  <div>
    <Row style="margin: 10px;">
      <i-col span="24">
        <Button @click="onSubmit" long type="primary" :loading="submitLock">
          <span v-if="!submitLock">
            <b>Submit</b>
          </span>
          <span v-else>
            <b>Submitting Issue...</b>
          </span>
        </Button>
      </i-col>
    </Row>
  </div>
</template>

<script>
export default {
  methods: {
    onSubmit() {
      this.$store.dispatch('submit')
    }
  },
  computed: {
    submitLock() {
      return this.$store.state.form.submitLock
    }
  }
}
</script>
