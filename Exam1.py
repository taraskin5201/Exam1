import json
import re
from datetime import date
from typing import List

class Employee:
    def __init__(self, name: str, position: str, phone: str, email: str):
        self.name = name
        self.position = position
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"ПІБ: {self.name}, Посада: {self.position}, Телефон: {self.phone}, Email: {self.email}"

class Car:
    def __init__(self, manufacturer: str, year: int, model: str, cost_price: float, selling_price: float):
        self.manufacturer = manufacturer
        self.year = year
        self.model = model
        self.cost_price = cost_price
        self.selling_price = selling_price

    def __str__(self):
        return f"Виробник: {self.manufacturer}, Рік: {self.year}, Модель: {self.model}, Собівартість: {self.cost_price}, Ціна продажу: {self.selling_price}"

class Sale:
    def __init__(self, employee: Employee, car: Car, sale_date: str, actual_price: float):
        self.employee = employee
        self.car = car
        self.sale_date = sale_date
        self.actual_price = actual_price

    def __str__(self):
        return f"Співробітник: {self.employee}, Автомобіль: {self.car}, Дата продажу: {self.sale_date}, Реальна ціна: {self.actual_price}"

class Dealership:
    def __init__(self):
        self.employees = []
        self.cars = []
        self.sales = []

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def remove_employee(self, employee: Employee):
        self.employees.remove(employee)

    def add_car(self, car: Car):
        self.cars.append(car)

    def remove_car(self, car: Car):
        self.cars.remove(car)

    def record_sale(self, sale: Sale):
        self.sales.append(sale)

    def delete_sale(self, sale: Sale):
        self.sales.remove(sale)

    def get_employee_report(self):
        return "\n".join([str(emp) for emp in self.employees])

    def get_car_report(self):
        return "\n".join([str(car) for car in self.cars])

    def get_sales_report(self):
        return "\n".join([str(sale) for sale in self.sales])

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump({
                "employees": [vars(emp) for emp in self.employees],
                "cars": [vars(car) for car in self.cars],
                "sales": [self._serialize_sale(sale) for sale in self.sales]
            }, file, indent=4)

    def _serialize_sale(self, sale):
        return {
            "employee": vars(sale.employee),
            "car": vars(sale.car),
            "sale_date": sale.sale_date,
            "actual_price": sale.actual_price
        }

    def load_from_file(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.employees = [Employee(**emp) for emp in data['employees']]
                self.cars = [Car(**car) for car in data['cars']]
                self.sales = [Sale(Employee(**sale['employee']), Car(**sale['car']), sale['sale_date'], sale['actual_price']) for sale in data['sales']]
            print("Дані успішно завантажені з файлу.")
        except FileNotFoundError:
            print("Помилка! Такий файл не існує.")
        except json.JSONDecodeError:
            print("Помилка! Невірний формат файлу.")

def input_name(prompt: str) -> str:
    while True:
        name = input(prompt).strip()
        if re.match("^[А-Яа-яІіЄєЇїҐґ]+$", name):
            return name
        else:
            print("Помилка! ПІБ повинно містити тільки літери.")

def input_position(prompt: str) -> str:
    while True:
        position = input(prompt).strip()
        if re.match("^[А-Яа-яІіЄєЇїҐґ]+$", position):
            return position
        else:
            print("Помилка! Посада повинна містити тільки літери.")

def input_phone(prompt: str) -> str:
    while True:
        phone = input(prompt).strip()
        if phone.isdigit() and len(phone) == 10:
            return phone
        else:
            print("Помилка! Телефон повинен містити 10 цифр.")

def input_year(prompt: str) -> int:
    while True:
        year = input(prompt).strip()
        if year.isdigit() and len(year) == 4:
            return int(year)
        else:
            print("Помилка! Рік повинен бути числом з 4 цифр.")

def input_price(prompt: str) -> float:
    while True:
        price = input(prompt).strip()
        if price.isdigit():
            return float(price)
        else:
            print("Помилка! Ціна повинна бути числом.")

def input_date(prompt: str) -> str:
    while True:
        date_input = input(prompt).strip()
        try:
            day, month, year = map(int, date_input.split("-"))
            return f"{year}-{month:02d}-{day:02d}"
        except ValueError:
            print("Помилка! Введіть дату у форматі дд-мм-рррр.")

def main_menu():
    dealership = Dealership()

    while True:
        print("\n1. Додати співробітника")
        print("2. Видалити співробітника")
        print("3. Додати автомобіль")
        print("4. Видалити автомобіль")
        print("5. Записати продаж")
        print("6. Видалити продаж")
        print("7. Звіт про співробітників")
        print("8. Звіт про автомобілі")
        print("9. Звіт про продажі")
        print("10. Зберегти дані в файл")
        print("11. Завантажити дані з файлу")
        print("0. Вихід")

        choice = input("Виберіть опцію: ")

        if choice == '1':
            name = input_name("Введіть ПІБ співробітника: ")
            position = input_position("Введіть посаду: ")
            phone = input_phone("Введіть номер телефону: ")
            email = input("Введіть email: ").strip()
            employee = Employee(name, position, phone, email)
            dealership.add_employee(employee)
            print(f"Співробітник {name} доданий.")

        elif choice == '2':
            name = input_name("Введіть ПІБ співробітника для видалення: ")
            employee = next((emp for emp in dealership.employees if emp.name == name), None)
            if employee:
                dealership.remove_employee(employee)
                print(f"Співробітник {name} видалений.")
            else:
                print(f"Співробітник з ПІБ {name} не знайдений.")

        elif choice == '3':
            manufacturer = input("Введіть виробника: ").strip()
            year = input_year("Введіть рік випуску автомобіля: ")
            model = input("Введіть модель: ").strip()
            cost_price = input_price("Введіть собівартість: ")
            selling_price = input_price("Введіть ціну продажу: ")
            car = Car(manufacturer, year, model, cost_price, selling_price)
            dealership.add_car(car)
            print(f"Автомобіль {manufacturer} {model} доданий.")

        elif choice == '4':
            manufacturer = input("Введіть виробника для видалення автомобіля: ").strip()
            year = input_year("Введіть рік випуску: ")
            model = input("Введіть модель: ").strip()
            car = next((car for car in dealership.cars if car.manufacturer == manufacturer and car.year == year and car.model == model), None)
            if car:
                dealership.remove_car(car)
                print(f"Автомобіль {manufacturer} {model} видалений.")
            else:
                print("Автомобіль не знайдений.")

        elif choice == '5':
            name = input_name("Введіть ПІБ співробітника, який здійснив продаж: ")
            employee = next((emp for emp in dealership.employees if emp.name == name), None)
            if not employee:
                print(f"Співробітник з ПІБ {name} не знайдений.")
                continue

            manufacturer = input("Введіть виробника автомобіля: ").strip()
            car = next((car for car in dealership.cars if car.manufacturer == manufacturer), None)
            if not car:
                print(f"Автомобіль {manufacturer} не знайдений.")
                continue

            sale_date = input_date("Введіть дату продажу (дд-мм-рррр): ")
            actual_price = input_price("Введіть реальну ціну продажу: ")

            sale = Sale(employee, car, sale_date, actual_price)
            dealership.record_sale(sale)
            print(f"Продаж автомобіля {car.model} здійснено співробітником {employee.name}.")

        elif choice == '6':
            name = input_name("Введіть ПІБ співробітника для видалення продажу: ")
            sale = next((sale for sale in dealership.sales if sale.employee.name == name), None)
            if sale:
                dealership.delete_sale(sale)
                print("Продаж видалено.")
            else:
                print("Продаж не знайдений.")

        elif choice == '7':
            print("Звіт про співробітників:")
            print(dealership.get_employee_report())

        elif choice == '8':
            print("Звіт про автомобілі:")
            print(dealership.get_car_report())

        elif choice == '9':
            print("Звіт про продажі:")
            print(dealership.get_sales_report())

        elif choice == '10':
            file_name = input("Введіть ім'я файлу для збереження: ").strip()
            dealership.save_to_file(file_name)

        elif choice == '11':
            file_name = input("Введіть ім'я файлу для завантаження: ").strip()
            dealership.load_from_file(file_name)

        elif choice == '0':
            break
        else:
            print("Невірна опція, спробуйте ще раз.")

if __name__ == '__main__':
    main_menu()
