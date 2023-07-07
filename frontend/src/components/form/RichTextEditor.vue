<template>
  <div>
    <Upload
      multiple
      action="/plugins/bugit/api/attachments"
      :format="['jpg','jpeg','png']"
      accept=".jpg,.jpeg,.png"
      :show-upload-list="false"
      :on-success="handleSuccess"
      style="display: none;"
      >
      <Button id="self-defined-upload"></Button>
    </Upload>
    <quill-editor
      v-model="data.value"
      ref="myQuillEditor"
      :options="editorOption"
      style="background-color: white;"
      >
    </quill-editor>
  </div>
</template>

<script>
const toolbarContainerOptions = [
  ['clean'],
  ['bold', 'italic', 'underline', 'strike'],
  [{ 'header': 1 }, { 'header': 2 }],
  [{ 'script': 'sub' }, { 'script': 'super' }],
  [{ 'direction': 'rtl' }],
  [{ 'list': 'ordered' }, { 'list': 'bullet' }],
  [{ 'indent': '-1' }, { 'indent': '+1' }],
  ['image']
]
var toolbarOptions = {
  container: toolbarContainerOptions,
  handlers: {
    'image': function (value) {
      if (value) {
        document.querySelector('#self-defined-upload').click()
      } else {
        this.quill.format('image', false)
      }
    }
  }
}
export default {
  props: ['data'],
  data () {
    return {
      editorOption: {
        modules: {
          toolbar: toolbarOptions
        }
      },
      placeholder: 'Enter your description...'
    }
  },
  mounted () {
    const descValue = this.$refs.myQuillEditor.quill
    this.$store.commit('setDescValue', descValue)
  },
  methods: {
    handleSuccess (response, file, fileList) {
      this.$store.dispatch('updateImgToDesc', file)
    }
  }
}
</script>

<style>
.ql-snow.ql-container {
  height: 300px;
}
</style>
