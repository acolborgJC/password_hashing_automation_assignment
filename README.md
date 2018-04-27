# Password Hashing Automation Assignment

### Assignment for JumpCloud

## Purpose

This tests the hashing and encoding application 
given to me by JumpCloud. There are 4 endpoints that
I could test encompassing two POST and two GET requests.


## Language, IDE and platforms used

This was developed using Python 3.6.5

Highligted modules that were used:

* pytest
* requests 
* hashlib
* codecs

PyCharm 2018.1 was used to develop the automation suite

Automation was tested and proved on macOS High Sierra

Automated was tested on Windows 2010 but still attempting to diagnose
module issues

## What was chosen to test

I chose to test all endpoints with the most concentration on the first
POST endpoint (to create an encoded SHA-512 password ). The focus was testing
using pytest parameterized tests with variations 
on password key and password value. Additionally, concurrent and 
sequential tests we added to test performance.

On the GET side to retrieve the base64 encoded hash I had two tests to validate
the encoding returned for a password and a negative test to check what would be
returned with an invalid integer request.

A shutdown request scenario was added while concurrent requests were attempted
against the application. 

Finally, the stats endpoint was tested with no data and after the post hash 
endpoint was called once.

All tests should have assert statements in the test itself or in the helper
methods

## How to run the tests

You can run the tests a few different ways

#### Run a particular method signature test 

This should be a good start to validate a smaller piece of the automation

Most Basic Test (Happy Path waiting on identifier)

* pytest automation_tests/ -k test_post_single_
password_hash_call_with_long_wait

Most Basic Test (Waiting less than a second)

* pytest automation_tests/ -k test_post_single_
password_hash_call_with_immediate_job_identifier

More Complex Tests

* pytest automation_tests/ -k concurrent_password_hash_calls

* pytest automation_tests/ -k parameterized_password_hash_calls

#### All tests

Try to run all tests in the root folder by running:

* pytest automation_tests/

## Test Cases

Test Cases live under the test_cases folder

I detailed test cases I ran manually before developing the automation

I briefly listed out failures I encountered

As of 4/26/18 there are 16 test cases that are automated

## Latest Test Results

5 failed, 9 passed, 2 skipped in 85.74 seconds 

## Todos

* Further refactoring
* Further code cleanup
* Possible use of Python classes
* Adding export for junit_xml output that could be 
read by Jenkins or another XML parsing program


