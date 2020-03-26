# CCI Data Volumes

Script to calculate and print the data volumes for the CCI 
project as held in the CEDA elasticsearch index. Values are printed
in base 10 SI units.

## Setup

This script requires the Elasticsearch python client and python 3.
1. Make a virtual environmemt:

    ```shell script
    python -m venv venv
    ```
2. Install the requirements:

    ```shell script
    pip install -r requirements.txt
    ```
   
## Running the script
```shell script
python cci_data_volumes.py
```
