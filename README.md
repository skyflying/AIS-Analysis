# AIS-Analyss

## AIS Data: It is the information broadcasted by the vessel, including name, MMSI  code, IMO code, coordinates, vessel type, heading, width, length, and timestamp.
## Data Period: 2020.04.01 - 2022.05.25
## Data file: 7 days per file and 112 spreadsheets.
## Data Quality:
### Data source doesn’t come from the Marine traffic.
### Missing MMSI, IMO code or name.
### Missing vessel type or other information.
### Time interval is not fixed. 
### Isolated points.
### AIS signal is all over the world including landlocked countries or mountains.

![image](https://github.com/user-attachments/assets/ca64cd86-5b85-4e22-a2c4-3f944d5f615a)


## Vessel Track: Build up the track by connecting data points with the MMSI code(or IMO code ) and sorting by the timestamp. Also filtering by the timestamp, if the time gap for two consecutive points is more than 4 hours, the tracking line would be split into two-part.

![image](https://github.com/user-attachments/assets/42f2d87e-c0f5-42b3-ae4a-5d41cff67c80)

![image](https://github.com/user-attachments/assets/3bad0505-bca1-4725-8c4f-e3cceac638a6)
