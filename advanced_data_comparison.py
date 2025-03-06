
differences = []

def is_same(data1, data2):
    if is_same_entity(data1, data2):
        return True, None
    else:
        return False, differences

def is_same_entity(data1, data2):
    differences.append(f"Comparing DATA1: {data1} and DATA2: {data2} > ")
    # If list
    if isinstance(data1, list) and isinstance(data2, list):
        same = is_same_list(data1, data2)
    # If dictionary
    elif isinstance(data1, dict) and isinstance(data2, dict):
        same = is_same_dict(data1, data2)
    # if primitive
    else:
        same = data1 == data2
    if same:
        differences.append("They were equal!")
        return same
    else:
        differences.append(f"{data1} did NOT equal... {data2}")
        return same


def is_same_list(data1, data2) -> bool:
    same = True

    if len(data1) != len(data2):
        same = False
    else:
        for i in range(len(data1)):
            if not is_same_entity(data1[i], data2[i]):
                same = False

                break
    return same

def is_same_dict(data1, data2) -> bool:
    same = True

    if len(data1) != len(data2):
        same = False
    else:
        for key, value in data1.items():
            if not is_same_entity(data1[key], data2[key]):
                same = False

                break
    return same

print(is_same([1],[1]))
print(is_same([1],[2]))
print(is_same({"key": 1},{"key": 1}))
print(is_same({"key": 1},{"key": 1, "key2": 2}))
print(is_same({"key": 1},{"key": 2}))
sample_data1 = {
    'a': '1',
    'b': 2,
    'c': {'a': 1, 'b': [1, 2, 3], 'c': None, 'd': False},
    'd': [1, 2, [3, 4, 5], {'e': 'e1', 'f': 'f1'}, True, None],
    'e': True,
    'f': None
}
sample_data2 = {
    'a': 1,
    'b': '2',
    'c': {'a': '1', 'b': [1, 2, 3, 4], 'c': None, 'd': True},
    'd': [1, 2, [3, 4, 5], {'e': 'e1', 'f': 'f1'}, True],
    'e': True
}
print(is_same(sample_data1, sample_data2))