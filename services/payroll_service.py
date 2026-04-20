import datetime


class PAYROLL_MANAGEMENT:
    def __init__(self, db):
        self.db = db
        self.collection = db['payroll']

        self.basic_salaries = {
            "Driver": 30000,
            "Conductor": 20000,
            "Manager": 80000,
            "HR": 50000,
            "Finance": 60000,
            "IT": 70000
        }

        self.tax_rate = 0.15

    def calculate_payroll(self, payroll_data):
        """Calculates and stores payroll record."""

        try:
            position = payroll_data.get("position", "Unknown").title()

            basic_salary = self.basic_salaries.get(position, 0)

            allowances = float(payroll_data.get("allowances", 0))
            deductions = float(payroll_data.get("deductions", 0))

            gross_salary = basic_salary + allowances
            tax_amount = round(gross_salary * self.tax_rate, 2)
            net_salary = round(gross_salary - deductions - tax_amount, 2)

            payroll_record = {
                "employee_name": payroll_data.get("employee_name", "Unknown"),
                "position": position,
                "basic_salary": basic_salary,
                "allowances": allowances,
                "deductions": deductions,
                "gross_salary": gross_salary,
                "tax_amount": tax_amount,
                "net_salary": net_salary,
                "calculation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.collection.insert_one(payroll_record)

            return {
                "message": "Payroll saved successfully!"
            }, 201

        except Exception as e:
            return {
                "error": f"Error calculating payroll: {str(e)}"
            }, 500

    def view_records(self):
        """Retrieves payroll records."""

        try:
            records = list(self.collection.find())

            for record in records:
                record["_id"] = str(record["_id"])

            return {"records": records}, 200

        except Exception as e:
            return {
                "error": f"Error viewing payroll records: {str(e)}"
            }, 500