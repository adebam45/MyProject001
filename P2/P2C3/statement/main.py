# Write your code here!
# Create a function for monthly salary using weekly salary as a parameter
def monthly_salary(annual_salary):

   # return the annual_salary and divide by 12
    return annual_salary/12

# Create a function for annual salary using weekly salary as a parameter   
def weekly_salary(monthly_salary):

  # return the annual_salary and divide by 4
    return monthly_salary/4

# Create a function to calculate hour  worked
def hourly_wage(weekly_salary, hours_worked):
    return weekly_salary/hours_worked

# Main function to bring all the parameters together
def main():
    # Ask user for annual salary and hours worked per week
    annual = float(input("Annual salary input:"))
    hours = float(input("Number of hours worked per week:"))

    # Calculations using the defined functions
    monthly = monthly_salary (annual)
    weekly = weekly_salary (monthly)
    hourly = hourly_wage (weekly,hours)

    # Display the result
    print ("The hourly wage is", hourly, "dollars")

# Do not modify the code below
if __name__ == "__main__":
    main()