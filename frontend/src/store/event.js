import * as api from '@/api'
import { bus } from '@/eventbus'

export default {
  state: {
    channelNames: [],
    channelFilters: ['flow', 'notice', 'snapshot'],
    events: [],
    loadingEvents: false,
    selectedEventId: null,
    eventDetail: '',
    page: null,
    searchStr: ''
  },
  mutations: {
    setChannelNames (state, channelNames) {
      state.channelNames = channelNames
    },
    setChannelFilters (state, filters) {
      state.channelFilters = filters
    },
    setEvents (state, events) {
      state.events = events
    },
    setLoadingEvents (state, isLoading) {
      state.loadingEvents = isLoading
    },
    setSelectedEventId (state, eventId) {
      state.selectedEventId = eventId
    },
    setEventDetail (state, eventDetail) {
      state.eventDetail = eventDetail
    },
    setPage (state, page) {
      state.page = page
    },
    setSearchStr (state, searchStr) {
      state.searchStr = searchStr
    }
  },
  actions: {
    loadChannelNames ({ commit }) {
      // Filter out the target channel
      api.getDefaultChannelNames().then(response => {
        if (response.data.code === 1000) {
          commit('setChannelNames', response.data.data)
        }
      })
    },
    loadEvents ({ state, commit }, options = {}) {
      let eventId = null
      if (options.eventId) {
        eventId = options.eventId
      } else if (state.selectedEventId) {
        eventId = state.selectedEventId
      }
      commit('setLoadingEvents', true)
      api.getEvent({
        channelFilters: state.channelFilters,
        eventId: eventId,
        page: options.page,
        searchStr: state.searchStr
      }).then(response => {
        if (response.data.code === 1000) {
          let events = response.data.events
          if (eventId) {
            let i = 1
            for (const event of events) {
              if (event.event_id === eventId) {
                event._highlight = true
                const prettyJson = JSON.stringify(JSON.parse(event.content), null, 2)
                commit('setEventDetail', prettyJson)
                commit('setSelectedEventId', event.event_id)
                bus.$emit('eventLitScroll', i / events.length)
                break
              }
              i++
            }
          }
          commit('setEvents', events)
          commit('setPage', {
            index: response.data.page, count: response.data.page_count, size: response.data.page_size
          })
          commit('setLoadingEvents', false)
        }
      })
    },
    updateChannelFilters ({ commit, dispatch }, filters) {
      commit('setChannelFilters', filters)
      dispatch('loadEvents')
    },
    showNotice ({ dispatch }) {
      dispatch('updateChannelFilters', ['notice'])
    },
    showAll ({ dispatch }) {
      api.getDefaultChannelNames().then(response => {
        if (response.data.code === 1000) {
          dispatch('updateChannelFilters', response.data.data)
        }
      })
    }
  }
}
