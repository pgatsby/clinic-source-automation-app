const path = require("node:path");

const { app, BrowserWindow } = require("electron");

const createWindow = () => {
  const iconPath =
    process.platform === "darwin"
      ? path.join(__dirname, "assets/icon.icns") // Path to .icns file for macOS
      : path.join(__dirname, "assets/icon.ico"); // Path to .ico file for Windows

  const win = new BrowserWindow({
    width: 800,
    height: 600,
    icon: iconPath,
    webPreferences: {
      nodeIntegration: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  win.loadFile("src/index.html");
};

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
