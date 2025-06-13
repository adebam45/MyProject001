# Write your code here!
# print ("I learn Python!")
# print (17 + 35 * 2)

# Do not modify the code below

import csv

# Data Extract
def data_extract():
    employee_data_extract = []
    with open('C:/Users/ayoba/PycharmProjects/AyobamiPythonProject/MyProject001/P3/P3C3/statement/input.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            employee_data_extract.append(row)
    return employee_data_extract

# Data Transformation
def transform_data(data_to_change):
    salary_data = []
    for data in data_to_change:
        change_data = {}
        change_data["name"] = data["name"]
        salary = int(data["hours_worked"]) * 15
        change_data["salary"] = str(salary)
        salary_data.append(change_data)
    return salary_data  # Make sure this is outside the for-loop

# Data Load
def load(change_data):
    with open('C:/Users/ayoba/PycharmProjects/AyobamiPythonProject/MyProject001/P3/P3C3/statement/output.csv', mode='w', newline='') as file:
        fieldnames = ['name', 'salary']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in change_data: 
            writer.writerow(data)

# Main function
def main():
    data_to_change = data_extract()
    change_data = transform_data(data_to_change)
    load(change_data)
    print("Salary data written to output.csv")

# Run main
if __name__ == "__main__":
    main()