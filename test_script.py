from tasks import finalize_data
json_file_path = 'enterprises.json'
result = finalize_data.delay(json_file_path)
print(result.get())