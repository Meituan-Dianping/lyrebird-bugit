<template>
  <div class="split-right-bar">
    <p style="line-height:28px;vertical-align:middle;">
      <span style="padding-left:10px;padding-right:10px">
        <b>Devices:</b>
      </span>
      <span v-if="noneDevices">
        <b>N/A - Please connect your phone to your computer using a USB cable</b>
      </span>
      <span v-for="(device, index) in devicesInfo" :key="index" class="device-btn-group">
        <a @click="addDevice(device)" class="device-btn">
          <Tooltip max-width="400" placement="bottom-end">
            <span>
              <Icon v-if="device.platform === 'Android'" type="logo-android"/>
              <Icon v-else type="logo-apple"/>
              {{device.info.model}}
            </span>
            <div slot="content">
              <p>Click to add the following info to description</p>
              <p>-----------------------------------------------------------</p>
              <Row v-for="(value, key) in device.info" :key="key" style="width:200px">
                <i-col span="9" v-if="value">
                  <b v-if="DeviceInfoAllUpperKey.indexOf(key) > -1" style="float: right">{{key.toUpperCase()}}</b>
                  <b v-else style="float: right">{{key.charAt(0).toUpperCase() + key.slice(1)}}</b>
                </i-col>
                <i-col span="14" offset="1">{{value}}</i-col>
              </Row>
            </div>
          </Tooltip>
        </a>
        <a class="screenshot-btn" @click="takeScreenshot(device)">
          <Tooltip placement="bottom-end">
            <Icon type="md-images"/>
            <div slot="content">Take a screenshot</div>
          </Tooltip>
        </a>
      </span>
    </p>
  </div>
</template>

<script>
export default {
  created () {
    this.loadDevices()
    this.$io.on('devices', this.loadDevices)
  },
  data () {
    return {
      DeviceInfoAllUpperKey: ['os', 'sn', 'ip']
    }
  },
  computed: {
    devicesInfo () {
      return this.$store.state.devicesInfo
    },
    noneDevices () {
      return this.devicesInfo === null || this.devicesInfo.length === 0
    }
  },
  methods: {
    addDevice (device) {
      let msg = 'Model: ' + device.info.model + '\nVersion: ' + device.info.os + '\n'
      if (device.app) {
        msg += 'App: ' + device.app.packageName + '\nApp version: ' + device.app.version + '\n'
        if (device.app.build) {
          msg += 'BundleID: ' + device.app.build + '\n'
        }
      }
      this.$bus.$emit('addMessage', {
        channel: device.platform,
        message: msg
      })
    },
    takeScreenshot (device) {
      this.$store.dispatch('takeScreenshot', { platform: device.platform, deviceId: device.id })
    },
    loadDevices () {
      this.$store.dispatch('loadDevices')
    }
  }
}
</script>

<style scoped>
.split-right-bar {
  height: 28px;
  overflow-x: auto;
  overflow-y: hidden;
  white-space: nowrap;
  border-bottom: 1px solid #dcdee2;
}
.device-btn-group {
  margin: 2px 2px;
}
.device-btn {
  border: 1px solid #c3d9ee;
  border-radius: 3px 0 0 3px;
  background: #ffffff;
  cursor: pointer;
  padding: 2px 5px;
}
.screenshot-btn {
  border: 1px solid #c3d9ee;
  border-left: 0;
  border-radius: 0 3px 3px 0;
  background: #ffffff;
  cursor: pointer;
  padding: 2px 5px;
}
</style>
