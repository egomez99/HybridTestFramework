# Hybrid (Selenium WEB UI/APIs/Mobile) Test Framework 

## PAP (Python Automation Project)

Project folder structure
```
lalo$ tree
Test Framework
|____apis
| |____step_defs
| | |____backend
| | | |____chucknorris_jokes_categories_test.py
| | | |____chucknorris_basic_random_joke_test.py
| |____features
| | |____backend
| | | |____chucknorris_basic_random_joke.feature
| | | |____chucknorris_jokes_categories.feature
|____web
| |____step_defs
| | |____frontend
| | | |____conftest.py
| | | |____searchgoogle_test.py
| | | |____duck_test.py
| |____features
| | |____frontend
| | | |____searchgoogle.feature
| | | |____duck.feature
|____mobile
| |____step_defs
| | |____payments
| | | |____conftest.py
| | | |____payments_test.py
| |____features
| | |____payments
| | | |____payments.feature
```


### Framework to perform automation testing for regression on different environments.

How to start the project?

Invoke pytest commands to run the tests: 

## Running all tests 
```
>$ python3 -m pytest
============================================= test session starts =============================================
platform darwin -- Python 3.8.2, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
rootdir: /Users/lalo/Downloads/PABLOGOMEZROMO/PycharmProjects/TestFramework, configfile: pytest.ini
plugins: xdist-2.5.0, forked-1.4.0, bdd-4.0.2, html-3.1.1, metadata-1.11.0
collecting ... 
--------------------------------------------- live log collection ---------------------------------------------
2022-02-11 13:49:31 INFO 

2022-02-11 13:49:31 INFO ====== WebDriver manager ======
2022-02-11 13:49:31 INFO Current google-chrome version is 98.0.4758
2022-02-11 13:49:31 INFO Get LATEST chromedriver version for 98.0.4758 google-chrome
2022-02-11 13:49:31 INFO Driver [/Users/lalo/.wdm/drivers/chromedriver/mac64/98.0.4758.80/chromedriver] found in cache
collecting 3 items                                                                                            2022-02-11 13:49:35 INFO 

2022-02-11 13:49:35 INFO ====== WebDriver manager ======
2022-02-11 13:49:35 INFO Current google-chrome version is 98.0.4758
2022-02-11 13:49:35 INFO Get LATEST chromedriver version for 98.0.4758 google-chrome
2022-02-11 13:49:35 INFO Driver [/Users/lalo/.wdm/drivers/chromedriver/mac64/98.0.4758.80/chromedriver] found in cache
collected 4 items                                                                                             

tests/apis/step_defs/backend/chucknorris_basic_random_joke_test.py::test_chuck_norris_basic_random_joke PASSED [ 25%]
tests/apis/step_defs/backend/chucknorris_jokes_categories_test.py::test_chuck_norris_jokes_categories PASSED [ 50%]
tests/web/step_defs/frontend/duck_test.py::test_basic_duckduckgo_search PASSED                          [ 75%]
tests/web/step_defs/frontend/searchgoogle_test.py::test_verify_user_search_in_google PASSED             [100%]

============================================== warnings summary ===============================================
../../../../Library/Python/3.8/lib/python/site-packages/pytest_bdd/plugin.py:85
  /Users/lalo/Library/Python/3.8/lib/python/site-packages/pytest_bdd/plugin.py:85: PytestUnknownMarkWarning: Unknown pytest.mark.search - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/mark.html
    mark = getattr(pytest.mark, tag)

-- Docs: https://docs.pytest.org/en/stable/warnings.html
======================================= 4 passed, 5 warnings in 19.02s ========================================
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
