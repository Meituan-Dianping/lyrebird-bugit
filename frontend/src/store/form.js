import * as api from '@/api'
import { bus } from '@/eventbus'

export default {
  state: {
    templates: [],
    cacheList: [],
    selectedTemplateIndex: null,
    selectedCache: null,
    templateDetail: null,
    formInfo: null,
    ruleValidate: null,
    formValue: {},
    attachmentsList: [],
    inEditModeAttachments: [],
    snapshotList: [],
    loadAttachmentCount: 0,
    shownFileName: null,
    submitLock: false,
    loadTemplate: false,
    shownDraftNameModal: false,
    createName: 'Default',
    shownFileContent: {
      code: null,
      type: null,
      message: null
    },
    'illegalChars': [':', '/']
  },
  mutations: {
    setFormData (state, sourceData) {
      state.templateDetail[sourceData.index].value = sourceData.value
    },
    setTemplates (state, templates) {
      state.templates = templates
    },
    setCacheList (state, cacheList) {
      state.cacheList = cacheList
    },
    setSelectedTemplateIndex (state, selectedTemplateIndex) {
      state.selectedTemplateIndex = selectedTemplateIndex
    },
    setSelectedCache (state, selectedCache) {
      state.selectedCache = selectedCache
    },
    setTemplateDetail (state, templateDetail) {
      state.templateDetail = templateDetail
    },
    setSubmitLock (state, isLock) {
      state.submitLock = isLock
    },
    setLoadTemplate (state, isLoad) {
      state.loadTemplate = isLoad
    },
    setShownDraftNameModal (state, shownDraftNameModal) {
      state.shownDraftNameModal = shownDraftNameModal
    },
    setCreateName (state, createName) {
      state.createName = createName
    },
    updateFormInfo (state, template) {
      for (let i in state.metadata) {
        if (state.metadata[i].key === template) {
          state.formInfo = state.metadata[i]
          state.ruleValidate = state.metadata[i].rules
        }
      }
    },
    updateRuleValidate (state, ruleValidate) {
      state.ruleValidate = ruleValidate
    },
    updateFormValue (state, formValue) {
      state.formValue = formValue
    },
    deleteFormValue (state, formValue) {
      state.formValue = {}
    },
    updateExtraMsg (state, msg) {
      state.templateDetail[msg.index].extraMsg = msg.value
    },
    addExtraMsg (state, msg) {
      let value = msg.value
      state.templateDetail[msg.index].extraMsg.push(value)
    },
    deleteExtraMsg (state, indexes) {
      state.templateDetail[indexes.propsIndex].extraMsg.splice(indexes.index, 1)
    },
    recordInEditModeAttachments (state) {
      state.inEditModeAttachments = []
      for (const i in state.attachmentsList) {
        if (state.attachmentsList[i].editMode === true) {
          state.inEditModeAttachments.push(state.attachmentsList[i].id)
        }
      }
    },
    updateAttachmentsList (state, attachmentsList) {
      for (const i in attachmentsList) {
        let id = attachmentsList[i].id
        if (state.inEditModeAttachments.indexOf(id) > -1) {
          attachmentsList[i].editMode = true
        } else {
          attachmentsList[i].editMode = false
        }
      }
      state.attachmentsList = attachmentsList
    },
    updateShownFileName (state, name) {
      state.shownFileName = name
    },
    updateShownFileContent (state, fileInfo) {
      state.shownFileContent = fileInfo
    },
    deleteAttachment (state, index) {
      state.attachmentsList.splice(index, 1)
    },
    setAttachmentEditMode (state, { index, mode }) {
      state.attachmentsList[index].editMode = mode
    },
    addSnapshot (state, snapshot) {
      let fileName = 'snapshot_' + snapshot.id
      state.snapshotList.push({
        'name': fileName,
        'editMode': false,
        'eventObj': snapshot
      })
    },
    deleteSnapshot (state, index) {
      state.snapshotList.splice(index, 1)
    },
    setSnapshotName (state, { index, newName }) {
      state.snapshotList[index].name = newName
    },
    setSnapshotEditMode (state, { index, mode }) {
      state.snapshotList[index].editMode = mode
    }
  },
  actions: {
    loadTemplateList ({ commit, dispatch }) {
      api.getTemplate().then(response => {
        if (response.data.code === 1000) {
          commit('setSelectedTemplateIndex', response.data.selected_template_index)
          commit('setTemplates', response.data.templates)
          commit('setSelectedCache', response.data.selected_cache)
          commit('setCacheList', response.data.drafts)
          dispatch('loadTemplate')
        } else {
          bus.$emit('msg.error', response.data.message)
        }
      })
    },
    loadCacheList ({ state, commit }) {
      if (state.selectedTemplateIndex === null) {
        return
      }
      const selectedTemplate = state.templates[state.selectedTemplateIndex]
      api.getCache(selectedTemplate.id)
        .then(response => {
          if (response.data.code === 1000) {
            commit('setCacheList', response.data.data)
          } else {
            bus.$emit('msg.error', 'Load draft error: ' + response.data.message)
          }
        }).catch(error => {
          bus.$emit('msg.error', 'Load draft error: ' + error)
        })
    },
    loadTemplate ({ state, commit }) {
      if (state.selectedTemplateIndex === null) {
        return
      }
      const path = state.templates[state.selectedTemplateIndex].path
      commit('setTemplateDetail', [])
      commit('setLoadTemplate', true)
      api.getTemplate(path, state.selectedCache).then(response => {
        commit('setTemplateDetail', response.data)
        commit('setLoadTemplate', false)
      }).catch(error => {
        bus.$emit('message', 'Load template detail error: ' + error)
        commit('setLoadTemplate', false)
      })
    },
    updateSelectedTemplateIndex ({ commit, dispatch, state }, selectedTemplateIndex) {
      commit('setSelectedTemplateIndex', selectedTemplateIndex)
      commit('setSelectedCache', null)
      dispatch('loadCacheList')
      dispatch('loadTemplate')
    },
    setExtraMsgUpward ({ state, commit }, indexes) {
      let descFormEventbus = state.templateDetail[indexes.propsIndex].extraMsg
      let index = indexes.index
      let upDesc = descFormEventbus[index]
      descFormEventbus.splice(index, 1)
      let newDescFormEventbus = []
      for (let i = 0; i < descFormEventbus.length; i++) {
        if (i === index - 1) {
          newDescFormEventbus.push(upDesc)
        }
        newDescFormEventbus.push(descFormEventbus[i])
      }
      commit('updateExtraMsg', { index: indexes.propsIndex, value: newDescFormEventbus })
    },
    saveEditedImage ({ state, commit }, { id, imageData }) {
      api.saveImage(id, imageData)
    },
    submit ({ state, commit }) {
      bus.$emit('message', 'Submitting issue ...')
      commit('setSubmitLock', true)
      api.createIssue(state.templates[state.selectedTemplateIndex], state.templateDetail,
        state.attachmentsList, state.snapshotList)
        .then(response => {
          bus.$emit('message', response.data)
          commit('setSubmitLock', false)
        }).catch(response => {
          bus.$emit('message', response.data)
          commit('setSubmitLock', false)
        })
    },
    loadAttachment ({ state, commit }) {
      commit('recordInEditModeAttachments')
      api.getAttachments().then(response => {
        commit('updateAttachmentsList', response.data)
        if (state.attachmentsList.length > 0 && state.loadAttachmentCount > 0) {
          const index = state.attachmentsList.length - 1
          bus.$emit('displayAttach', state.attachmentsList[index])
        }
        state.loadAttachmentCount += 1
      })
    },
    removeAttachment ({ commit }, attachment) {
      commit('deleteAttachment', attachment.index)
      api.removeAttachment(attachment.id)
    },
    isNameValid ({ state }, name) {
      if (!name || name.trim().length === 0) {
        return Promise.reject('File name cannot be empty')
      }
      for (const i in state.illegalChars) {
        if (name.indexOf(state.illegalChars[i]) > -1) {
          return Promise.reject(`Illegal character [${state.illegalChars[i]}] in file name.`)
        }
      }
      return Promise.resolve()
    },
    isNameNotExists ({ state }, { name, sourceList, index }) {
      for (let i in sourceList) {
        if (sourceList[i].name.toLowerCase() === name.toLowerCase() && i.toString() !== index.toString()) {
          return Promise.reject('A file with the same name exists')
        }
      }
      return Promise.resolve()
    },
    renameAttachment ({ state, commit, dispatch }, { index, baseName, extensionName }) {
      dispatch('isNameValid', baseName).then(() => {
        let newName = `${baseName}.${extensionName}`
        dispatch('isNameNotExists', {
          name: newName,
          sourceList: state.attachmentsList,
          index: index
        }).then(() => {
          let attachment = state.attachmentsList[index]
          api.renameAttachment(attachment.id, newName)
            .then(response => {
              if (response.data.code !== 1000) {
                bus.$emit('msg.error', response.data.message)
                return
              }
              commit('setAttachmentEditMode', {
                index: index,
                mode: false
              })
              commit('recordInEditModeAttachments')
              api.getAttachments().then(response => {
                commit('updateAttachmentsList', response.data)
              })
              bus.$emit('msg.success', `Rename attachment to [${newName}] success!`)
            })
            .catch(response => {
              bus.$emit('msg.error', response.data)
            })
        }).catch(err => {
          bus.$emit('msg.error', `Rename attachment to [${newName}] error: ${err}`)
        })
      }).catch(err => {
        bus.$emit('msg.error', `Rename attachment error: ${err}`)
      })
    },
    renameSnapshot ({ state, commit, dispatch }, { index, newName }) {
      dispatch('isNameValid', newName).then(() => {
        dispatch('isNameNotExists', {
          name: newName,
          sourceList: state.snapshotList,
          index: index
        }).then(() => {
          commit('setSnapshotName', { index, newName })
          commit('setSnapshotEditMode', {
            index: index,
            mode: false
          })
          bus.$emit('msg.success', `Rename snapshot to [${newName}] success!`)
        }).catch(err => {
          bus.$emit('msg.error', `Rename snapshot to [${newName}] error: ${err}`)
        })
      }).catch(err => {
        bus.$emit('msg.error', `Rename snapshot error: ${err}`)
      })
    },
    saveCache ({ state, dispatch, commit }) {
      if (!state.createName || state.createName.trim().length === 0) {
        bus.$emit('msg.error', 'Draft name should not be empty!')
        return
      }
      if (state.selectedTemplateIndex === null) {
        return
      }
      const template = state.templates[state.selectedTemplateIndex]
      api.setCache(template.id, template.path, state.createName, state.templateDetail)
        .then(response => {
          if (response.data.code === 1000) {
            bus.$emit('msg.success', 'Save draft ' + state.createName + ' success!')
            commit('setSelectedCache', state.createName)
            commit('setShownDraftNameModal', false)
            dispatch('loadTemplate')
            dispatch('loadCacheList')
          } else {
            bus.$emit('msg.error', 'Save draft error: ' + response.data.message)
          }
        }).catch(response => {
          bus.$emit('msg.error', 'Save draft error:' + response)
        })
    },
    deleteCache ({ state, dispatch, commit }, draftName) {
      const template = state.templates[state.selectedTemplateIndex]
      api.deleteCache(template.id, template.path, draftName)
        .then(response => {
          if (response.data.code === 1000) {
            bus.$emit('msg.success', 'Delete success!')
            commit('setSelectedCache', state.selectedCache)
            dispatch('loadCacheList')
          } else {
            bus.$emit('msg.error', 'Delete failed error: ' + response.data.message)
          }
        }).catch(error => {
          bus.$emit('msg.error', 'Delete failed error: ' + error)
        })
    }
  }
}
