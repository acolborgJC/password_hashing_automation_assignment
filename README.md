# Password Hashing Automation Assignment

### Assignment for JumpCloud

## Purpose

This tests the hashing and encoding application 
given to me by JumpCloud. There are 4 endpoints that
I could test encompassing two POST and two GET requests.


## Language, IDE and platfroms

This was developed on Python 3.6.5

PyCharm 2018.1 was used to develop the autmation suite

Automation was tested on macOS High Sierra

It was also tested on Windows 10

## How to run the tests

You can run the tests a few different ways

#### All tests

Try to run all tests in the root folder by running:

* pytest automation_tests/

#### Run a particular method signature test 

Most Basic Test (Happy Path)

* pytest automation_tests/ -k test_post_single_
password_hash_call_with_long_wait

More Complex Tests

* pytest automation_tests/ -k concurrent_password_hash_calls

* pytest automation_tests/ -k parameterized_password_hash_calls

## Test Cases

Test Cases live under the test_cases folder

I detailed test cases I ran manually before developing the automation

I briefly listed out failures I encountered

As of 4/26/18 there are 16 test cases that are automated

## Todos

* Further refactoring
* Further code cleanup
* Possible use of Python classes
* Adding export for junit_xml output that could be 
read by Jenkins or another XML parsing program


