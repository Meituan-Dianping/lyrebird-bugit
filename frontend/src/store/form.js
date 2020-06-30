import * as api from '@/api'
import { bus } from '@/eventbus'
import crypto from 'crypto'

export default {
  state: {
    templates: [],
    selectedTemplateIndex: null,
    templateDetail: null,
    formInfo: null,
    ruleValidate: null,
    formValue: {},
    attachmentsList: [],
    snapshotList: [],
    loadAttachmentCount: 0,
    shownFileName: null,
    submitLock: false,
    shownFileContent: {
      code: null,
      type: null,
      message: null
    }
  },
  mutations: {
    setFormData (state, sourceData) {
      state.templateDetail[sourceData.index].value = sourceData.value
    },
    setTemplates (state, templates) {
      state.templates = templates
    },
    setSelectedTemplateIndex (state, selectedTemplateIndex) {
      state.selectedTemplateIndex = selectedTemplateIndex
    },
    setTemplateDetail (state, templateDetail) {
      state.templateDetail = templateDetail
    },
    setSubmitLock (state, isLock) {
      state.submitLock = isLock
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
    updateAttachmentsList (state, attachmentsList) {
      state.attachmentsList = attachmentsList
    },
    addAttachmentsList (state, attachment) {
      state.attachmentsList.push(attachment)
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
    addSnapshot (state, snapshot) {
      let fileName = 'snapshot_' + snapshot.id
      state.snapshotList.push({ 'name': fileName, 'eventObj': snapshot })
    },
    deleteSnapshot (state, index) {
      state.snapshotList.splice(index, 1)
    }
  },
  actions: {
    loadTemplateList ({ commit, dispatch }) {
      api.getTemplate().then(response => {
        if (response.data.code === 1000) {
          commit('setSelectedTemplateIndex', response.data.selected_index)
          commit('setTemplates', response.data.templates)
          dispatch('loadTemplate')
        } else {
          bus.$emit('msg.error', response.data.message)
        }
      })
    },
    loadTemplate ({ state, commit }) {
      if (state.selectedTemplateIndex === null) {
        return
      }
      const path = state.templates[state.selectedTemplateIndex].path
      api.getTemplate(path).then(response => {
        commit('setTemplateDetail', response.data)
      })
    },
    updateSelectedTemplateIndex ({ commit, dispatch }, selectedTemplateIndex) {
      commit('setSelectedTemplateIndex', selectedTemplateIndex)
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
    saveCache ({ state }) {
      if (state.selectedTemplateIndex === null) {
        return
      }
      const selectedTemplate = state.templates[state.selectedTemplateIndex]
      const md5 = crypto.createHash('md5')
      md5.update(selectedTemplate.path)
      const templateKey = md5.digest('hex')
      api.setCache(templateKey, state.templateDetail).then(response => {
        if (response.data.code === 1000) {
          bus.$emit('msg.success', 'Save as draft, success')
        } else {
          bus.$emit('msg.error', 'Save draft failed: ' + response.message)
        }
      }).catch(response => {
        bus.$emit('msg.error', 'Can\'t save as draft')
        console.error('Can\'t save as draft', response)
      })
    }
  }
}
