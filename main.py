import json

class Employee:
    def __init__(self, emp_id, name, base_salary):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary

    def get_info(self):
        pass

class PermanentEmployee(Employee):
    def __init__(self, emp_id, name, base_salary, bonus_code):
        super().__init__(emp_id, name, base_salary)
        self.bonus_code = bonus_code

    def get_info(self):
        bonus = 0
        if self.bonus_code == "PERF2026": bonus = 2000000
        elif self.bonus_code == "SENIOR10": bonus = 3000000
        elif self.bonus_code == "LEAD2026": bonus = 5000000
        total_salary = self.base_salary + bonus
        return f"[TETAP] {self.emp_id} - {self.name} | Gaji Total: Rp{total_salary:,.0f} (Termasuk Bonus)"

class ContractEmployee(Employee):
    def get_info(self):
        return f"[KONTRAK] {self.emp_id} - {self.name} | Gaji Total: Rp{self.base_salary:,.0f} (Tanpa Bonus)"

class Sensor:
    def __init__(self, sensor_id, location, temperature, status):
        self.sensor_id = sensor_id
        self.location = location
        self.temperature = temperature
        self.status = status

    def check_alert(self):
        pass

class MonitoredSensor(Sensor):
    def __init__(self, sensor_id, location, temperature, status, operator_id):
        super().__init__(sensor_id, location, temperature, status)
        self.operator_id = operator_id

    def check_alert(self):
        return f"[{self.status}] {self.sensor_id} di {self.location} | Suhu: {self.temperature}°C | Diawasi Operator: {self.operator_id}"

class UnmonitoredSensor(Sensor):
    def check_alert(self):
        peringatan = f"[{self.status}] {self.sensor_id} di {self.location} | Suhu: {self.temperature}°C | TIDAK ADA OPERATOR!"
        if self.status == "DANGER":
            peringatan += " -> PERINGATAN KRITIS: SEGERA KIRIM TIM DARURAT BROO!"
        return peringatan


def main():
    employees_list = []
    sensors_list = []

    try:
        with open('employee.json', 'r') as file:
            data_emp = json.load(file)
            for emp in data_emp['employees']:
                if emp['is_permanent']:
                    employees_list.append(PermanentEmployee(emp['emp_id'], emp['name'], emp['base_salary'], emp['bonus_code']))
                else:
                    employees_list.append(ContractEmployee(emp['emp_id'], emp['name'], emp['base_salary']))
    except FileNotFoundError:
        print("File employee.json tidak ditemukan!")

    try:
        with open('sensor_logs.json', 'r') as file:
            data_sns = json.load(file)
            for sns in data_sns['readings']:
                if sns['operator_id'] is not None:
                    sensors_list.append(MonitoredSensor(sns['sensor_id'], sns['location'], sns['temperature'], sns['status'], sns['operator_id']))
                else:
                    sensors_list.append(UnmonitoredSensor(sns['sensor_id'], sns['location'], sns['temperature'], sns['status']))
    except FileNotFoundError:
        print("File sensor_logs.json tidak ditemukan!")

    print("=== DATA KARYAWAN ===")
    for employee in employees_list:
        print(employee.get_info())

    print("\n=== DATA SENSOR ===")
    for sensor in sensors_list:
        print(sensor.check_alert())

if __name__ == "__main__":
    main()