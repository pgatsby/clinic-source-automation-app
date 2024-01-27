function updateLog(messages) {
  const logContainer = document.getElementById("processLog");
  messages.forEach((message) => {
    console.log("Updating log with:", message); // Add this for debugging
    const logElement = document.createElement("div");
    logElement.textContent = message;
    logContainer.appendChild(logElement);
  });
}

function updateProgressBar(percentage) {
  // Round the percentage to the nearest whole number
  const roundedPercentage = Math.round(percentage);

  const progressBar = document.getElementById("progressBar");
  progressBar.style.width = roundedPercentage + "%";
  progressBar.textContent = roundedPercentage + "%";
  progressBar.setAttribute("aria-valuenow", roundedPercentage);
}

function clearLog() {
  const logContainer = document.getElementById("processLog");
  logContainer.innerHTML = ""; // Clear all child elements
}

function resetProgressBar() {
  updateProgressBar(0); // Reset to 0%
  document.getElementById("progressBarContainer").style.display = "none";
}

// Function to enable the submit button
function enableSubmitButton() {
  const submitBtn = document.getElementById("submitBtn");
  submitBtn.classList.remove("btn-secondary");
  submitBtn.classList.add("btn-primary");
  submitBtn.disabled = false;
}

// Function to disable the submit button
function disableSubmitButton() {
  const submitBtn = document.getElementById("submitBtn");
  submitBtn.classList.remove("btn-primary");
  submitBtn.classList.add("btn-secondary");
  submitBtn.disabled = true;
}

// Update the server URL here
const serverUrl = "https://clinic-source-server-f660b6c1e07c.herokuapp.com";

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

socketAPI.on("log_message", (data) => {
  console.log("Received log message:", data); // Check the structure of 'data'
  if (data && data.data) {
    // Safely access 'data.data'
    updateLog([data.data]);
  } else {
    console.log("Unexpected data structure:", data);
  }
});

socketAPI.on("task_completed", (progress) => {
  // Assuming 'progress' contains information about how much of the task is completed
  updateProgressBar(progress.completedPercentage); // Replace with actual property name
});

document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    // Disable the submit button on form submission
    disableSubmitButton();

    document.getElementById("progressBarContainer").style.display = "block";

    // Gather form data
    var formData = {
      clinicName: document.getElementById("clinicName").value,
      username: document.getElementById("username").value,
      password: document.getElementById("password").value,
      numOfPts: document.getElementById("numOfPts").value,
    };

    // Update the POST request URL here
    window.electronAPI
      .postRequest(serverUrl + "/run_script", formData)
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  });

// Event listener for form reset
document.getElementById("loginForm").addEventListener("reset", function () {
  clearLog();
  resetProgressBar();
  enableSubmitButton(); // Enable the submit button on reset
});
