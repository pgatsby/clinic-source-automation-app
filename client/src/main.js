const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("node:path");

let win; // Declare 'win' in the global scope

const createWindow = () => {
  const iconPath =
    process.platform === "darwin"
      ? path.join(__dirname, "assets/icon.icns") // Path to .icns file for macOS
      : path.join(__dirname, "assets/icon.ico"); // Path to .ico file for Windows

  win = new BrowserWindow({
    // Initialize 'win' here
    width: 500,
    height: 420,
    icon: iconPath,
    webPreferences: {
      nodeIntegration: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  win.loadFile("src/renderer/login/login.html");
};

app.whenReady().then(createWindow);

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

ipcMain.on("login-success", () => {
  if (win) {
    win.setSize(500, 550);
    win.loadFile("src/renderer/patientEntry/patientEntry.html");
    win.webContents.on("did-finish-load", () => {
      win.webContents.send("login-successful");
    });
  }
});
