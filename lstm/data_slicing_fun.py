from features_extracting_fun import features_extracting


# this function receives pre-processed data and turn them into format acceptable to ML model
# titles of data should be removed
# first column of data should be timestamp
# t should be transform to the same scale as timestamp
# this function return a matrix[[n_max, features]...] or nothing
def slice_data(data, t, n_min, n_max, m):
    result = []
    temp_data = []
    start_time = data[0][0]
    for i in range(0, len(data)):
        if data[i][0] < start_time + t:
            temp_data.append(data[i])
        else:
            result.append(features_extracting(temp_data))
            temp_data.clear()
            start_time = data[i][0]
            temp_data.append(data[i])
    if len(result) < n_min:
        return
    elif n_min <= len(result) < n_max:
        padding = [0 for i in range(0, 14)]
        while len(result) < n_max:
            result.append(padding)
        return [].append(result)
    else:
        result_pro = []
        for i in range(0, len(result), m):
            temp_result = []
            if i + n_max <= len(result):
                for j in range(i, i + n_max):
                    temp_result.append(result[j])
            else:
                for j in range(i, len(result)):
                    temp_result.append(result[j])
                padding = [0 for j in range(0, 14)]
                while len(temp_result) < n_max:
                    temp_result.append(padding)
            result_pro.append(temp_result)
        return result_pro
