input = ''''''

list = list(map(str, input.split()))


for i in list:
    name = i.split(':')[1]
    print(f"    '{name}': '{i}',")