Playwright Test Automation Framework
This repository provides a generic and scalable test automation framework built using Playwright with Python. Designed with the Page Object Model (POM) design pattern, this framework ensures modularity, readability, and maintainability. It supports cross-browser testing, robust logging, and a layered architecture for efficient automation testing.

Features
Playwright Integration: Leverages Async Playwright for modern, fast, and reliable browser automation.
Page Object Model (POM): Encapsulates page-specific logic in reusable page classes.
Layered Architecture: Separates concerns across base classes, handlers, and utilities for scalability.
Custom Handlers: Utilities for common UI element interactions like buttons, menus, and text inputs.
Cross-Browser Compatibility: Supports Chromium, Firefox, and WebKit browsers.
Robust Logging: Centralized logging for better debugging and test insights.
Asynchronous Support: Handles asynchronous browser interactions seamlessly.

Setup Instructions
Prerequisites
Install Python 3.8+.
Install Playwright:
bash
Copy code
pip install playwright pytest-playwright
playwright install
Install additional Python packages:
bash
Copy code
pip install -r requirements.txt
Usage
1. Running Tests
Navigate to the tests/ directory and execute test cases:

bash
Copy code
pytest --browser=chromium -v
For cross-browser testing:

bash
Copy code
pytest --browser=all -v
2. Framework Overview
BasePage: Provides reusable methods for navigation, element interactions, and waits.
Page-Specific Classes: Encapsulate business logic for individual web pages.
Handlers: Specialized modules for interacting with UI components such as text boxes, buttons, and menus.
Core Components
1. Base Classes
BasePage: A foundational class for all page objects, containing common web interactions:
go_to(url): Navigates to a given URL.
click(selector): Clicks an element by its selector.
fill(selector, text): Inputs text into a field.
wait_for_element(selector): Waits for an element to appear.
2. Handlers
Reusable utility modules for interacting with UI components:

ButtonHandler: Click and validate button interactions.
MenuHandler: Fetch and interact with menu items dynamically.
TextboxHandler: Automate textbox operations like entering or clearing text.
3. Page-Specific Classes
Encapsulate page logic for reuse:

SamplePage (Example): Includes methods for interacting with a generic sample page.
Cross-Browser Support
Playwright supports multiple browsers out-of-the-box:

Chromium
Firefox
WebKit
You can run tests across all supported browsers or target a specific browser using the --browser flag.

Logging
Logs are managed using the logger utility:

Info Logs: Record successful interactions and navigations.
Error Logs: Capture and report issues during test execution.
Report Generation
HTML Reports:
Run tests with:
bash
Copy code
pytest --html=reports/report.html --self-contained-html
Allure Reports:
Generate results with:
bash
Copy code
pytest --alluredir=reports/allure-results
Serve Allure reports:
bash
Copy code
allure serve reports/allure-results
Extending the Framework
Add New Pages: Create a new class in the pages/ folder and extend the BasePage.
Add Custom Handlers: Implement reusable UI interaction logic in the handlers/ folder.
Add Test Cases: Write new tests in the tests/ folder and follow naming conventions.
Contributing
We welcome contributions to enhance the framework. Fork the repository, create a feature branch, and submit a pull request.

License
This project is licensed under the MIT License.

Author
Developed by [Your Name]. For questions, reach out at ehudsuryano@gmail.com.
