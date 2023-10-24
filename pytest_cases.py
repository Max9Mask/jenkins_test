import pymssql
import pytest


# Connection to DB
@pytest.fixture(scope="module")
def db_connection():
    server = 'host.docker.internal:1433'
    user = 'test_login'
    password = '123456abcdefABC'
    db_name = 'AdventureWorks2012'
    with pymssql.connect(server, user, password, db_name) as conn:
        yield conn



# Test Cases
def test_table_exists(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT OBJECT_ID(N'Person.Address')")
        result = cursor.fetchall()
    assert result[0][0] is not None


def test_address_count(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM Person.Address")
        result = cursor.fetchall()
    assert result[0][0] == 19615


def test_address_sum(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT SUM(StateprovinceID) FROM Person.Address")
        result = cursor.fetchall()
    assert result[0][0] == 966669


def test_document_exists(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT OBJECT_ID(N'Production.Document')")
        result = cursor.fetchall()
    assert result[0][0] is not None


def test_document_avg(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT AVG(ChangeNumber) FROM Production.Document")
        result = cursor.fetchall()
    assert result[0][0] == 35


def test_document_range(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Production.Document WHERE Status NOT IN (1, 2, 3)")
        result = cursor.fetchall()
    assert result[0][0] == 0


def test_measure_exists(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT OBJECT_ID(N'Production.UnitMeasure')")
        result = cursor.fetchall()
    assert result[0][0] is not None


def test_measure_length(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Production.UnitMeasure WHERE LEN(UnitMeasureCode) NOT BETWEEN 1 AND 3")
        result = cursor.fetchall()
    assert result[0][0] == 0


def test_measure_min_max(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT MIN(Name), MAX(Name) FROM Production.UnitMeasure")
        result = cursor.fetchall()
    assert result[0] == ('Bottle', 'US pound')


# Commands for terminal to generate report:
#  pytest --alluredir=allure-report pytest_cases.py
#  allure serve allure-report
#  allure generate allure-report --clean
