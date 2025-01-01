@echo off
echo Running tests in parallel...
pytest -n auto --alluredir=reports/allure_reports/

echo Generating and serving Allure report...
allure serve allure_reports/