import json

f = open('link.json')
link = json.load(f)
counter = 0
file_counter = 0
quota = 100
data = []
for entry in link:
    counter += 1
    data.append(entry)
    if counter == quota :
        filename = 'split/link_' + str(file_counter) + '.json'
        f = open(filename, 'w+')
        f.write(json.dumps(data))
        f.close()
        data = []
        counter = 0
        file_counter += 1
        quota += 100
if data:
    filename = 'split/link_' + str(file_counter) + '.json'
    f = open(filename, 'w+')
    f.write(json.dumps(data))
    f.close()
        