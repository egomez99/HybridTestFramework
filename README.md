# Hybrid (UI/APIs) Test Framework 

## PAP (Python Automation Project)

### Framework to perform automation testing for regression on different environments.

How to start the project?

Invoke pytest commands to run the tests: 

## Running all tests 
>lalo$ python3 -m pytest
```
===================================================== test session starts =====================================================
platform darwin -- Python 3.8.2, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /Users/lalo/Downloads/PABLOGOMEZROMO/PycharmProjects/TestFramework
plugins: bdd-4.0.2, html-3.1.1, metadata-1.11.0
collected 10 items                                                                                                            

tests/ui/login/step_definitions/test_login_steps.py EE                                                                  [ 20%]
tests/ui/page_builder/step_definitions/test_page_builder_steps.py EE                                                    [ 40%]
tests/server/chuck_norris/step_definitions/test_chuck_norris_basic_random_joke_steps.py ..                              [ 60%]
tests/server/chuck_norris/step_definitions/test_chuck_norris_jokes_categories_steps.py .
-- Docs: https://docs.pytest.org/en/stable/warnings.html
=========================================================== short test summary info ============================================================
ISSUE tests/ui/page_builder/step_definitions/test_page_builder_steps.py::test_verify_validations_on_all_the_mandatory_fields_for_leadspace_content_type
tests/ui/login/step_definitions/test_login_steps.py::Test_URL::test_open_url[chrome] - selenium.common.exceptions.SessionNotCreatedExce...
tests/ui/login/step_definitions/test_login_steps.py::Test_URL::test_open_url[firefox] - selenium.common.exceptions.WebDriverException: ...
tests/ui/page_builder/step_definitions/test_page_builder_steps.py::Test_URL::test_open_url[chrome] - selenium.common.exceptions.Session...
tests/ui/page_builder/step_definitions/test_page_builder_steps.py::Test_URL::test_open_url[firefox] - selenium.common.exceptions.WebDri...
============================================== 1 failed, 5 passed, 3 warnings, 4 errors in 20.42s ==============================================
```


## Running specific tests 
>lalo$ python3 -m pytest tests/ui/login/step_definitions/test_login_steps.py
```
===================================================== test session starts =====================================================
platform darwin -- Python 3.8.2, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /Users/lalo/Downloads/PABLOGOMEZROMO/PycharmProjects/TestFramework
plugins: bdd-4.0.2, html-3.1.1, metadata-1.11.0
collected 3 items                                                                                                             
tests/ui/login/step_definitions/test_login_steps.py EE.                                                                 [100%]

/Users/lalo/Library/Python/3.8/lib/python/site-packages/selenium/webdriver/common/service.py:81: WebDriverException
====================================================== warnings summary =======================================================
../../../../Library/Python/3.8/lib/python/site-packages/pytest_bdd/plugin.py:85
  /Users/lalo/Library/Python/3.8/lib/python/site-packages/pytest_bdd/plugin.py:85: PytestUnknownMarkWarning: Unknown pytest.mark.login - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/mark.html
    mark = getattr(pytest.mark, tag)

-- Docs: https://docs.pytest.org/en/stable/warnings.html
=================================================== short test summary info ===================================================
tests/ui/login/step_definitions/test_login_steps.py::Test_URL::test_open_url[chrome] - selenium.common.exceptions.Sess...
tests/ui/login/step_definitions/test_login_steps.py::Test_URL::test_open_url[firefox] - selenium.common.exceptions.Web...
=========================================== 1 passed, 1 warning, 2 errors in 7.94s ============================================
```

For more reference, check [Pytest Documentation](https://docs.pytest.org/en/6.2.x/).
