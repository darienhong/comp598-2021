import pandas as pd 
import numpy as np
import sys 
import json

def data_collection(): 
    '''
    n = len(sys.argv)
    print("Total arguments passed: ", n)
    print("\nname of python script: ", sys.argv[0])
    print("\n dialog file: ", sys.argv[3]) 
    ''' 

    data = pd.read_csv(sys.argv[3]) 
    total = len(data)
    count_twilight_sparkle = len(data[data['pony'].str.casefold() == "Twilight Sparkle".casefold()])
    count_applejack = len(data[data['pony'].str.casefold() == "Applejack".casefold()])
    count_rarity = len(data[data['pony'].str.casefold() == "Rarity".casefold()])
    count_pinkie_pie = len(data[data['pony'].str.casefold() == "Pinkie Pie".casefold()])
    count_rainbow_dash = len(data[data['pony'].str.casefold() == "Rainbow Dash".casefold()])
    count_fluttershy = len(data[data['pony'].str.casefold() == "Fluttershy".casefold()])

    verbosity_twilight_sparkle = count_twilight_sparkle / total
    verbosity_applejack = count_applejack / total
    verbosity_rarity = count_rarity / total
    verbosity_pinkie_pie = count_pinkie_pie / total
    verbosity_rainbow_dash = count_rainbow_dash / total
    verbosity_fluttershy = count_fluttershy / total

    json_result = {
        "count": { 
            "twilight sparkle": count_twilight_sparkle, 
            "applejack" : count_applejack, 
            "rarity": count_rarity, 
            "pinkie pie": count_pinkie_pie, 
            "rainbow dash": count_rainbow_dash, 
            "fluttershy": count_fluttershy
        },

        "verbosity": { 
            "twilight sparkle": round(verbosity_twilight_sparkle, 2), 
            "applejack": round(verbosity_applejack, 2), 
            "rarity": round(verbosity_rarity, 2), 
            "pinkie pie": round(verbosity_pinkie_pie, 2), 
            "rainbow dash": round(verbosity_rainbow_dash, 2), 
            "fluttershy": round(verbosity_fluttershy, 2)
        }
    }

    with open(sys.argv[2], 'w') as outfile: 
            json.dump(json_result, outfile, indent=4)


if __name__ == "__main__": 
    data_collection()