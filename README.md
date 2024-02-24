<a name="readme-top"></a>

<!-- ABOUT THE PROJECT -->

## About The Project

<div align="center"> 
<img width="491" alt="login" src="https://github.com/p-gatsby/Clinic-Source-Automation-App/assets/106583795/81dcb3fe-6a63-4f4b-ac08-70af5a5663f7">
<img width="492" alt="patientEntry" src="https://github.com/p-gatsby/Clinic-Source-Automation-App/assets/106583795/c728a750-df26-4460-b7b4-4390b80fb718">
</div>

This application, built with Electron, Flask, and Selenium, is designed to streamline clinical processes by automating redundant tasks like filling in patient information using previously submitted data.
<!-- GETTING STARTED -->

## Getting Started

Welcome to CSAP (clinic-source-automation-app)! This guide provides detailed steps to set up the environment and install this project on your local computer.

### Prerequisites

Before you begin, ensure you have the following installed:

- Node.js
- Python3

### Installation

Clone the repository > clinic-source-automation-app

  ```bash
  git clone https://github.com/p-gatsby/clinic-source-automation-app.git
  ```

Electron app installation ~ > clinic-source-automation-app > client

- Install node dependencies
  
  ```sh
  npm install
  ```

Flask server installation ~ > clinic-source-automation-app > server

- Install virtual environment:

  ```sh
  python3 -m venv env
  ```

- Install server dependencies:

  ```sh
  pip install -r requirements.txt
  ```

### Server Environmental Variables

  ```
  WAIT_TIMEOUT = 10
  CHROMEDRIVER_PATH = /app/.chromedriver/bin/chromedriver
  GOOGLE_CHROME_BIN = /app/.apt/usr/bin/google-chrome
  ```

### Running the app

- Run Flask Server ~ > clinic-source-automation-app > server
  
  ```sh
  flask --app app run
  ```

- Run Electron App ~ > clinic-source-automation-app > client
  
  ```sh
  npm start
  ```

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
