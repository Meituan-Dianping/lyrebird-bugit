<template>
  <div>
    <Row>
      <Col span="6">
        <Tooltip content="Upward this section" placement="top" :delay="500">
          <a v-if="index">
            <Icon type="md-arrow-round-up" style="padding-right:5px;" @click="sortDesc(index)" />
          </a>
        </Tooltip>
        <strong style="padding-right:5px;">{{data.channel}}</strong>
        <Tooltip content="Delete this section" placement="top" :delay="500">
          <a>
            <Icon type="md-trash" @click="deleteDesc(index)" />
          </a>
        </Tooltip>
      </Col>
      <Col span="18" style=" text-align:right">
        <Tag v-if="data.sender" color="green" style="max-width:100%">{{data.sender.file}}</Tag>
      </Col>
    </Row>
    <Input v-model="data.message" type="textarea" :autosize="{ minRows: 2, maxRows: 20 }" />
  </div>
</template>

<script>
export default {
  props: ["data", "index"],
  methods: {
    deleteDesc (index) {
      this.$parent.$parent.deleteDesc(index)
    },
    sortDesc (index) {
      this.$parent.$parent.sortDesc(index)
    }
  }
}
</script>
