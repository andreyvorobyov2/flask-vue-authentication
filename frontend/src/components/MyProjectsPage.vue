
<script>
import {MyProjectsService} from '../service.js';
import Toast from 'primevue/toast';

export default{
    components:{
        Toast
    },
    data(){
        return{
            BackendData: '',
            UserName:''
        }
    },
    mounted(){
        this.UserName = this.$store.state.username;
        MyProjectsService(this.OnMyProjectsSuccess, this.OnMyProjectsError)
    },
    methods:{
        OnMyProjectsSuccess(response){
            this.BackendData = response.data.backendtext;
        },
        OnMyProjectsError(error_text){
            this.$toast.add({ severity: 'error', summary: 'My Projects error', 
                detail: error_text, group:'br', life: 3000 });        
        },
        
    }
}
</script>

<template>
    <h2>Wllcome {{ UserName }}</h2>
    <h4>This is protected page My projects</h4>
    <h3>{{ BackendData }}</h3>
    <Toast/>
</template>