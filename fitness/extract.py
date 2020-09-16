"""Extract nested values from a JSON tree."""


def json_extract(json_data, page):
    date_object = {
        "dates" : [],
        "fitness_data" : [],
    }

    for idx, bucket in enumerate(json_data['bucket']):
        date_object['dates'].append(json_data['bucket'][idx]['startTimeMillis'])
        try:
            if page == "steps":
                date_object['fitness_data'].append(json_data['bucket'][idx]['dataset'][0]['point'][0]['value'][0]['intVal'])
            elif page == "calories":
                date_object['fitness_data'].append(json_data['bucket'][idx]['dataset'][0]['point'][0]['value'][0]['fpVal'])
        except IndexError:
            date_object['fitness_data'].append(0)

    return date_object
