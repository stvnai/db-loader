import os
import numpy as np
import pandas as pd
from garmin_fit_sdk import Stream, Decoder
from app.set_logging import set_module_logger

logger= set_module_logger(__name__)


                    ##########  DATA AND METADATA SCHEMAS  ##########


## METADATA SCHEMA

metadata_schema= {
    "athlete_id": "Int64",
    "timestamp": "datetime64[ns, UTC]",
    "sport": "string",
    "sub_sport": "string",
    "weight": "Float64",
    "threshold_power": "Int64",
    "total_time": "string",
    "ride_time": "string",
    "total_distance": "Float64",
    "total_work": "Float64",
    "total_kj_kg": "Float64",
    "total_calories": "Int64",
    "avg_speed": "Float64",
    "max_speed": "Float64",
    "avg_power": "Int64",
    "max_power": "Int64",
    "normalized_power": "Int64",
    "training_stress_score":"Float64",
    "intensity_factor": "Float64",
    "avg_heart_rate": "Int64",
    "max_heart_rate": "Int64",
    "avg_cadence": "Int64",
    "max_cadence": "Int64",
    "min_temperature": "Int64",
    "max_temperature": "Int64",
    "avg_temperature": "Int64",
    "total_ascent": "Int64",
    "total_descent": "Int64",
    "avg_vam": "Float64"
}


## DATA SCHEMA

data_schema= {
    'activity_id': 'Int64',
    'elapsed_time': 'string',
    'position_lat': 'Float64',
    'position_long': 'Float64',
    'distance': 'Float64',
    'elevation': 'Float64',
    'speed': 'Float64',
    'power': 'Int64',
    'heart_rate': 'Int64',
    'temperature': 'Int64',
    'cadence': 'Int64',
    'respiration_rate': 'Int64',
    'accumulated_power': 'Int64',
    'left_torque_effectiveness': 'Float64',
    'right_torque_effectiveness': 'Float64',
    'left_pedal_smoothness': 'Float64',
    'right_pedal_smoothness': 'Float64',
    'work': 'Float64',
    'w_kg': 'Float64',
    'kj_kg': 'Float64',
    'left_power_phase_start': 'Float64',
    'left_power_phase_end': 'Float64',
    'right_power_phase_start': 'Float64',
    'right_power_phase_end': 'Float64',
    'left_power_peak_start': 'Float64',
    'left_power_peak_end': 'Float64',
    'right_power_peak_start': 'Float64',
    'right_power_peak_end': 'Float64',
    'balance_left': 'Int64',
    'balance_right': 'Int64',
    'lap': 'boolean'
}


def extract_data(filepath:str) -> tuple:

    '''
    Description
    ----
        Extract metrics used for another feature engineer process.
    
    
    :param str filepath: string with absolute path to file being processed.
    :param str name_id: string with the athlete's name introduced by the user in the GUI.

    :return: tuple with data_df and metadata_df
    :rtype: tuple

    '''
    
     
                    ########## EMPTY  MAIN DATAFRAMES WITH SCHEMA  ##########

    filename= os.path.basename(filepath)

    metadata_cols= list(metadata_schema.keys())
    metadata_df= pd.DataFrame(columns=metadata_cols).astype(metadata_schema)

    data_cols= list(data_schema.keys())
    data_df= pd.DataFrame(columns=list(data_schema.keys())).astype(data_schema)


##### GET DATA FROM .FIT FILE #####
    raw_metadata_df= pd.DataFrame()
    raw_data_df=pd.DataFrame()

    try:

        stream= Stream.from_file(filepath)
        decoder= Decoder(stream)
        messages, _ = decoder.read()
        messages_keys= list(messages.keys())

    except Exception as e:
        logger.critical(f"CRITICAL ERROR: Unable to read data from {filename}: {e}.")               
        return raw_data_df, raw_metadata_df


                    ##########   METADATA   ##########

##### EXTRACT SESSION AND USER METADATA #####

## SESSION METADATA 

    concat_df= []

    if "session_mesgs" in messages_keys:

        try:

            session_raw_data= messages.get("session_mesgs")
            session_raw_df= pd.DataFrame(session_raw_data)
            concat_df.append(session_raw_df)

        except Exception as e:
            logger.error(f"Error building session raw dataframe from {filename}: {e}.")


## DEVICE METADATA 

    if "device_info_mesgs" in messages_keys:
        
        try:

            manufacturer= messages.get("device_info_mesgs",[{}])[0].get("manufacturer", None)

        except Exception as e:
            logger.warning(f"Error obtaining manufacturer from {filename}: {e}")


