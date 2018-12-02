def test_value_function(file, function_name, value):
    exec(file)
    try:
        return True if locals()[function_name]() == value else False
    except KeyError:
        return False

def test_type_function(file, function_name, type):
    exec(file)
    try:
        return True if type(locals()[function_name]()) == type else False
    except KeyError:
        return False
