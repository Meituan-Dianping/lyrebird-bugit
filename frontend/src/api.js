import axios from 'axios'

const API_PREFIX = '/plugins/bugit/api'

export const getTemplate = (path) => {
  let url = API_PREFIX + '/template'
  if (path) {
    return axios({
      url: url,
      method: 'POST',
      data: { path }
    })
  } else {
    return axios({
      url: url
    })
  }
}

export const getDevices = () => {
  return axios({
    url: API_PREFIX + '/device'
  })
}

//------EventInspector------

export const getEvent = (options) => {
  let url = '/api/event'
  if (options && options.hasOwnProperty('channelFilters') && options.channelFilters.length > 0) {
    url += '/' + options.channelFilters.join('+')
  }
  if (options && options.hasOwnProperty('eventId') && options.eventId) {
    url += '/id/' + options.eventId
  } else if (options && options.hasOwnProperty('page') && options.page) {
    url += '/page/' + options.page
  }
  return axios({
    url: url
  })
}

export const getDefaultChannelNames = () => {
  return axios({
    url: '/api/channel/default'
  })
}

export const saveImage = (id, imageData) => {
  return axios({
    url: API_PREFIX + '/attachments/' + id,
    method: 'PUT',
    data: { imageData }
  })
}

export const createIssue = (templateInfo, issue, attachments, snapshots) => {
  return axios({
    url: API_PREFIX + '/issue',
    method: 'POST',
    data: {
      template: templateInfo,
      issue,
      attachments,
      snapshots
    }
  })
}

export const takeScreenshot = (platform, deviceId) => {
  return axios({
    url: API_PREFIX + '/take_screenshot/' + platform + '/' + deviceId
  })
}

export const getAttachments = () => {
  return axios({
    url: API_PREFIX + '/attachments'
  })
}

export const getAttachment = (id) => {
  return axios({
    url: API_PREFIX + '/attachments/' + id
  })
}

export const removeAttachment = (id) => {
  return axios({
    url: API_PREFIX + '/attachments/' + id,
    method: 'DELETE'
  })
}

export const getCache = (key) => {
  return axios({
    url: API_PREFIX + '/cache/' + key
  })
}

export const setCache = (key, data) => {
  return axios({
    url: API_PREFIX + '/cache/' + key,
    method: 'POST',
    data: data
  })
}