## LAP DATA 
    if "lap_mesgs" in messages_keys:

        try:

            lap_data= messages.get("lap_mesgs",None)
            lap_df= pd.DataFrame(lap_data)

        except Exception as e:
            logger.error(f"Error building lap dataframe: {e}.")

## USER METADATA

    if "user_profile_mesgs" in messages_keys:
        
        try:

            weight= messages.get("user_profile_mesgs",[{}])[0].get("weight", None)

        except Exception as e:
            logger.warning(f"Error getting weight from user profile raw data from {filename}: {e}")

        try:

            user_raw_data= messages.get("user_profile_mesgs")
            user_raw_df= pd.DataFrame(user_raw_data)
            concat_df.append(user_raw_df)

        except Exception as e:
            logger.error(f"Error building user profile raw dataframe from {filename}: {e}.")

    else:
        weight= None

    if concat_df:
        try:

            raw_metadata_df= pd.concat(concat_df, axis=1)

        except Exception as e:
            logger.error(f"Error concatenating Dataframes into raw metadata dataframe from {filename}: {e}.")
            return raw_data_df, raw_metadata_df


##### POPULATE METADATA DATAFRAME WITH INITIAL RAW METADATA #####

    raw_metadata_cols= raw_metadata_df.columns.to_list()
    for r_col in raw_metadata_cols:
        if r_col in  metadata_cols:
            metadata_df[r_col]= raw_metadata_df[r_col]
        

    


##### METADATA PREPROCESSING #####

## TOTAL TIME AND RIDE TIME

    try:

        metadata_df["total_time"]= (raw_metadata_df["total_elapsed_time"].apply(\
            lambda x: f"{int(x // 3600):02}:{int(x % 3600 //60):02}:{int(x % 60):02}"
            )).astype("string")

        metadata_df["ride_time"]= (raw_metadata_df["total_timer_time"].apply(\
            lambda x: f"{int(x // 3600):02}:{int(x % 3600 //60):02}:{int(x % 60):02}"
            )).astype("string")
        
    except (ValueError, TypeError) as e:
        logger.critical(f"Error converting position lat/long data from {filename}: {e}.")
    
    except TypeError as e:
        logger.warning(f"No column {e} present in raw metadata for {filename}.")



# TOTAL_WORK
    try:    

        metadata_df["total_work"] = (raw_metadata_df["total_work"] / 1000).round(2).astype("Float64")

    except (ValueError, TypeError) as e:
        logger.critical(f"Error converting total work data from {filename}: {e}.")

    except KeyError as e:
        logger.warning(f"No column {e} present in raw metadata for {filename}.")


# TOTAL_KJ/KG

    if weight:

        try:

            metadata_df["total_kj_kg"] = ((raw_metadata_df["total_work"] / 1000) / weight).round(2).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.warning(f"Error creating total work/kj metric from {filename}: {e}.")

        except KeyError as e:
            logger.warning(f"No column {e} present in raw metadata for {filename}.")


# TOTAL_DISTANCE

    metadata_df["total_distance"] = (raw_metadata_df["total_distance"] / 1000).round(3).astype("Float64")

## SPEED 
    if "avg_speed" in raw_data_df.columns: 
        metadata_df["avg_speed"]= (raw_metadata_df["avg_speed"] * 3.6).round(2).astype("Float64")

    else:
        metadata_df["avg_speed"]= 0.00

    if "max_speed" in raw_data_df.columns:    
        metadata_df["max_speed"]= (raw_metadata_df["max_speed"] * 3.6).round(2).astype("Float64")

    else:
        metadata_df["max_speed"]= 0.00

## SPORT AND SUBSPORT

    metadata_df["sport"]= raw_metadata_df["sport"].astype("string")
    metadata_df["sub_sport"]= raw_metadata_df["sub_sport"].astype("string")  

                    ##########   DATA   ##########

##### EXTRACT DATA RECORDS #####

    if "record_mesgs" in messages_keys:

        try:

            raw_data= messages.get('record_mesgs')
            raw_data_df= pd.DataFrame(raw_data)

        except Exception as e:
            logger.error(f"Error building raw data dataframe from {filename}. Data will be empty {e}.")
            return raw_data_df, metadata_df

