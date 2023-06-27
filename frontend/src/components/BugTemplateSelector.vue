<template>
  <Form :label-width="80" class="split-left-template-selector">
    <Row>
      <i-col span="12">
        <FormItem label="Template">
          <Select
            v-model="selectedTemplateIndex"
            filterable
            size="small"
            placeholder="Select template"
            not-found-text="No Template"
          >
            <Option v-for="(template, index) in templates" :value="index" :key="index">{{ template.name }}</Option>
          </Select>
        </FormItem>
      </i-col>
      <i-col span="12">
        <FormItem label="Draft">
          <Select
            v-model="selectedDraft"
            filterable
            clearable
            size="small"
            placeholder="Select a saved draft"
            not-found-text="No saved draft"
          >
            <Option
              v-for="(template, index) in cacheList"
              :value="template.cacheName"
              :key="index"
              class="draft-option"
            >{{template.cacheName}}<Icon
              v-show="template.cacheName===selectedCache"
              class="delete-icon"
              type="md-trash"
              @click="isShownDeleteModal = true"
              />
            </Option>
          </Select>
        </FormItem>
      </i-col>
    </Row>
    <Modal v-model="isShownDeleteModal">
      <p slot="header" style="color: #f60; text-align: center">
        <Icon type="ios-information-circle"/>
        <span>Delete confirmation</span>
      </p>
      <div style="text-align: center">
        <span style="font-size: 14px">
          Are you sure you want to delete draft <b>{{selectedCache}}</b>?
        </span>
      </div>
      <div slot="footer">
        <Button type="error" long @click="onDelete">Delete</Button>
      </div>
    </Modal>
  </Form>
</template>

<script>
export default {
  data () {
    return {
      isShownDeleteModal: false
    }
  },
  created () {
    this.$store.dispatch('loadTemplateList')
  },
  methods: {
    onDelete () {
      this.$store.dispatch('deleteCache', this.selectedCache)
      this.isShownDeleteModal = false
    }
  },
  computed: {
    templates () {
      return this.$store.state.form.templates
    },
    selectedCache () {
      return this.$store.state.form.selectedCache
    },
    cacheList () {
      return this.$store.state.form.cacheList
    },
    selectedTemplateIndex: {
      get () {
        return this.$store.state.form.selectedTemplateIndex
      },
      set (val) {
        this.$store.dispatch('updateSelectedTemplateIndex', val)
      }
    },
    selectedDraft: {
      get () {
        return this.$store.state.form.selectedCache
      },
      set (val) {
        if (val !== undefined) {
          this.$store.commit('setSelectedCache', val)
          this.$store.dispatch('loadTemplate')
        }
      }
    }
  }
}
</script>

<style scoped>
.split-left-template-selector {
  padding-right: 10px;
  background-color: #ffffff;
}
.split-left-template-selector .ivu-form-item {
  margin-bottom: 0px;
  padding-bottom: 5px;
}
.draft-option {
  white-space: normal;
  position: relative;
}
.delete-icon {
  position: absolute;
  bottom: 10px;
  margin: auto;
}
</style>
