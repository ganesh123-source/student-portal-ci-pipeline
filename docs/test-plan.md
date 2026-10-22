## Student Portal – Test Plan

Goal: Automatically test the Student Portal on every code push.
Features to test: Registration, Login, Logout, Dashboard.
Types of testing: UI tests, API tests, data-driven tests.
Tools: Playwright or Selenium, Postman or REST Assured, Allure, GitHub Actions, Supabase.
Test data: Separate test accounts only, never real data.
Pass rule: The pipeline is green only if every test passes.

 ID	          Test case	                 Expected result
TC01	Register with valid details	    Account created, goes to dashboard
TC02	Register with an existing email	Error message shown
TC03	Register with an empty name	    Validation error
TC04	Register with a weak password	Validation error
TC05	Login with correct details	    Dashboard opens
TC06	Login with wrong password	    Error message, stays on login
TC07	Login with empty fields	        Validation error
TC08	Logout	                        Goes back to login page

