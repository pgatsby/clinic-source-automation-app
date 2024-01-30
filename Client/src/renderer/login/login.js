$(document).ready(function () {
  // Check if there are saved credentials and clinic name when the app starts
  const savedClinicName = localStorage.getItem("clinicName");
  const savedUsername = localStorage.getItem("username");
  const savedPassword = localStorage.getItem("password");

  if (savedClinicName && savedUsername && savedPassword) {
    $("#clinicName").val(savedClinicName);
    $("#username").val(savedUsername);
    $("#password").val(savedPassword);
    $("#rememberMe").prop("checked", true);
  }
});

$("#loginForm").on("submit", function (event) {
  event.preventDefault();

  // Show the spinner by removing 'd-none' and adding 'd-flex'
  $("#loginSpinner").removeClass("d-none").addClass("d-flex");

  // Extract login details
  const clinicName = $("#clinicName").val();
  const username = $("#username").val();
  const password = $("#password").val();
  const rememberMe = $("#rememberMe").is(":checked");

  if (rememberMe) {
    localStorage.setItem("clinicName", clinicName);
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);
  } else {
    localStorage.removeItem("clinicName");
    localStorage.removeItem("username");
    localStorage.removeItem("password");
  }

  let formData = {
    clinicName: clinicName,
    username: username,
    password: password,
  };

  window.electronAPI
    .postRequest(serverUrl + "/login", formData)
    .then((data) => {
      if (data.status === "success") {
        window.electronAPI.sendLoginSuccess();
      } else {
        showErrorAlert();
      }
    })
    .catch((error) => {
      showErrorAlert();
    });
});

function showErrorAlert() {
  $("#loginSpinner").removeClass("d-flex").addClass("d-none");
  $("#loginError").addClass("show-alert");
  setTimeout(function () {
    $("#loginError").removeClass("show-alert").delay(500);
  }, 5000);
}
