import { io } from "socket.io-client";

//const socketURL = "http://127.0.0.1:5000/";
const socketURL = 'http://172.20.0.10:8080/api/';
//const socketURL = '/api/';

function create_socket(params) {
  try {
    var socket = io.connect(socketURL, { withCredentials: true });
    params.on_success(socket);
  } catch (error) {
    params.on_error(error);
  }
}

export { create_socket };
