
import axios from "axios";

//const backendURL = 'http://127.0.0.1:5000/';
const backendURL = 'http://172.20.0.10:8080/api/';

function  SignupService(OnSuccess, OnError, username, password){
    axios.post(backendURL + 'signup',
        {
            username: username,
            password: password
        }, {withCredentials: true})
        .then((response)=>OnSuccess(response))
        .catch((error)=>OnError(ErrorText(error)))
}

function  LoginService(OnSuccess, OnError, username, password){
    axios.post(backendURL + 'login',
        {
            username: username,
            password: password
        }, {withCredentials: true})
        .then((response)=>OnSuccess(response))
        .catch((error)=>OnError(ErrorText(error)))
}

function  LogoutService(OnSuccess, OnError){
    axios.delete(backendURL + 'logout', {}, {withCredentials: true})
        .then((response)=>OnSuccess(response))
        .catch((error)=>OnError(ErrorText(error)))
}

function  MyProjectsService(OnSuccess, OnError){
     axios.get(backendURL + 'myprojects', {withCredentials: true})
        .then((response)=>OnSuccess(response))
        .catch((error)=>OnError(ErrorText(error)))
}

function ErrorText(error){
    if (error.code == 'ERR_NETWORK'){
        return error.message;
    }
    return `${error.code} ${error.message} ${error.response.data.error}`;
    
}

export { SignupService, LoginService, LogoutService, MyProjectsService };