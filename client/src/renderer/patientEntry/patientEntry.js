$(document).ready(function () {
  $("#loginSpinner").removeClass("d-none").addClass("d-flex");
});

socketAPI.on("log_message", (data) => {
  if (data && data.data) {
    updateLog([data.data]);
  } else {
    console.log("Unexpected data structure:", data);
  }
});

socketAPI.on("task_completed", (progress) => {
  updateProgressBar(progress.completedPercentage);
});

window.electronAPI.onLoginSuccessful((event, arg) => {
  populatePatientNames();
});

function populatePatientNames() {
  window.electronAPI
    .getRequest(serverUrl + "/get_patient_names")
    .then((data) => {
      if (data.patientNames && data.patientNames.length > 0) {
        $("#ptName").autocomplete({
          source: data.patientNames,
        });
        // Set the first item as the default value
        $("#ptName").val(data.patientNames[0]);
      } else {
        console.error("Failed to retrieve patient names");
      }
      $("#loginSpinner").removeClass("d-flex").addClass("d-none");
    })
    .catch((error) => {
      console.error("Error:", error);
      $("#loginSpinner").removeClass("d-flex").addClass("d-none");
    });
}

function updateLog(messages) {
  const logContainer = $("#processLog");
  $.each(messages, (index, message) => {
    $("<div>").addClass("log-message").text(message).appendTo(logContainer);
  });
}

function updateProgressBar(percentage) {
  const roundedPercentage = Math.round(percentage);
  const progressBar = $("#progressBar");

  progressBar
    .css("width", roundedPercentage + "%")
    .text(roundedPercentage + "%")
    .attr("aria-valuenow", roundedPercentage);
}

function clearLog() {
  $("#processLog .log-message").remove();
}

function showProgressBar() {
  $("#progressBarContainer").removeClass("d-none");
}

function hideProgressBar() {
  $("#progressBarContainer").addClass("d-none");
}

function resetProgressBar() {
  updateProgressBar(0);
  hideProgressBar();
}

function enableSubmitButton() {
  $("#submitBtn")
    .removeClass("btn-secondary")
    .addClass("btn-primary")
    .prop("disabled", false);
}

function disableSubmitButton() {
  $("#submitBtn")
    .removeClass("btn-primary")
    .addClass("btn-secondary")
    .prop("disabled", true);
}

$("#patientNameForm").on("submit", function (event) {
  event.preventDefault();
  disableSubmitButton();
  showProgressBar();

  let ptName = $("#ptName").val();
  let numOfNotes = $("#numOfNotes").val();

  if (ptName === "- All -" || ptName === " ") {
    ptName = "None";
  }

  let formData = { numOfNotes: numOfNotes, ptName: ptName };

  window.electronAPI
    .postRequest(serverUrl + "/run_script", formData)
    .then((data) => {
      console.log(data.status);
    })
    .catch((error) => {
      console.error(error);
    });
});

$("#patientNameForm").on("reset", function () {
  clearLog();
  resetProgressBar();
  enableSubmitButton();
});
