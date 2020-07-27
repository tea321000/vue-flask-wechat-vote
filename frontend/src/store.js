import Vue from 'vue'
import Vuex from 'vuex'
import user from '@/store/user'
import permission from '@/store/permission'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    permission
  },
  state: {

  },
  mutations: {

  },
  actions: {

  }
})