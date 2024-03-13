# OpenTopography-DTM-Downloader

This repository contains a Python script for downloading Digital Terrain Model (DTM) data from the OpenTopography API based on specified geographic locations or bounding boxes.
The script utilizes the `requests` library to interact with the API and `geopandas` for handling geographic data.


## Prerequisites

Before using this script, ensure you have the following:

- Python installed on your system (preferably version 3.x).
- Required Python libraries installed (`requests-2.31.0`, `geopandas-0.14.3`).
- An API code obtained from the OpenTopography website. If you don't have one, you can sign up for free on their website to obtain it.


# OpenTopography WEBSITE:

![image](https://github.com/Eng-Moka/OpenTopo-DTM-Downloader/assets/132586649/81c1c581-7df0-47f9-9db6-ea79a71066ba)

Link : https://opentopography.org


## Usage

1. Clone the repository to your local machine using:
  git clone https://github.com/Eng-Moka/OpenTopo-DTM-Downloader.git

2. Replace placeholders in the script (`YOUR_API_CODE`, `DATASET_SOURCE_ID`, `YOUR_FEATUER_CLASS`, `YOUR_OUTPUT_FOLDER`, `DTM_NAMES_FIELD`, `BUFFER`) with your specific values. Details on these placeholders are provided in the script comments.

3. Run the script:  python OpenTopo-DTM-Downloader.py :)


## Script Explanation

- `OpenTopo-DTM-Downloader.py`: This script is the main Python script. It contains functions for interacting with the OpenTopography API to download DTM data based on specified geographic locations or bounding boxes. The script fetches data in GeoTIFF format and saves it to the specified output directory.

## Parameters

- `YOUR_API_CODE`: Your personal API code obtained from the OpenTopography website.
- `DATASET_SOURCE_ID`: The identifier of the desired dataset source. It corresponds to the index of the dataset in the `global_raster_datasets` list.
- `YOUR_FEATUER_CLASS`: Path to your feature class (shapefile or geodatabase feature class) containing the locations or boundaries from which you want to download DTM data.
- `YOUR_OUTPUT_FOLDER`: Directory where the downloaded DTM files will be saved.
- `DTM_NAMES_FIELD`: Name of the field in the feature class that contains names for each location.
- `BUFFER`: Buffer around points to be used when downloading data, in the coordinate system units of the feature class. Set to 0 if not needed or if using polygon features.


## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request for any improvements or additional features you'd like to see.




  
