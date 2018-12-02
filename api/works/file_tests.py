def test_value_function(file, function_name, value):
    exec(file.read())
    return True if locals()[function_name]() == value else False

def test_type_function(file, function_name, type):
    exec(file.read())
    return True if type(locals()[function_name]()) == type else False
