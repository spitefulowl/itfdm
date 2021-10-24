def get_descendants(size, vertex):
    result = set([item for item in range(1, size + 1)])
    for item in vertex:
        result.remove(item)
    return result

def get_time(task, vertex):
    time = task.delivery_matrix[0, vertex[0]]
    for idx in range(1, len(vertex)):
        time += task.delivery_matrix[vertex[idx - 1], vertex[idx]]

    return time

# global_crit_cache = {}

def get_crit(task, vertex):
    # global global_crit_cache
    # cached_value = global_crit_cache.get(vertex)
    # if cached_value:
    #     return cached_value

    result = 0
    time = task.delivery_matrix[0, vertex[0]]
    if time > task.target_dates[vertex[0] - 1]:
        result += 1

    for idx in range(1, len(vertex)):
        time += task.delivery_matrix[vertex[idx - 1], vertex[idx]]
        if time > task.target_dates[vertex[idx] - 1]:
            result += 1

    # global_crit_cache[vertex] = result
    return result
