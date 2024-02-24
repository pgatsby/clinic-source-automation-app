const { contextBridge, ipcRenderer } = require("electron");
const axios = require("axios");
const io = require("socket.io-client");

contextBridge.exposeInMainWorld("electronAPI", {
  getRequest: (url) => axios.get(url).then((response) => response.data),
  postRequest: (url, data) => axios.post(url, data).then((response) => response.data),
  createSocket: (url) => {
    const socket = io(url);

    return {
      on: (event, func) => socket.on(event, func),
      emit: (event, data) => socket.emit(event, data),
      disconnect: () => socket.disconnect(),
    };
  },
  sendLoginSuccess: () => ipcRenderer.send("login-success"),
  onLoginSuccessful: (callback) => ipcRenderer.on("login-successful", callback),
});
