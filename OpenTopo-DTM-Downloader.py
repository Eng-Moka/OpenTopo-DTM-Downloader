import os
import requests
import geopandas as gpd


global_raster_datasets = ['SRTMGL3',  'SRTMGL1',    'SRTMGL1_E', 'AW3D30',
                          'AW3D30_E', 'SRTM15Plus', 'NASADEM',   'COP30',
                          'COP90',    'EU_DTM',     'GEDI_L3']


# Available global raster datasets on OpenTopography website:

        # 0   SRTMGL3 (SRTM GL3 90m)
        # 1   SRTMGL1 (SRTM GL1 30m)
        # 2   SRTMGL1_E (SRTM GL1 Ellipsoidal 30m)
        # 3   AW3D30 (ALOS World 3D 30m)
        # 4   AW3D30_E (ALOS World 3D Ellipsoidal, 30m)
        # 5   SRTM15Plus (Global Bathymetry SRTM15+ V2.1)
        # 6   NASADEM (NASADEM Global DEM)
        # 7   COP30 (Copernicus Global DSM 30m)
        # 8   COP90 (Copernicus Global DSM 90m)
        # 9   EU_DTM (DTM 30m)
        # 10  GEDI_L3 (DTM 1000m)

# https://opentopography.org/developers



#-----------------------------------------------------------------------------------

YOUR_API_CODE = 'YOUR_API_KEY' # Replace with your own API code from the OpenTopography website.
DATASET_SOURCE_ID = 1 # replace with NEDED dataset ID in reang [0-10].
YOUR_FEATUER_CLASS = r'PATH\TO\YOUR\FEATUERCLASS'  # replace with path to your locations feature class 
YOUR_OUTPUT_FOLDER = r'PATH\TO\YOUR\OUTPUTFOLDER'  # Define output directory here.
DTM_NAMES_FIELD =  "DTM_Name"  # Name of field that contains names for each location
BUFFER = 000   # Buffer around points to be used when downloading data,In your featuer class crs units.
               # unnecessary if  you are using polygon features.

#-----------------------------------------------------------------------------------


def get_DTM_data(YOUR_API_CODE,DATASET_SOURCE_ID,boundary):
    """
    Get Digital Terrain Model data from GeoNames API.
    
    Parameters:
      YOUR_API_CODE (str): Your personal API code for access to the service.
      DATASET_SOURCE_ID (int): The identifier of the desired dataset source.
      boundary (list of flot ): [miny,maxy,minx,max] define the area of interest.
      
    Returns:
      response.content: Binary Data containing the requested information (DTM data).
    """
    DATASET = global_raster_datasets[DATASET_SOURCE_ID]
    south, north, west, east = boundary
    URL = fr'https://portal.opentopography.org/API/globaldem?demtype={DATASET}&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key={YOUR_API_CODE}'
    response =  requests.get(URL)
    match response.status_code:
        case 200:
            return response.content
        case 400:
            print('Bad request')
            return None
        case 401:
            print('Invalid API code')
            return None
        case 204:
            print("No data available")
            return None
        case 500:
            print('Internal server error')
            return None


def make_DTM_file(file_path, content):
    """
    Create a DTM file .
    
    Parameters:
      file_path (string): Path where the new DTM file will be saved.
      content (binary): Content that will be written into the new DTM file.
    """

    with open(file_path, "wb") as DTM:
        DTM.write(content)
        print(f'File {file_path} created successfully!')


def  featuer_bound_to_DTM(featuer_bounds):
    """
    Transform features bounds from a GeoDataFrame to a Polygon object.
    
    The function receives a feature bound in the form of a geopandas.GeoDataFrame
      with columns [DTM_NAMES_FIELD,miny,maxy,minx,maxx] for etch location.

    This function is used when you need to send the feature bounds to the API in order
      to get the corresponding DTM data.
    
    Parameters:
      feature_bounds (geopandas.GeoDataFrame): A geodataframe containing the Polygon geometry of each location.
      
    """
    for index, row  in featuer_bounds.iterrows():
        # boundary = south, north, west, east 
        boundary = (row['miny'], row['maxy'], row['minx'], row['maxx'])
        # get the binary data of DTM file from OpenTopography API
        data = get_DTM_data(YOUR_API_CODE,DATASET_SOURCE_ID,boundary)
        # if there is no data skip this iteration and move to next feature
        if not data:
            print(f'Error at file: {dtm_file_path}')
            continue
        # create a DTM filename based on the feature name field
        dtm_file_name = str(row[DTM_NAMES_FIELD]) + "_DTM.tif"
        dtm_file_path = os.path.join(YOUR_OUTPUT_FOLDER , dtm_file_name)
        # write the binary data into the corresponding DTM file
        return make_DTM_file(dtm_file_path, data)

            

if '__main__' == __name__:
    
    layer = os.path.basename(YOUR_FEATUER_CLASS)  # get the featuerclass name
    
    GDB = YOUR_FEATUER_CLASS.split('gdb')[0] + 'gdb'  # get the fileGDB path
    
    featuer = gpd.read_file(GDB,layer=layer)  # read feature class from  geodatabase
    
    featuer = featuer.buffer(BUFFER) if BUFFER > 0 else  featuer  # Apply buffer if have one
    
    buffer_featuer_to_WGS = featuer.to_crs('4326')  # convert to WGS84 geographic coordinate system
    
    featuer_bounds = buffer_featuer_to_WGS.bounds  # calculate bounds of each features and save it into a DataFrame
    
    featuer_bounds[DTM_NAMES_FIELD] = featuer[DTM_NAMES_FIELD]  # copy the DTM_NAMES  field to new column NAME_WITH_EXTENSION
    
    featuer_bound_to_DTM(featuer_bounds)  # call the function that will download DTMs based on the bounds of features
