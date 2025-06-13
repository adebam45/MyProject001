def main():
        # Step 1: Create two variables left_number and right_number with input()
    left_number = input("I can enter any input number here:(e.g 20)")
    right_number = input("I can enter any input number here:(e.g 10)")

    # Step 2: Create the operation variable (symbol)
    operation = input("['+','-','*', or '/']:")

    # Step 3: Initialize the result variable
    result = 0

    # Step 4: Check if both left_number and right_number are integers
    if not left_number.isnumeric() or not right_number.isnumeric():
        print("Error: both numbers must be integers")
        return
    else:
        # Convert to integers
        left_number = int(left_number)
        right_number = int(right_number)

    # Step 5: Use match to handle the operation symbol and calculate
    match operation:
        case "+":
            result = left_number + right_number
        case "-":
            result = left_number - right_number
        case "*":
            result = left_number * right_number
        case "/":
            # Check for division by zero
            if right_number == 0:
                print("Error: division by zero is not allowed")
                return
            else:
                result = left_number / right_number
        case _:
            print("Error: the operation symbol must be '+', '-', '*', or '/'.")
            return

    # Step 6: Display the result
    print(f"Result: {left_number} {operation} {right_number} = {result}")

# Do not modify the code below
if __name__ == "__main__":
    main()