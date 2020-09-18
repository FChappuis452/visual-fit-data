
def json_extract(json_data, page):
    """
    Returns a dictionary of dates with its corresponding data
    Depending on the API call the JSON will be laid out differently at key
    position or missing if no activity was recorded for the time period so 
    this brute force approach was used

    :param json_data: JSON from the API to parse
    :param page: str for the type of data being retrieved 
    """
    
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