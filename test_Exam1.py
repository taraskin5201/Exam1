import pytest
from Exam1 import Employee, Car, Sale, Dealership

def test_employee():
    employee = Employee("Іван Іванов", "Менеджер", "1234567890", "ivan@example.com")
    assert employee.name == "Іван Іванов"
    assert employee.position == "Менеджер"
    assert employee.phone == "1234567890"
    assert employee.email == "ivan@example.com"

def test_car():
    car = Car("Toyota", 2020, "Camry", 20000, 25000)
    assert car.manufacturer == "Toyota"
    assert car.year == 2020
    assert car.model == "Camry"
    assert car.cost_price == 20000
    assert car.selling_price == 25000

def test_sale():
    employee = Employee("Іван Іванов", "Менеджер", "1234567890", "ivan@example.com")
    car = Car("Toyota", 2020, "Camry", 20000, 25000)
    sale = Sale(employee, car, "2024-01-01", 24000)
    assert sale.employee.name == "Іван Іванов"
    assert sale.car.model == "Camry"
    assert sale.sale_date == "2024-01-01"
    assert sale.actual_price == 24000

def test_dealership_add_remove_employee():
    dealership = Dealership()
    employee = Employee("Іван Іванов", "Менеджер", "1234567890", "ivan@example.com")
    dealership.add_employee(employee)
    assert len(dealership.employees) == 1
    dealership.remove_employee(employee)
    assert len(dealership.employees) == 0

def test_dealership_add_remove_car():
    dealership = Dealership()
    car = Car("Toyota", 2020, "Camry", 20000, 25000)
    dealership.add_car(car)
    assert len(dealership.cars) == 1
    dealership.remove_car(car)
    assert len(dealership.cars) == 0

def test_dealership_record_delete_sale():
    dealership = Dealership()
    employee = Employee("Іван Іванов", "Менеджер", "1234567890", "ivan@example.com")
    car = Car("Toyota", 2020, "Camry", 20000, 25000)
    dealership.add_employee(employee)
    dealership.add_car(car)
    sale = Sale(employee, car, "2024-01-01", 24000)
    dealership.record_sale(sale)
    assert len(dealership.sales) == 1
    dealership.delete_sale(sale)
    assert len(dealership.sales) == 0

def test_get_reports():
    dealership = Dealership()
    employee = Employee("Іван Іванов", "Менеджер", "1234567890", "ivan@example.com")
    car = Car("Toyota", 2020, "Camry", 20000, 25000)
    dealership.add_employee(employee)
    dealership.add_car(car)
    assert "Іван Іванов" in dealership.get_employee_report()
    assert "Toyota" in dealership.get_car_report()

def test_save_load_file(tmp_path):
    dealership = Dealership()
    employee = Employee("Іван Іванов", "Менеджер", "1234567890", "ivan@example.com")
    car = Car("Toyota", 2020, "Camry", 20000, 25000)
    dealership.add_employee(employee)
    dealership.add_car(car)
    sale = Sale(employee, car, "2024-01-01", 24000)
    dealership.record_sale(sale)

    file_path = tmp_path / "test_data.json"
    dealership.save_to_file(file_path)
    dealership_loaded = Dealership()
    dealership_loaded.load_from_file(file_path)

    assert len(dealership_loaded.employees) == 1
    assert len(dealership_loaded.cars) == 1
    assert len(dealership_loaded.sales) == 1
