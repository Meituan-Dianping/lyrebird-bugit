<template>
  <div>
    <Row>
      <i-col span="2">
        <ButtonGroup vertical>
          <Button @click="setMode('text')" :type="btnType('text')">
            <b>T</b>
          </Button>
          <Button icon="md-brush" @click="setMode('brush')" :type="btnType('brush')"></Button>
          <Button icon="md-undo" @click="undo" :class="undoButtonClass"></Button>
        </ButtonGroup>
      </i-col>
      <i-col span="20" style="text-align:center;padding:10px;">
        <canvas
          ref="canvas"
          v-on:mousedown="handleMouseDown"
          v-on:mousemove="handleMouseMove"
          v-on:mouseup="handleMouseUp"
          :style="{ cursor: canvasStyle}"
        />
        <input
          ref="textInput"
          v-show="isTextInputShown"
          v-model="inputText"
          width="120px"
          style="position: absolute"
          :style="{left:inputLeft, top:inputTop}"
          @keyup.enter="addText"
        >
      </i-col>
    </Row>
  </div>
</template>

<script>
export default {
  props: ['src', 'attachmentId'],
  data () {
    return {
      activatedMode: 'brush',
      history: [],
      currentPath: null,
      canvasBounds: null,
      inputText: '',
      isTextInputShown: false,
      inputLeft: '50%',
      inputTop: '50%',
      canvas: null,
      ctx: null,
      img: null
    }
  },
  mounted () {
    this.canvas = this.$refs.canvas
    this.canvas.addEventListener('resize', () => { console.log('resize') })
    this.ctx = this.canvas.getContext('2d')
    this.ctx.imageSmoothingEnabled = false
    this.img = new Image()
    let scaleCanvas = this.scaleCanvas
    let drawBackground = this.drawBackground
    this.img.onload = () => {
      scaleCanvas()
      drawBackground()
    }
    this.img.src = this.src
  },
  watch: {
    src () {
      this.inputText = ''
      this.isTextInputShown = false
      this.img.src = this.src
    }
  },
  created () {
    this.$bus.$on('saveImage', this.save)
  },
  computed: {
    canvasStyle () {
      if (this.activatedMode === 'brush') {
        return 'crosshair'
      } else if (this.activatedMode === 'text') {
        return 'text'
      } else {
        return 'pointer'
      }
    },
    undoButtonClass () {
      return { disabled: (this.history.length <= 0) }
    }
  },
  methods: {
    showTextInput (isShown, mouseEvent) {
      const textPosition = this.event2position(mouseEvent)
      this.inputLeft = mouseEvent.clientX - this.canvasBounds.left + this.canvas.offsetLeft + 'px'
      this.inputTop = mouseEvent.clientY - this.canvasBounds.top + 'px'
      this.textX = textPosition.x
      this.textY = textPosition.y
      this.isTextInputShown = isShown
      this.$nextTick(() => {
        this.$refs.textInput.focus()
      })
    },
    btnType (name) {
      if (name === this.activatedMode) {
        return 'primary'
      } else {
        return 'default'
      }
    },
    setMode (mode) {
      this.activatedMode = mode
      if (mode !== 'text') {
        this.isTextInputShown = false
      }
    },
    undo () {
      if (this.history.length <= 0) {
        return
      }
      this.clearCanvas()
      this.drawBackground()

      this.history.pop()

      for (const action of this.history) {
        if (action.name === 'path') {
          this.ctx.beginPath()

          for (let index = 0; index < action.data.length; index++) {
            const point = action.data[index]
            if (index === 0) {
              this.ctx.moveTo(point.x, point.y)
            } else {
              this.ctx.lineTo(point.x, point.y)
            }
          }
          this.ctx.strokeStyle = '#FF0000'
          this.ctx.lineWidth = 5
          this.ctx.stroke()
          this.ctx.closePath()
        } else if (action.name === 'text') {
          this.ctx.font = 'normal normal 36pt Verdana'
          this.ctx.fillStyle = '#FF0000'
          this.ctx.fillText(action.data.text, action.data.x, action.data.y)
        }
      }
    },
    event2position (event) {
      return {
        x: (event.clientX - this.canvasBounds.left) * this.ratio * this.ratio,
        y: (event.clientY - this.canvasBounds.top) * this.ratio * this.ratio
      }
    },
    scaleCanvas () {
      this.canvas.width = 250
      this.canvas.height = this.canvas.width * this.img.height / this.img.width

      var ratio = this.getPixelRatio(this.ctx)
      this.ratio = ratio

      this.canvas.style.width = this.canvas.width + 'px'
      this.canvas.style.height = this.canvas.height + 'px'
      this.canvas.width = this.canvas.width * ratio
      this.canvas.height = this.canvas.height * ratio

      this.ctx.scale(1 / ratio, 1 / ratio)
    },
    clearCanvas () {
      this.ctx.clearRect(0, 0, this.canvas.width * this.ratio, this.canvas.height * this.ratio)
    },
    drawBackground () {
      this.ctx.drawImage(
        this.img,
        0,
        0,
        this.img.width,
        this.img.height,
        0,
        0,
        this.canvas.width * this.ratio,
        this.canvas.height * this.ratio
      )
      this.canvasBounds = this.canvas.getBoundingClientRect()
    },
    handleMouseDown (event) {
      if (this.activatedMode === 'brush') {
        this.canvasBounds = this.canvas.getBoundingClientRect()
        this.ctx.beginPath()
        const point = this.event2position(event)
        this.ctx.moveTo(point.x, point.y)
        this.currentPath = { name: 'path', data: [point] }
      }
    },
    handleMouseUp (event) {
      if (this.activatedMode === 'brush') {
        this.ctx.closePath()
        this.history.push(this.currentPath)
        this.currentPath = null
      } else if (this.activatedMode === 'text') {
        this.showTextInput(true, event)
      }
    },
    handleMouseMove (event) {
      if (this.activatedMode === 'brush' && event.buttons === 1) {
        const point = this.event2position(event)
        this.ctx.lineTo(point.x, point.y)
        this.ctx.strokeStyle = '#FF0000'
        this.ctx.lineWidth = 5
        this.ctx.stroke()

        if (this.currentPath) {
          this.currentPath.data.push(point)
        }
      }
    },
    addText () {
      this.ctx.font = 'normal normal 36pt Verdana'
      this.ctx.fillStyle = '#FF0000'
      this.ctx.fillText(this.inputText, this.textX, this.textY)
      this.history.push({ name: 'text', data: { text: this.inputText, x: this.textX, y: this.textY } })
      this.isTextInputShown = false
      this.inputText = ''
    },
    save () {
      this.$store.dispatch('saveEditedImage', {
        id: this.attachmentId,
        imageData: this.canvas.toDataURL('image/png')
      })
    },
    getPixelRatio (context) {
      var backingStore =
        context.backingStorePixelRatio ||
        context.webkitBackingStorePixelRatio ||
        context.mozBackingStorePixelRatio ||
        context.msBackingStorePixelRatio ||
        context.oBackingStorePixelRatio ||
        context.backingStorePixelRatio ||
        1
      return (window.devicePixelRatio || 1) / backingStore
    }
  }
}
</script>

<style>
.flex_input {
  position: absolute;
}
</style>
