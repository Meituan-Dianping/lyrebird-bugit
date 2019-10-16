import * as api from '@/api'
import { bus } from '@/eventbus'

export default {
  state: {

  },
  actions: {
    takeScreenshot (ctx, options) {
      api.takeScreenshot(options.platform, options.deviceId)
        .then(resp => {
          console.log('Take screenshot', resp)
          bus.$emit('message', resp.data)
        })
    }
  }
}
