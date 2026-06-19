repeat = True

while repeat:
    try:
        command = str(input('Please Select one of the following: +, -, *, /, %, or quit  '))
        x = int(input('Please enter a positive integer greater than 0  '))
        y = int(input('Please enter a positive integer greater than 0  '))

        match command:
            case "+":
                print(f"{x} {command} {y} = {x + y}")

            case "-":
                print(f"{x} {command} {y} = {x - y}")

            case "*":
                print(f"{x} {command} {y} = {x * y}")

            case "/":
                print(f"{x} {command} {y} = {x / y}")

            case "%":
                print(f"{x} {command} {y} = {x % y}")

            case "quit":
                print("Exiting...")
                repeat = False

            case _:
                print("You entered an invalid command!")

    except KeyboardInterrupt:
        repeat = False