##### CHECK FOR ACCUMULATED POWER AVAILABLE #####

    if "accumulated_power" not in raw_data_df.columns:

        try:

            raw_data_df["accumulated_power"] = (raw_data_df["power"].cumsum() / 1000).round().astype("Int64")

        except Exception as e:
            logger.warning(f"No power data in {filename} for creating accumulated power metric.")


##### POPULATE DATA DATAFRAME WITH INITIAL RAW DATA #####

    raw_data_cols= raw_data_df.columns.to_list()
    for r_col in raw_data_cols:
        if r_col in data_cols:
            data_df[r_col]= raw_data_df[r_col]


##### DATA PREPROCESSING #####

# ELAPSED TIME

    data_df["elapsed_time"]= pd.to_datetime(range(len(raw_data_df)), unit="s").strftime("%H:%M:%S").astype("string")


# LAP MARKING

    a= "timestamp" in lap_df.columns
    b= "start_time" in lap_df.columns
    c= "timestamp" in raw_data_cols

    if a and b and c :

        try:

            data_df["lap"] = (raw_data_df["timestamp"].isin(lap_df["timestamp"]) | 
                            raw_data_df["timestamp"].isin(lap_df["start_time"])).astype("boolean")
            
        except (ValueError, TypeError) as e:
            logger.warning(f"Error marking activity laps: {e}.")
            data_df["lap"] = False


## ACTIVITY ID

    data_df["activity_id"]= pd.Series([np.nan] * len(raw_data_df), dtype="Int64")


## INTEGER COLUMNS

    int64_raw_cols= [
        "power",
        "heart_rate",
        "temperature",
        "cadence",
        "enhanced_respiration_rate", 
        "accumulated_power"
    ]
    
    int64_cols= [
        "power",
        "heart_rate",
        "temperature",
        "cadence",
        "respiration_rate",
        "accumulated_power"
    ]

    for r_col, col in zip(int64_raw_cols, int64_cols):

        if r_col in raw_data_cols:

            try:

                data_df[col]= raw_data_df[r_col].round().astype("Int64")

            except (ValueError, TypeError) as e:
                logger.critical(f"Error converting {r_col} datatype from {filename}: {e}.")

        else:
            logger.warning(f"No data found for {r_col} from {filename}.")
            

## POSITION LAT/LONG

    semicircles= (180 / 2**31)
    if "position_lat" in raw_data_cols and "position_long" in raw_data_cols:

        try:
            data_df["position_lat"]= (raw_data_df["position_lat"] * semicircles).round(8).astype("Float64")
            data_df["position_long"]= (raw_data_df["position_long"] * semicircles).round(8).astype("Float64")
        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting position lat/long data from {filename}: {e}.")

    else:
        logger.warning(f"No data found for position lat/long.")


## DISTANCE

    if "distance" in raw_data_cols:

        try:

            data_df["distance"]= (raw_data_df["distance"] / 1000).round(3).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting distance data from {filename}: {e}.")

    else:
        logger.warning(f"No data found for distance in {filename}.") 


## ELEVATION

    if "altitude" in raw_data_cols:
        
        try:
            data_df["elevation"]= (raw_data_df["altitude"]).round(2).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting elevation data from {filename}: {e}.")

    elif "enhanced_altitude" in raw_data_cols:

        try:

            data_df["elevation"]= (raw_data_df["enhanced_altitude"]).round(2).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting elevation data from {filepath}: {e}.")

    else:
        logger.warning(f"No data found for elevation in {filename}.") 


## SPEED

    if "speed" in raw_data_cols:

        try:
            data_df["speed"]= (raw_data_df["speed"] * 3.6).round(2).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting speed data from {filepath}: {e}.")

    elif "enhanced_speed" in raw_data_cols:

        try:

            data_df["speed"]= (raw_data_df["enhanced_speed"] * 3.6).round(2).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting enhanced speed data from {filepath}: {e}.") 

    else:
        logger.warning(f"No data found for speed in {filename}.")


## TORQUE EFFECTIVENESS / PEDAL SMOOTHNESS

    torque_smoothness= [
        "left_torque_effectiveness", 
        "right_torque_effectiveness", 
        "left_pedal_smoothness",
        "right_pedal_smoothness"
    ]

    for metric in torque_smoothness:

        if metric in raw_data_cols:

            try:

                data_df[metric]= raw_data_df[metric].round(1).astype(data_schema[metric])

            except (ValueError, TypeError) as e:
                logger.critical(f"Error converting {metric} datatype from {filename}: {e}.")

        else:
            logger.warning(f"No data found for {metric} in {filename}.")


