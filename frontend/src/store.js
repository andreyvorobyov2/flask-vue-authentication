import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';


const store = new Vuex.Store({
    plugins: [createPersistedState({
        storage: window.sessionStorage,
    })],

    state:{
        username: '',
    },
    mutations:{
        SaveUserName(state, username){
            state.username = username;
        }
    }

})

export default store;