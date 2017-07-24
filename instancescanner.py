import mods
while True:
    command = input("~ ")
    
    if command == "-s":
        mods.scan()

    elif command[:2] == "-d":
        mods.display(command[3:])

    elif command == "-a":
        mods.all()

    elif command[:2] == "-r":
        mods.remove(command[3:])