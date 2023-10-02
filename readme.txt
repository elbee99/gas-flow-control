# Gas Flow Controller Read Me

## Quick Start Setup

1. Turn on the gas flow controllers at the outlet.
2. Turn on the Oxygen sensor.
3. Open the Argon and Oxygen gas supply taps and ensure there is a pressure of approximately 1 bar being supplied to both controllers.
4. Run Gui.py on the PC using Visual Studio Code.
5. Input the desired gas flow schedule for the experiment.
6. Click Run.

## Introduction

This Read Me file provides information for setting up and operating the Gas Flow Controllers to provide a specific oxygen concentration by regulating the flow of oxygen and argon to the Linkham stage.

## 1. System Overview

Basically, the system consists of two parts: the oxygen sensor and mass flow controllers. The oxygen concentration is detected with a gas sensor (Rapidox 2100ZF Oxygen Analyser) connected to the outlet of the Linkham stage. The oxygen and argon gas flowing into the Linkham stage are digitally controlled by Alicat mass flow controllers. A nice and simple diagram of the system can be found in this link: [System Diagram](https://www.notion.so/Teamspace-Home-e068aafcd44045b9ba48a1b07cb9d666?pvs=4#4b291ff66bf34c9bbd2d73300f163c8f).

## 2. Hardware Setup

Follow these steps to set up the Gas Flow Controllers with the Linkham stage if disassembled:

1. Ensure that there is a reliable source of Oxygen and Argon gas supply connected to the controllers.
2. Plug in and switch on the gas flow controllers.
3. Connect the gas supply lines to the respective gas inlet ports on the controllers.
4. Connect the outlet ports on the controllers to the Linkham stage.
5. Connect the outlet port of the Linkham stage to the Oxygen Sensor.
6. Make sure that all connections are secure and leak-free.
7. Connect the controllers to the computer using the provided USB cables.

(typical operations)
8. Open the Argon and Oxygen gas supply taps to 1 bar of pressure.
9. Ensure the Oxygen Sensor is turned on and connected to the PC by USB.
10. Ensure the gas flow controllers are switched on and connected to the PC by USB.
11. Run Gui.py in Visual Studio Code.

## 3. Operating Instructions

The Graphical User Interface (GUI) allows the user to input either the desired oxygen concentration or flow rates and see a live plot of the oxygen concentration.

**To set the desired oxygen concentration, follow these steps:**
1. Click on the “Concentration” button.
2. Enter the total flow rate (Note: It is recommended for the flow rate to be less than 100 sccm to prevent damaging the heating element. The software will have a warning window pop up if you input a value above 60 sccm, and a value above 100 sccm is outright forbidden).
3. Enter the desired oxygen concentration percentage in the range of 0 - 30%.
4. Enter the duration of the setpoint in minutes.
5. If it is desired to add more setpoints to the program, press the “Add Point” button. This will prompt you to add the oxygen concentration and duration setpoint for the next segment.
6. Press “run” to start the program. The program will only start if you have entered all the values correctly.
7. The live plotting shows the oxygen concentration as a function of time.

**To set the desired oxygen and argon flow rates, follow these steps:**
1. Click on the “Flowrate” button.
2. Enter the desired oxygen flow rate in sccm.
3. Enter the desired argon flow rate in sccm.
4. Enter the duration of the setpoint in minutes.
5. If it is desired to add more setpoints to the program, press the “Add Point” button. This will prompt you to add the desired oxygen and argon flow rates for the next segment.

## 4. Maintenance

Regular maintenance is essential to ensure the proper functioning of the Gas Flow Controllers:

- Periodically inspect gas supply lines for leaks.
- Ensure there are adequate amounts of gas for each experiment.

## 5. Software Requirements

- Python version ___
- Python libraries:
  - tkinter
  - customtkinter
  - numpy
  - os
  - matplotlib.pyplot
  - matplotlib
  - time
  - datetime
  - logging

## 6. Software Installation

To control the Gas Flow Controllers, you'll need to install the accompanying Python code:

1. Clone this repository to the local machine.
2. Open the repository in Visual Studio Code.
3. Run gui.py.

## 7. Contact Information

For technical support, questions, or additional information, please contact Celia Chen:
- Email: cc2147@cam.ac.uk

---

**Note:** Always refer to the user manual provided with the Gas Flow Controllers for specific details, safety instructions, and advanced features. Following these guidelines will help you operate the controllers efficiently and safely during your experiments.
