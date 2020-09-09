"""Extract nested values from a JSON tree."""


def json_extract(json_data):
    #fields['steps'] = json_extract(reply, 'intVal')
    # print("<<<<<<<<<<<<<<<<<FIELD STEP>>>>>>>>>>>>>>")
    # print(f"{reply['bucket'][0]['startTimeMillis']}")
    # try:
    #     print(f"{reply['bucket'][0]['dataset'][0]['point'][0]['value'][0]['intVal']}")
    # except IndexError:
    #     print("0")
    # print(f"{reply['bucket'][1]['startTimeMillis']}")
    # print(f"{reply['bucket'][1]['dataset'][0]['point'][0]['value'][0]['intVal']}")

    date_object = {
        "dates" : [],
        "fitness_data" : [],
    }

    for idx, bucket in enumerate(json_data['bucket']):
        date_object['dates'].append(json_data['bucket'][idx]['startTimeMillis'])
        try:
            date_object['fitness_data'].append(json_data['bucket'][idx]['dataset'][0]['point'][0]['value'][0]['intVal'])
        except IndexError:
            date_object['fitness_data'].append(0)

    return date_object