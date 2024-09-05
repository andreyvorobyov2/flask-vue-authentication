
<script>
import Card from 'primevue/card';
import Button from 'primevue/button';
import Password from 'primevue/password';
import FloatLabel from 'primevue/floatlabel';
import InputText from 'primevue/inputtext';
import Toast from 'primevue/toast';
import {LoginService} from '../service.js';

export default{
    components:{
        Card,
        Button,
        Password,
        FloatLabel,
        InputText,
        Toast
    },
    data(){
        return{
            username:'',
            password:''
        }
    },
    methods:{
        Login(){
            LoginService(this.OnLoginSuccess, this.OnLoginError, this.username, this.password);
        },
        OnLoginSuccess(response){
            this.$toast.add({ severity: 'success', summary: 'Login success', 
                detail: `status ${response.status} ${response.statusText} ${response.data.username}`, group:'br', life: 3000 }); 
                
            this.$store.commit('SaveUserName', response.data.username);
            this.$router.push('/myprojects');
        },
        OnLoginError(error_text){
            this.$toast.add({ severity: 'error', summary: 'Login error', detail: error_text, group:'br', life: 3000 });               
        },
        Signup(){
            this.$router.push('/signup');
        },
    }
}
</script>

<template>
    <Toast position="bottom-right" group="br"/>
    <Card>
    <template #title>Login</template>
        <template #content>
            
            <FloatLabel class="cl1">
                <InputText id="username" v-model="username" required/>
                <label for="username" >Username</label>
            </FloatLabel>
            
            <FloatLabel class="cl1">
                <Password id="password" v-model="password" :feedback="false"  />
                <label for="username">Password</label>
            </FloatLabel>

            <Button label="Login" severity="success" @click="Login" raised class="cl1"/>
            <Button label="Signup" severity="info" @click="Signup" raised class="cl1"/>
        </template>
    </Card>
</template>


<style scoped>
.cl1{
    margin-top: 25px;
    width: 100%;
}
</style>