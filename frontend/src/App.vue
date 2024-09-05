<script>
import { RouterLink, RouterView } from 'vue-router';
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import Chip from 'primevue/chip';
import {LogoutService} from './service.js';

export default{
    components:{
        Toolbar,
        Button,
        Toast,
        Chip
    },
    methods:{
        HomePage(){
            this.$router.push('/');
        },
        AboutPage(){
            this.$router.push('/about');
        },
        LoginPage(){
            this.$router.push('/login');
        },
        MyProjectsPage(){
            this.$router.push('/myprojects');
        },
        Logout(){
            LogoutService(this.OnLogoutSuccess, this.OnLogoutError);
        },
        OnLogoutSuccess(response){
            this.$toast.add({ severity: 'success', summary: 'Logout success', 
                detail: `status ${response.status} ${response.statusText}`, group:'br', life: 3000 });

            this.$store.commit('SaveUserName', '');
            this.$router.push('/');
        },
        OnLogoutError(error_text){
            this.$toast.add({ severity: 'error', summary: 'Logout error', detail: error_text, group:'br', life: 3000 });
        },
    },
}

</script>

<template>
    <Toast position="bottom-right" group="br"/>
    <div class="toolbar">
    <Toolbar >
            <template #start>
                <Button class="mr-2" severity="secondary" label="Home" @click="HomePage"/>
                <Button class="mr-2" severity="secondary" label="About" @click="AboutPage"/>
                <Button class="mr-2" severity="secondary" label="My projects" @click="MyProjectsPage"/>
            </template>

            
            <template #end> 
                <div v-if="this.$store.state.username">
                    <div class="block">
                        <Chip :label="this.$store.state.username"  icon="pi pi-user"/>
                        <!--<p style="margin-right: 10px;">{{this.$store.state.username}}</p>-->
                    </div>
                    <div class="block">
                        <Button class="mr-2" severity="warn" label="Logout" @click="Logout"/>
                    </div>
                </div>
                <Button v-else class="mr-2" severity="success" label="Login" @click="LoginPage"/>
                
            </template>
        </Toolbar>
    </div>
    <RouterView/>
</template>

<style scoped>
    .toolbar{
        width: 99%;
        position: absolute;
        top: 5px;
        left: 5px;
    }
    .block{
        display: inline-block;
        margin-left: 10px;
    }
</style>
