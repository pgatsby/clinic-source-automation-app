<a name="readme-top"></a>

<!-- ABOUT THE PROJECT -->

## About The Project

<div align="center"> 
<img width="492" alt="login" src="https://github.com/p-gatsby/Clinic-Source-Automation-App/assets/106583795/81dcb3fe-6a63-4f4b-ac08-70af5a5663f7">
<img width="492" alt="patientEntry" src="https://github.com/p-gatsby/Clinic-Source-Automation-App/assets/106583795/c728a750-df26-4460-b7b4-4390b80fb718">
</div>

This application, built with Electron, Flask, and Selenium, is designed to streamline clinical processes by automating redundant tasks such as filling in patient information using previously submitted data.

<!-- GETTING STARTED -->

## Getting Started

Welcome to CSAP (Clinic-Source-Automation-App)! This guide provides detailed steps to set up the environment and install this project on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/)
- [Python 3](https://www.python.org/)

### Installation

1. **Clone the Repository**  
   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/pgatsby/clinic-source-automation-app.git
   ```

2. **Electron App Installation**  
   Navigate to the `client` directory and install Node.js dependencies:

   ```bash
   cd clinic-source-automation-app/client
   npm install
   ```

3. **Flask Server Installation**  
   Navigate to the `server` directory, set up a virtual environment, and install Python dependencies:
   ```bash
    cd ../server
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
   ```

### Server Environmental Variables

Ensure the following environment variables are set for the Flask server:

```ini
WAIT_TIMEOUT=10
CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver
GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google-chrome
```

### Running the App

1. **Run Flask Server**   
   Start the Flask server from the `server` directory:

   ```bash
   flask --app app run
   ```

2. **Run Electron App**   
   Start the Electron app from the `client` directory:

   ```bash
   cd ../client
   npm start
   ```

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
