def split_command_string(command_string):
    parts = command_string.split()
    if len(parts) > 0:
        return parts
    else:
        return []

# Example usage:
input_string = "coolCommand arg1 arg2 arg3"
result = split_command_string(input_string)
print(result)
