import pandas as pd 
import numpy as np
import sys 
import json

def data_collection(): 
    n = len(sys.argv)
    print("Total arguments passed: ", n)
    print("\nname of python script: ", sys.argv[0])
    print("\n dialog file: ", sys.argv[3])  

    data = pd.read_csv(sys.argv[3]) 
    total = len(data)
    count_twilight_sparkle = len(data[data['pony'] == "Twilight Sparkle"])
    count_applejack = len(data[data['pony'] == "Applejack"])
    count_rarity = len(data[data['pony'] == "Rarity"])
    count_pinkie_pie = len(data[data['pony'] == "Pinkie Pie"])
    count_rainbow_dash = len(data[data['pony'] == "Rainbow Dash"])
    count_fluttershy = len(data[data['pony'] == "Fluttershy"])

    verbosity_twilight_sparkle = count_twilight_sparkle / total
    verbosity_applejack = count_applejack / total
    verbosity_rarity = count_rarity / total
    verbosity_pinkie_pie = count_pinkie_pie / total
    verbosity_rainbow_dash = count_rainbow_dash / total
    verbosity_fluttershy = count_fluttershy / total

    print(len(data))
    print(count_twilight_sparkle)
    print(count_applejack)
    print(count_rarity)
    print(count_pinkie_pie)
    print(count_rainbow_dash)
    print(count_fluttershy)
    print(len(data))
    print("------------------------")
    print(verbosity_twilight_sparkle)
    print(verbosity_applejack)
    print(verbosity_rarity)
    print(verbosity_pinkie_pie)
    print(verbosity_rainbow_dash)
    print(verbosity_fluttershy)

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
            "twilight sparkle": round(verbosity_twilight_sparkle, 3), 
            "applejack": round(verbosity_applejack, 3), 
            "rarity": round(verbosity_rarity, 3), 
            "pinkie pie": round(verbosity_pinkie_pie, 3), 
            "rainbow dash": round(verbosity_rainbow_dash, 3), 
            "fluttershy": round(verbosity_fluttershy, 3)
        }
    }

    '''
    json_result['count'] = { 
        "twilight sparkle": count_twilight_sparkle, 
        "applejack" : count_applejack, 
        "rarity": count_rarity, 
        "pinkie pie": count_pinkie_pie, 
        "rainbow dash": count_rainbow_dash, 
        "fluttershy": count_fluttershy
    },

    json_result['verbosity'] = { 
        "twilight sparkle": verbosity_twilight_sparkle, 
        "applejack": verbosity_applejack, 
        "rarity": verbosity_rarity, 
        "pinkie pie": verbosity_pinkie_pie, 
        "rainbow dash": verbosity_rainbow_dash, 
        "fluttershy": verbosity_fluttershy
    }

     with open(sys.argv[1], 'w') as outfile: 
        json.dump(json_result, outfile, indent=4)

'''

    with open(sys.argv[2], 'w') as outfile: 
            json.dump(json_result, outfile, indent=4)



   




if __name__ == "__main__": 
    data_collection()