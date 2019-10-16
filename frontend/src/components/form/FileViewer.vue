<template>
  <div>
    <pre style="overflow-x: auto;">{{shownFileContent}}</pre>
  </div>
</template>

<script>
export default {
  props: ['attachmentId'],
  data() {
    return {
      shownFileContent: null
    }
  }
}
</script>
