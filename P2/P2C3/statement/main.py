# Write your code here!
#Function for monthly salary
def monthly_salary(annual_salary)
return annual_salary/12

#Function for weekly salary
def weekly_salary(monthly_salary)
return monthly_salary/4

#function of parameters for the weekly salary and the number of hours worked per week
def hourly_salary(weekly_salary, hours_worked)
return weekly_salary/hours_worked

def_main():
    #Ask the user to enter their annual salary.
    annual_salary = float(input("Enter your annual salary : "))

    #Ask the user to enter the number of hours worked per week.
    hours_worked = float(input("Enter the number of hours worked per week : "))

    #Call the previously created functions to calculate the corresponding hourly wage.
    monthly = monthly_salary(annual_salary)
    weekly = weekly_salary(monthly)
    hourly = hourly_salary(weekly, hours_worked)


    #Display the result in the format: 
    print("Your hourly salary is",  hourly, "euros.")

# Do not modify the code below
if __name__ == "__main__":
    main()
