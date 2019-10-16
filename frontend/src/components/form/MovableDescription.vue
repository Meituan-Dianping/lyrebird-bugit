<template>
  <div>
    <p style="line-height:16px;vertical-align:middle;">
      <Tooltip content="Upward this section" placement="top" :delay="500">
        <a v-if="index">
          <Icon type="md-arrow-round-up" style="padding-right:5px;" @click="sortDesc(index)"/>
        </a>
      </Tooltip>
      <strong style="padding-right:5px;">{{data.channel}}</strong>
      <Tooltip content="Delete this section" placement="top" :delay="500">
        <a>
          <Icon type="md-trash" @click="deleteDesc(index)"/>
        </a>
      </Tooltip>
    </p>
    <Input v-model="data.message" type="textarea" :autosize="{ minRows: 2, maxRows: 20 }"/>
  </div>
</template>

<script>
export default {
  props: ['data', 'index'],
  methods: {
    deleteDesc(index) {
      this.$parent.$parent.deleteDesc(index)
    },
    sortDesc(index) {
      this.$parent.$parent.sortDesc(index)
    }
  }
}
</script>
