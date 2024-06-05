# POIT Final Project

## Introduction

### Project Name
**POIT Final Project**

### Overview
The POIT Final Project is a comprehensive web application designed to monitor sensor data in real-time using the Python Flask framework and SocketIO. The project integrates hardware components, including an Arduino Uno board and various sensors, with a Raspberry Pi to collect, process, and visualize data. The system supports real-time data monitoring, graphical data representation, and data storage in both a MySQL database and files.

### Goal
The primary goal of this project is to demonstrate the integration of IoT concepts by creating a web application that effectively monitors sensor data. The application provides functionalities for initializing the system, starting and stopping data monitoring, visualizing data in various formats, and archiving the data for future analysis.

## Features

1. **System Initialization**: Initialize the system and activate sensors.
2. **Parameter Settings**: Configure monitoring parameters.
3. **Start/Stop Monitoring**: Start or stop data monitoring and visualization.
4. **Data Display**: Display monitored data in JSON format, graphs, and gauges.
5. **Data Archiving**: Store monitored data in a MySQL database and local files.
6. **Data Retrieval**: Retrieve and visualize stored data from the database and files.
7. **System Deactivation**: Stop monitoring and close the application.

## Hardware Requirements

- Arduino Uno board
- MQ2 Gas sensor
- Light sensor
- Dallas Temperature sensor
- Rain sensor
- Jumper wires and breadboard
- Raspberry Pi (or a computer running Raspberry Pi OS in a virtual machine)

## Software Requirements

- Python 3.x
- Flask
- Flask-SocketIO
- MySQL
- Arduino IDE
- Plotly
- Bootstrap
- jQuery

## Installation

### Clone the Repository

1. Clone the repository to your local machine:

   ```sh
   git clone https://github.com/sarfiraz/poit_final_project.git
   cd poit_final_project
