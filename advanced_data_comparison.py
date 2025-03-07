
differences = []

def is_same(data1, data2) -> tuple[bool, str|None]:
    if is_same_entity(data1, data2, 0):
        return True, None
    else:
        return False, "\n".join(differences)

def is_same_entity(data1, data2, depth: int) -> bool:
    differences.append(comparison_output(data1, data2, depth))
    # If list
    if isinstance(data1, list) and isinstance(data2, list):
        same = is_same_list(data1, data2, depth)
    # If dictionary
    elif isinstance(data1, dict) and isinstance(data2, dict):
        same = is_same_dict(data1, data2, depth)
    # if primitive
    else:
        same = data1 == data2
    if same:
        differences.append(equal_output(data1, data2, depth))
        return same
    else:
        differences.append(not_equal_output(data1, data2, depth))
        return same

def is_same_list(data1, data2, depth) -> bool:
    depth+=1
    same = True
    if len(data1) != len(data2):
        differences.append(diff_size_output(data1, data2, depth))
        same = False
    else:
        for i in range(len(data1)):
            if not is_same_entity(data1[i], data2[i], depth):
                same = False
    if same: differences.append(equal_output(data1, data2, depth))
    return same

def is_same_dict(data1, data2, depth) -> bool:
    depth += 1
    same = True
    if len(data1) != len(data2):
        differences.append(diff_size_output(data1, data2, depth))
        same = False
    else:
        for key, value in data1.items():
            if not is_same_entity(data1[key], data2[key], depth):
                same = False
    if same: differences.append(equal_output(data1, data2, depth))
    return same

def comparison_output(data1, data2, depth: int) -> str:
    data1_text = truncated_data_text(data1)
    data2_text = truncated_data_text(data2)
    return f"{get_tabs(depth)}Comparing DATA1=> {data1_text} and DATA2=> {data2_text}"

def diff_size_output(data1, data2, depth: int) -> str:
    depth += 1
    return f"{get_tabs(depth)}DATA1 was size {len(data1)} and DATA2 was size {len(data2)}"

def not_equal_output(data1, data2, depth: int) -> str:
    depth += 1
    data1_text = truncated_data_text(data1)
    data2_text = truncated_data_text(data2)
    return f"{get_tabs(depth)}> {data1_text} did NOT equal {data2_text}"

def equal_output(data1, data2, depth: int) -> str:
    depth += 1
    data1_text = truncated_data_text(data1)
    data2_text = truncated_data_text(data2)
    return f"{get_tabs(depth)}> {data1_text} did equal {data2_text}!"

def truncated_data_text(data) -> str:
    data_text = str(data)
    length_limit = 50
    return data_text if (len(data_text)) < length_limit else data_text[0:length_limit] + "..."

def get_tabs(depth: int) -> str:
    return str("\t" * depth)

def print_is_same(result: tuple[bool, str]):
    print(result[0])
    print(result[1])

print_is_same(is_same([1],[1]))
print_is_same(is_same([1],[2]))
print_is_same(is_same({"key": 1},{"key": 1}))
print_is_same(is_same({"key": 1},{"key": 2}))
print_is_same(is_same({"key": 1},{"key": 1, "key2": 2}))
print_is_same(is_same({"key": 1, "key2": 1},{"key": 1, "key2": 2}))
print_is_same(is_same([1,2,3,4,5,6,7,8,9],[9,8,7,6,5,4,3,2,1]))
print_is_same(is_same({"key": 1, "key2": { "inner_key1": 1 }},{"key": 1, "key2": { "inner_key1": 2 }}))
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
print_is_same(is_same(sample_data1, sample_data2))