import unittest

import logging.config

class TestLogging(unittest.TestCase):
    def setUp(self):
        logging.config.fileConfig('test/config/logging.conf')

    def test_log_success(self):
        logger = logging.getLogger('crafts_success')

        self.assertIsNotNone(logger)

        logger.info('holy wow!')

    def test_log_fail(self):
        logger = logging.getLogger('crafts_fail')

        self.assertIsNotNone(logger)

        try:
            self.assertRaises(Exception, logger.info('gee wiz!'))
        except:
            pass

if __name__ == '__main__':
    unittest.main()
