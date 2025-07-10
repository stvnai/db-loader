import pandas as pd
import numpy as np
from garmin_fit_sdk import Stream, Decoder
import os
import time

# Columns to be extracted from .fit file and included in the dataframe and later in .csv file.
data_columns= ["activity_id", "elapsed_time","position_lat","position_long",
    "distance","elevation","speed","power","heart_rate","temperature",
    "cadence","respiration_rate","accumulated_power","left_torque_effectiveness",
    "right_torque_effectiveness","left_pedal_smoothness","right_pedal_smoothness",
    "work","w_kg","kj_kg","left_power_phase_start","left_power_phase_end",
    "right_power_phase_start","right_power_phase_end","left_power_peak_start",
    "left_power_peak_end","right_power_peak_start","right_power_peak_end",
    "balance_left","balance_right"
    ]

#Columns to be extracted from .fit file and included as metadata.
user_profile_data= ["weight", "gender", "age", "height"]

device_data= ["manufacturer", "garmin_product"]

session_data= ["timestamp","total_elapsed_time", "total_timer_time",
               "total_distance", "total_work", "total_calories", "avg_speed",
               "max_speed", "avg_power", "max_power", "avg_heart_rate",
               "max_heart_rate", "avg_cadence","max_cadence","min_temperature",
               "max_temperature","avg_temperature","total_ascent",
               "total_descent", "normalized_power", "training_stress_score",
               "intensity_factor", "threshold_power", "avg_vam", "sport", "sub_sport"               
               ]

# Columns to be used in the metadata dataframe and included in .csv file.
columns_metadata= ["timestamp","sport","sub_sport","weight", 
                   "threshold_power","total_time","ride_time","distance",
                   "work_kj","calories", "avg_speed","max_speed","avg_power",
                   "max_power","normalized_power","training_stress_score",
                   "intensity_factor","avg_heart_rate","max_heart_rate",
                   "avg_cadence","max_cadence","min_temperature","max_temperature",
                   "avg_temperature","total_ascent","total_descent","avg_vam",
                    ]

# Columns to be used in the athlete dataframe and included in .csv file.

