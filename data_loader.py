import pandas as pd  # type: ignore

def get_employee_data(employee_id):
    employees_df = pd.read_csv('employees.csv')
    employee_data = employees_df[employees_df['EmployeeID'] == int(employee_id)].to_dict('records')
    if employee_data:
        return employee_data[0]
    else:
        return None
