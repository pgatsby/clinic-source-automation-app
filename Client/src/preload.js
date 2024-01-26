const { contextBridge, ipcRenderer } = require("electron");
const axios = require("axios");
const io = require("socket.io-client");

contextBridge.exposeInMainWorld("electronAPI", {
  postRequest: (url, data) => axios.post(url, data),
  createSocket: (url) => {
    const socket = io(url);

    return {
      on: (event, func) => socket.on(event, func),
      emit: (event, data) => socket.emit(event, data),
      disconnect: () => socket.disconnect(),
    };
  },
});
