from madjin.celery import app
from works.file_tests import test_value_function, test_type_function
from works.models import Test, TestResult
import urllib.request

@app.task()
def start_tests(report):
    tests = report.task.tests.all()
    file_request = urllib.request.urlopen(report.file.url)
    for test in tests:
        if test.test_type == Test.VALUE_EQUALS:
            status = test_value_function(file_request, test.function_name, test.value)
        else:
            status = test_type_function(file_request, test.function_name, test.value)
        TestResult.objects.create(test=test, report=report, passed=status)
    report.passed = not report.tests_result.filter(passed=False).exists()
    report.save()
