<template>
  <Form :label-width="80" class="split-left-template-selector">
    <Row>
    <i-col span="12">
    <FormItem label="template">
      <Select v-model="selectedTemplateIndex" filterable size="small" placeholder="Select template">
        <Option v-for="(template, index) in templates" :value="index" :key="index">{{template.name}}</Option>
      </Select>
    </FormItem>
    </i-col>
    <i-col span="12">
    <FormItem label="draft">
      <Select v-model="selectedDraft" size="small" placeholder="Select draft">
        <Option v-for="(template, index) in cacheList" :value="template.cache_name" :key="index">{{template.cache_name}}<Icon disabled class="icon-form" style="float:right;" type="md-trash" @click.stop="deleteDraft(template.cache_name)" /></Option>
      </Select>
      <Modal v-model="shownDeleteModal">
        <p slot="header" style="color: #f60; text-align: center">
          <Icon type="ios-information-circle"></Icon>
          <span>Delete confirmation</span>
        </p>
        <div style="text-align: center">
          <span style="font-size: 14px"> Are you sure you want to delete?</span>
        </div>
        <div slot="footer">
          <Button type="error" size="large" @click.stop="onDelete()">Delete</Button>
        </div>
      </Modal>
    </FormItem>
    </i-col>
    </Row>
  </Form>
</template>

<script>
export default {
  data () {
    return {
      // selectedDraftIndex: null,
      shownDeleteModal: false,
      targetDeleteCache: null,
      items: ['Foo', 'Bar', 'Fizz', 'Buzz'],
    }
  },
  created() {
    this.$store.dispatch('loadTemplateList')
  },
  methods: {
    deleteDraft(template) {
      this.shownDeleteModal = true
      this.targetDeleteCache = template
    },
    onDelete() {
      this.shownDeleteModal = false
      this.$store.dispatch('deleteCache', this.targetDeleteCache)
    }
  },
  computed: {
    templates() {
      console.log('templates getter' + this.$store.state.form.templates);
      return this.$store.state.form.templates
    },
    cacheList() {
      console.log('cachelist', this.$store.state.form.cacheList)
      return this.$store.state.form.cacheList
    },
    selectedTemplateIndex: {
      get() {
        return this.$store.state.form.selectedTemplateIndex
      },
      set(val) {
        this.$store.dispatch('updateSelectedTemplateIndex', val)
      }
    },
    selectedDraft: {
      get() {
        console.log('selectedDraft getter!!!!!!!!', this.$store.state.form.selectedCache)
        return this.$store.state.form.selectedCache
      },
      set(val) {
        console.log('selectedDraft setter?????????', val)
        // this.$store.dispatch('updateSelectedCache', val)
        if (val !== undefined || !this.shownDeleteModal) {
          this.$store.commit('setSelectedCache', val)
          this.$store.dispatch('loadTemplate')
        }
        // this.$store.dispatch('loadTemplate')
      }
    }
  }
}
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
.icon-forn {

}
</style>
