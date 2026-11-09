import io
import logging
import unittest

import test_pipeline

suite = unittest.defaultTestLoader.loadTestsFromModule(test_pipeline)
runner = unittest.TextTestRunner(stream=io.StringIO())
logging.disable(logging.CRITICAL)
try:
    result = runner.run(suite)
finally:
    logging.disable(logging.NOTSET)
print("Success:", result.wasSuccessful())
print("Tests run:", result.testsRun)
print("Failures:", len(result.failures), "Errors:", len(result.errors))
