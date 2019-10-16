import Vue from 'vue'
import Vuex from 'vuex'
import * as api from '@/api'
import form from '@/store/form'
import event from '@/store/event'
import device from '@/store/device'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    form,
    event,
    device
  },
  state: {
    devicesInfo: null
  },
  mutations: {
    updateDevicesInfo (state, devicesInfo) {
      state.devicesInfo = devicesInfo
    }
  },
  actions: {
    loadDevices ({ commit }) {
      api.getDevices().then(response => {
        commit('updateDevicesInfo', response.data)
      })
    }
  }
})
