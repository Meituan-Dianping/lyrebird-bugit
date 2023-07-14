<template>
  <div>
    <Upload
      multiple
      action="/plugins/bugit/api/attachments"
      :format="['jpg','jpeg','png']"
      accept=".jpg,.jpeg,.png"
      :show-upload-list="false"
      :before-upload="loadingFile"
      :on-success="handleSuccess"
      :on-error="handleError"
      style="display: none;"
      >
      <Button id="self-defined-upload"></Button>
    </Upload>
    <quill-editor
      v-model="data.value"
      ref="myQuillEditor"
      :options="editorOption"
      style="background-color: white; white-space: normal;"
      >
    </quill-editor>
  </div>
</template>

<script>
export default {
  props: ['data'],
  data () {
    return {
      editorOption: {
        modules: {
          toolbar: {
            container: [
              ['clean'],
              ['bold', 'italic', 'underline', 'strike'],
              [{ 'header': 1 }, { 'header': 2 }],
              [{ 'script': 'sub' }, { 'script': 'super' }],
              [{ 'direction': 'rtl' }],
              [{ 'list': 'ordered' }, { 'list': 'bullet' }],
              [{ 'indent': '-1' }, { 'indent': '+1' }],
              ['image']
            ],
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
        },
        placeholder: 'Enter your description...'
      }
    }
  },
  created () {
    this.data.value = this.data.value.replace(/\n/g, '<br>')
  },
  mounted () {
    this.quill = this.$refs.myQuillEditor.quill
    this.initEvent()
    this.$store.commit('setDescValue', this.quill)
  },
  methods: {
    loadingFile () {
      this.loadingMsg = this.$Message.loading({
        content: 'Loading image...',
        duration: 0
      })
    },
    handleSuccess (response, file, fileList) {
      this.$store.dispatch('updateImgToDesc', file)
      setTimeout(this.loadingMsg, 10)
    },
    handleError (error, file) {
      this.$bus.$emit('msg.error', 'Import ' + file.name + ' error: ' + error)
      setTimeout(this.loadingMsg, 10)
    },
    initEvent () {
      this.quill.on('text-change', this.deleteImg)
    },
    deleteImg (delta, oldDelta) {
      let deleteContent = ''
      // move operation: insert-retain-delete or retain-delete-retain-insert
      // add operation: insert or retain-insert
      // delete operation: delete or retain-delete [watched]
      if (delta.ops.length === 1 && 'delete' in delta.ops[0]) {
        deleteContent = oldDelta.slice(0, 1).ops[0].insert
      }
      if (delta.ops.length === 2 && 'delete' in delta.ops[1]) {
        const idx = delta.ops[0].retain
        deleteContent = oldDelta.slice(idx, idx + 1).ops[0].insert
      }
      if (typeof (deleteContent) === 'object' && 'image' in deleteContent) {
        const deleteImgId = String(deleteContent.image.split('/').slice(-1))
        this.$store.dispatch('removeAttachmentById', deleteImgId)
      }
    }
  }
}
</script>

<style>
.ql-snow.ql-container {
  height: 300px;
}
</style>
