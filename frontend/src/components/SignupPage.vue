
<script>
import Card from 'primevue/card';
import Button from 'primevue/button';
import Password from 'primevue/password';
import FloatLabel from 'primevue/floatlabel';
import InputText from 'primevue/inputtext';
import Toast from 'primevue/toast';
import {SignupService} from '../service.js';

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
        Signup(){
            SignupService(this.OnSignupSuccess, this.OnSignupError, this.username, this.password);
        },
        OnSignupSuccess(response){
            this.$toast.add({ severity: 'success', summary: 'Signup success', 
                detail: `status ${response.status} ${response.statusText} ${response.data.username}`, group:'br', life: 3000 }); 
                this.$store.commit('SaveUserName', response.data.username);
            this.$router.push('/myprojects');
        },
        OnSignupError(error_text){
            this.$toast.add({ severity: 'error', summary: 'Signup error', 
                detail: error_text, group:'br', life: 3000 });        
        }
    }
}
</script>

<template>
    <Toast position="bottom-right" group="br"/>
    <Card>
    <template #title>Signup</template>
        <template #content>
            
            <FloatLabel class="cl1">
                <InputText id="username" v-model="username" />
                <label for="username">Username</label>
            </FloatLabel>
            
            <FloatLabel class="cl1">
                <Password id="password" v-model="password" :feedback="false"  />
                <label for="username">Password</label>
            </FloatLabel>

            <Button label="Signup" severity="success" @click="Signup" raised class="cl1"/>
        </template>
    </Card>
</template>

<style scoped>
.cl1{
    margin-top: 25px;
    width: 100%;
}
</style>