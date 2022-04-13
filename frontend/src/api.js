import axios from 'axios'

const API_PREFIX = '/plugins/bugit/api'

export const getTemplate = (path, cacheName) => {
  let url = API_PREFIX + '/template'
  if (path) {
    return axios({
      url: url,
      method: 'POST',
      data: { path, cache_name: cacheName }
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

// ------EventInspector------

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

export const renameAttachment = (id, newName) => {
  return axios({
    url: API_PREFIX + '/attachments/' + id,
    method: 'POST',
    data: { newName }
  })
}

export const getCache = (key) => {
  return axios({
    url: API_PREFIX + '/cache/' + key
  })
}

export const setCache = (key, templatePath, cacheName, data) => {
  return axios({
    url: API_PREFIX + '/cache/' + key,
    method: 'POST',
    data: {
      template_path: templatePath,
      cache_name: cacheName,
      data
    }
  })
}

export const deleteCache = (key, templatePath, cacheName) => {
  return axios({
    url: API_PREFIX + '/cache/' + key,
    method: 'DELETE',
    data: {
      cache_name: cacheName,
      template_path: templatePath
    }
  })
}
