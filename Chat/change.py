print("입력후 Ctrl-z")
contents = []

while True:
    try:
        line = input()
    except EOFError:
        break
    contents.append(line)

for i in contents:
    name = i.split(':')[1]
    print(f"    '{name}': '{i}',")