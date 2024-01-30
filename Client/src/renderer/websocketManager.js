// Update the server URL here
const serverUrl = "https://clinic-source-server-c397a1ddd444.herokuapp.com/";

// Debugging on localhost
// const serverUrl = "http://127.0.0.1:5000";

const socketAPI = window.electronAPI.createSocket(serverUrl);

socketAPI.on("connect", () => {
  console.log("Connected to server");
  statusDot.classList.remove("offline");
  statusDot.classList.add("online");
  statusText.textContent = "Connected";
});

socketAPI.on("disconnect", () => {
  console.log("Disconnected from server");
  statusDot.classList.remove("online");
  statusDot.classList.add("offline");
  statusText.textContent = "Offline";
});
