def main():
#  I added a list of integers separated by commas (e.g., `1,2,3,4`)
    numbers =  input("Any list of integers should be entered here (e.g., 1,2,3,4,5): ")

    # Use split() to create a list of strings from the input
    numbers=numbers.split(",")

    # Display the list of numbers
    print ("The list of numbers is:", numbers)


    # Calculate the sum using a for loop
    total_sum = 0
    for x in numbers:
        total_sum += int(x)
    print ("sum of numbers:",total_sum)


    # Calculate the average
    average = total_sum/len(numbers)
    print ("Average of number:", average)

    # Count how many numbers are greater than the average 
    greater_than_average = 0
    for x in numbers:
        if int(x) > average:
            greater_than_average +=1
    print("Number of numbers that are greater than the average:",greater_than_average)

    # Count how many numbers are even using "while" loop
    even_number = 0
    index = 0
    while index < len(numbers):
        if int(numbers[index]) % 2 == 0:
            even_number += 1
        index +=1
    print("Number of even numbers:", even_number)

# Do not modify the code below
if __name__ == "__main__":
    main()