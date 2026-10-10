import time

current_struct = time.localtime()
formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", current_struct)
print(formatted_time)
