import numpy as np
from arcgis import geometry

def make_new_range(arr_raw):
    arr = np.array(arr_raw, dtype=int)
    max_num = arr.max()

    result = np.zeros((max_num, len(arr)), dtype=int)

    for i in range(max_num):
        result[i] = (arr > i).astype(int)
    
    return np.array(result, dtype=str)


def expand_row_with_range(original_row, check_cells, transformed_range):
    prefix = [original_row[i] for i in range(min(check_cells))]
    suffix = [original_row[i] for i in range(max(check_cells) + 1, len(original_row))]

    result_rows = []
    for r in transformed_range:
        row = prefix + list(r) + suffix
        
        result_rows.append(row)

    return result_rows


def get_cells_to_update(argument, row):
    check_cells = []
    header_row = row["values"][0]

    for i, h_row in enumerate(header_row):
        if argument in  h_row:
            check_cells.append(i)

    return check_cells

def get_mapping():
    return [
    {"name": "date_1", "source": "Дата"},
    {"name": "Область", "source": "Область"},
    {"name": "city", "source": "Місто"},
    {"name": "value_1", "source": "Значення_1"},
    {"name": "value_2", "source": "Значення_2"},
    {"name": "value_3", "source": "Значення_3"},
    {"name": "value_4", "source": "Значення_4"},
    {"name": "value_5", "source": "Значення_5"},
    {"name": "value_6", "source": "Значення_6"},
    {"name": "value_7", "source": "Значення_7"},
    {"name": "value_8", "source": "Значення_8"},
    {"name": "value_9", "source": "Значення_9"},
    {"name": "value_10", "source": "Значення_10"},
    {"name": "long", "source": "long"},
    {"name": "lat", "source": "lat"},
    {"name": "OBJECTID", "source": "ObjectId"},
]


def get_n_mapping(gis, data):
    x = float(str(data.get("long")).replace(',', '.'))
    y = float(str(data.get("lat")).replace(',', '.'))


    input_geometry = {'y':y,'x':x}
    output_geometry = geometry.project(geometries = [input_geometry],
                                       in_sr = 4326, 
                                       out_sr = 3857,
                                    gis = gis)
 
    return {
        "attributes": {
            "d_date": data.get("Дата"),
            "t_region": data.get("Область"),
            "city": data.get("Місто"),
            "value_1": data.get("Значення 1"),
            "value_2": data.get("Значення 2"),
            "value_3": data.get("Значення 3"),
            "value_4": data.get("Значення 4"),
            "value_5": data.get("Значення 5"),
            "value_6": data.get("Значення 6"),
            "value_7": data.get("Значення 7"),
            "value_8": data.get("Значення 8"),
            "value_9": data.get("Значення 9"),
            "value_10": data.get("Значення 10"),
            "long" : x,
            "lat" :  y
        },
        "geometry": output_geometry[0]
    }

