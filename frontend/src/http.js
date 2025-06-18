import axios from "axios";

//const httpURL = "http://127.0.0.1:5000/";
const httpURL = 'http://172.20.0.10:8080/api/';
//const httpURL = '/api/';

function http_signup(params) {
  axios
    .post(
      httpURL + "signup",
      {
        username: params.username,
        password: params.password,
      },
      { withCredentials: true }
    )
    .then((response) => params.on_success(response))
    .catch((error) => params.on_error(error_text(error)));
}

function http_login(params) {
  axios
    .post(
      httpURL + "login",
      {
        username: params.username,
        password: params.password,
      },
      { withCredentials: true }
    )
    .then((response) => params.on_success(response))
    .catch((error) => params.on_error(error_text(error)));
}

function http_logout(params) {
  axios
    .delete(httpURL + "logout", { withCredentials: true })
    .then((response) => params.on_success(response))
    .catch((error) => params.on_error(error_text(error)));
}

function MyProjectsService(OnSuccess, OnError) {
  axios
    .get(httpURL + "myprojects", { withCredentials: true })
    .then((response) => OnSuccess(response))
    .catch((error) => OnError(error_text(error)));
}

function http_userlist(params) {
  axios
    .get(httpURL + "userlist", {
      withCredentials: true,
      params: { only_online: params.only_online },
    })
    .then((response) => params.on_success(response))
    .catch((error) => params.on_error(error_text(error)));
}

function error_text(error) {
  if (error.code == "ERR_NETWORK") {
    return error.message;
  }
  return `${error.code} ${error.message} ${error.response.data.error}`;
}

export {
  http_login,
  http_signup,
  http_userlist,
  http_logout,
  MyProjectsService,
};