##### ADITIONAL/DERIVATED METRICS #####

## WORK

    if "accumulated_power" in raw_data_cols:
        
        try:

            data_df["work"]= ((raw_data_df["accumulated_power"] / 1000)).round(2).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting work data from {filename}: {e}.")

    else:
        logger.warning(f"No data found for accumulated work in {filename}.")


## WEIGHT RELATED METRICS

    if weight:

        try:

            if "accumulated_power" in raw_data_cols:

                data_df["kj_kg"]= ((raw_data_df["accumulated_power"] / 1000) / weight).round(2).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting kj_kg data from {filename}: {e}.")

        try:

            if "power" in raw_data_cols:

                data_df["w_kg"]= (raw_data_df["power"] / weight).round(2).astype("Float64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting w_kg data from {filename}: {e}.")
        
    else:
        logger.warning(f"No data found for kj/kg and w/kg in {filename}.")


## L/R BALANCE

    if "left_right_balance" in raw_data_cols:
        
        try:

            if manufacturer == "garmin":
                    data_df["balance_right"] = raw_data_df["left_right_balance"].round().astype("Int64") - 128
                    data_df["balance_left"] = 100 - (raw_data_df["left_right_balance"].round().astype("Int64") - 128)

            else:

                data_df["balance_right"] = 100 - raw_data_df["left_right_balance"].round().astype("Int64")
                data_df["balance_left"] = raw_data_df["left_right_balance"].round().astype("Int64")

        except (ValueError, TypeError) as e:
            logger.critical(f"Error converting L/R balance data from {filename}: {e}.")

    else:
        logger.warning(f"No data found fo L/R balance in {filename}.")


## POWER PHASE DATA

    power_phase_columns= {
        "left_power_phase": ["left_power_phase_start","left_power_phase_end"],
        "right_power_phase": ["right_power_phase_start","right_power_phase_end"],
        "left_power_phase_peak": ["left_power_peak_start","left_power_peak_end"],
        "right_power_phase_peak": ["right_power_peak_start","right_power_peak_end"]
    }

    for key, cols in power_phase_columns.items():

        if key in raw_data_cols:
            try:
                data_df[cols[0]] = raw_data_df[key].str[0].round(2).astype("Float64")
                data_df[cols[1]] = raw_data_df[key].str[1].round(2).astype("Float64")
            except (ValueError, TypeError, KeyError) as e:
                logger.critical(f"Error converting Power Phase Data from {filename}: {e}.")

        else:
            logger.warning(f"No power phase data for {key} in {filename}.")
    
    
    metadata_df= metadata_df.replace({pd.NA:None})
    data_df= data_df.replace({pd.NA:None})

    logger.info(f"Extracting and processing data process finished for {filename}")
    return data_df, metadata_df


def save_to_csv(data_df:pd.DataFrame, metadata_df:pd.DataFrame, csv_filename:str, filepath:str):

    '''
    Description
    ----
        Takes data_df and metadata_df processed already processed and dump all data into a .csv files.
        The previously defined csv_filename variable contains a string, it will be
        the .csv file name. filepath variable it's just for Exception control.

    
    :param DataFrame data_df: DataFrame with activity data processed.
    :param DataFrame metadata_df: DataFrame with activity metadata processed.
    :param str csv_filename: string with a unique name for .csv files.
    :param str filepath: string with absolute path to file being processed.
    :return: Saves a .csv file.
    :rtype: None
    
    '''

    try:
        data_df.to_csv(f"{csv_filename}_activity.csv", index=False)
        print(f"Data .csv file(s) saved for {filepath}")

    except Exception as e:
        print(f"WARNING, -activity.csv file not saved for {filepath}: {e}")

    try:
        metadata_df.to_csv(f"{csv_filename}_metadata.csv", index=False)
        print(f"Metadata .csv file(s) saved for {filepath}")

    except Exception as e:
        print(f"WARNING, .csv file not saved for {filepath}: {e}")

def process_and_insert(filepath:str):

    '''
    Description
    ----
    Takes extract_data and save_to_csv functions and executes them, it allows to pass the
    hole script to a multiprocessing pool.

    
    :param str filepath: string with absolute path to file being processed.
    :param str name_id: string with the athlete's name introduced by the user in the GUI.

    :return: 
    :rtype: None
    
    '''

    data_df, metadata_df = extract_data(filepath)
    return data_df, metadata_df

    # save_to_csv(data_df, metadata_df, csv_filename, filepath)

