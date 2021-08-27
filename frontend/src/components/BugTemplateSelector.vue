<template>
  <Form :label-width="80" class="split-left-template-selector">
    <Row>
      <i-col span="12">
        <FormItem label="template">
          <Select
            v-model="selectedTemplateIndex"
            filterable
            size="small"
            placeholder="Select template"
          >
            <Option
              v-for="(template, index) in templates"
              :value="index"
              :key="index"
              >{{ template.name }}</Option
            >
          </Select>
        </FormItem>
      </i-col>
      <i-col span="12">
        <FormItem label="draft">
          <Select
            v-model="selectedDraft"
            size="small"
            placeholder="Select draft"
          >
            <Option
              v-for="(template, index) in cacheList"
              :value="template.cache_name"
              :key="index"
              >{{ template.cache_name
              }}<Icon
                v-if="template.cache_name==selectedCache"
                class="icon-form"
                style="float: right"
                type="md-trash"
                @click="deleteDraft(template.cache_name)"
            /></Option>
          </Select>
          <Modal v-model="shownDeleteModal">
            <p slot="header" style="color: #f60; text-align: center">
              <Icon type="ios-information-circle"></Icon>
              <span>Delete confirmation</span>
            </p>
            <div style="text-align: center">
              <span style="font-size: 14px">
                Are you sure you want to delete {{selectedCache}}?</span
              >
            </div>
            <div slot="footer">
              <Button type="error" size="large" @click="onDelete()"
                >Delete</Button
              >
            </div>
          </Modal>
        </FormItem>
      </i-col>
    </Row>
  </Form>
</template>

<script>
export default {
  data() {
    return {
      shownDeleteModal: false,
      targetDeleteCache: null,
    };
  },
  created() {
    this.$store.dispatch("loadTemplateList");
  },
  methods: {
    deleteDraft(template) {
      this.targetDeleteCache = template
      this.shownDeleteModal = true;
    },
    onDelete() {
      this.shownDeleteModal = false;
      this.$store.dispatch('deleteCache', this.targetDeleteCache)
    },
  },
  computed: {
    templates() {
      return this.$store.state.form.templates;
    },
    selectedCache() {
      return this.$store.state.form.selectedCache;
    },
    cacheList() {
      return this.$store.state.form.cacheList;
    },
    selectedTemplateIndex: {
      get() {
        return this.$store.state.form.selectedTemplateIndex;
      },
      set(val) {
        this.$store.dispatch("updateSelectedTemplateIndex", val);
      },
    },
    selectedDraft: {
      get() {
        return this.$store.state.form.selectedCache;
      },
      set(val) {
        if (val !== undefined) {
          this.$store.commit("setSelectedCache", val);
          this.$store.dispatch("loadTemplate");
        }
      },
    }
  },
};
</script>

<style scoped>
.split-left-template-selector {
  padding-right: 10px;
  background-color: #f8f8f9;
}
.split-left-template-selector .ivu-form-item {
  margin-bottom: 0px;
  padding-bottom: 5px;
}
.input-dropdown {
  height: 18px;
}
</style>