def extract_data(filepath:str)-> tuple:
    '''
    Description
    ----
        Extract metrics used for another feature engineer process.
    
    
    :param str filepath: string with absolute path to file being processed.
    :param str name_id: string with the athlete's name introduced by the user in the GUI.

    :return: tuple with data_df, metadata_df, csv_filename and filepath
    :rtype: tuple

    '''

    try:
        stream = Stream.from_file(filepath)
        decoder = Decoder(stream)
        messages, _ = decoder.read()

    except Exception as e:
        print(f"FATAL ERROR: Unable to read data from {filepath}: {e}")
        return
    
    try:
        manufacturer = messages.get('device_info_mesgs',[{}])[0].get('manufacturer', "N/A")
        weight = messages.get('user_profile_mesgs',[{}])[0].get('weight',66.66)
        time= messages["record_mesgs"][0]["timestamp"].strftime("%H%M%S")
        date= messages["record_mesgs"][0]["timestamp"].strftime("%Y-%m-%d")
        date = date if date else "1900-10-17"
        

    except Exception as e:
        print(f"Error in extract_data function:\nManufacturer set to N/A weight to 66.66, date to 1900-10-17, {e}")

    #Extract strings for csv filename
    # filename = f"{name_id}-{date}-{time}"
    # directory = os.path.dirname(filepath)
    # csv_filename = os.path.join(directory, f"{filename}")
    try:
        data = messages.get("record_mesgs",[])
        if not data:
            print(f"WARNING: No data in {filepath}")
            data_df= pd.DataFrame()
        
        data_df=pd.DataFrame(data)

    except Exception as e:
        print(f"Error extracting records from file. DataFrame will be empty {filepath}: {e}")
        data_df=pd.DataFrame()

    '''
    Takes raw data extracted metadata from a .fit file
    and applies feature engineer, creates new metrics and select the columns 
    to include in the resulting DataFrame. Resulting data_df will be
    written in a .csv file.
    '''

    if  data_df.empty:
        print(f"WARNING: No data in DataFrame. Returning empty DataFrame")
        data_df=pd.DataFrame(data_columns)

    else:

        
        data_df["elapsed_time"]= pd.to_datetime(range(len(data_df)), unit="s").strftime("%H:%M:%S")
        # data_df["time_offset"]= pd.Series(range(len(data_df)))
        semicircles_to_degrees= (180 / 2**31)
        data_df["position_lat"] = np.round(data_df.get("position_lat", np.nan) * semicircles_to_degrees,8)
        data_df["position_long"] = np.round(data_df.get("position_long", np.nan) * semicircles_to_degrees,8)
        data_df["distance"] = np.round(data_df.get("distance", np.nan) / 1000,3)
        data_df["elevation"] = np.round(data_df.get("altitude", np.nan),2)
        data_df["speed"] = np.round(data_df.get("enhanced_speed", np.nan) * 3.6,3)
        data_df["work"]= np.round(data_df.get("accumulated_power", np.nan)/1000,2)
        
        # df["respiration_rate"] = np.round(df["enhanced_respiration_rate"])

        if weight:
            data_df["w_kg"] = np.round(data_df.get("power",np.nan) / weight,2)
            data_df["kj_kg"]= np.round(data_df.get("work", np.nan) / weight,2)

        power_phase_columns= {"left_power_phase": ["left_power_phase_start","left_power_phase_end"],
                            "right_power_phase": ["right_power_phase_start","right_power_phase_end"],
                            "left_power_phase_peak": ["left_power_peak_start","left_power_peak_end"],
                            "right_power_phase_peak": ["right_power_peak_start","right_power_peak_end"]
                            }
        
        for key, new_cols in power_phase_columns.items():
            if key in data_df.columns:
                data_df[new_cols[0]]= np.round(data_df[key].str[0].astype(float),2)
                data_df[new_cols[1]]= np.round(data_df[key].str[1].astype(float),2)
        
        if "left_right_balance" in data_df.columns:
            if manufacturer =="garmin":
                data_df["balance_right"] = data_df["left_right_balance"] - 128
                data_df["balance_left"] = 100 - (data_df["left_right_balance"] - 128)
            else:
                data_df["balance_right"] = 100 - data_df["left_right_balance"]
                data_df["balance_left"] = data_df["left_right_balance"]

        pedaling_metrics= ["left_torque_effectiveness",
                        "right_torque_effectiveness",
                        "left_pedal_smoothness",
                        "right_pedal_smoothness"]

        for col in pedaling_metrics:
            data_df[col]= data_df.get(col, np.nan)
        
        for col in data_columns:
            if col not in data_df.columns:
                data_df[col]= np.nan
        data_df = data_df[data_columns].copy()

    '''
    Takes a .fit file and parse it with garmin_fit_sdk library
    and drops data msgs into pd.DataFrame object.
    '''
    concat_df= []
    try:
        device = messages.get('device_info_mesgs', [])
        if not device:
            print(f"WARNING: No device info in {filepath}")
            device= pd.DataFrame()

        device_df = pd.DataFrame(device,columns=device_data)
        device_df= device_df.loc[[0],]
        concat_df.append(device_df)

        user_profile= messages.get("user_profile_mesgs", [])

        if not user_profile:
            print(f"WARNING: No user profile info in {filepath}")
            user_profile= pd.DataFrame()

        user_profile_df = pd.DataFrame(user_profile, columns=user_profile_data)
        concat_df.append(user_profile_df)  
    
        session = messages.get("session_mesgs", [])

        if not session:
            print(f"WARNING: No session info in {filepath}")
            session= pd.DataFrame()

        session_df = pd.DataFrame(session, columns=session_data)
        concat_df.append(session_df)
        metadata_df= pd.concat(concat_df,axis=1)

    except Exception as e:
        print(f"Error extracting metadata from file. DataFrame will be empty {filepath}: {e}")
        metadata_df=pd.DataFrame()

    '''
    Takes raw metadata extracted metadata from a .fit file
    and applies feature engineer, creates new metrics and select the columns 
    to include in the resulting DataFrame. Resulting metadata_df will be
    written in a .csv file.
    '''

    if metadata_df.empty:
        print(f"WARNING: No metadata in DataFrame. Returning empty DataFrame")
        metadata_df= pd.DataFrame(columns=columns_metadata)

    else:
        
        

        metadata_df["total_time"]= metadata_df["total_elapsed_time"].apply(\
        lambda x: f"{int(x//3600):02}:{int(x % 3600//60):02}:{int(x % 60):02}")

        metadata_df["ride_time"]= metadata_df["total_timer_time"].apply(\
        lambda x: f"{int(x//3600):02}:{int(x % 3600//60):02}:{int(x % 60):02}")

        metadata_df["avg_speed"]= np.round(metadata_df.get("avg_speed",np.nan)*3.6,2)
        metadata_df["max_speed"]= np.round(metadata_df.get("max_speed",np.nan)*3.6,2)
        metadata_df["distance"]= np.round(metadata_df.get("total_distance",np.nan)/1000,2)
        metadata_df["work_kj"]= np.round(metadata_df.get("total_work",np.nan)/1000,2)
        metadata_df["calories"]= np.round(metadata_df.get("total_calories",np.nan),2)
        metadata_df["training_stress_score"]= np.round(metadata_df.get("training_stress_score",np.nan),2)
        metadata_df["intensity_factor"]= np.round(metadata_df.get("intensity_factor",np.nan),2)
        metadata_df["avg_vam"]= np.round(metadata_df.get("avg_vam",np.nan),2)
        
        


        for col in columns_metadata:
            if col not in metadata_df.columns:
                metadata_df[col]= np.nan

        metadata_df= metadata_df[columns_metadata].copy()

    return data_df, metadata_df  #csv_filename, filepath


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

def process_and_insert(filepath:str, athlete_df):

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

    # save_to_csv(data_df, metadata_df, csv_filename, filepath)
