# ~/managers/operatorsSimaudit/hardwareTest.py
import unittest

from hardware import HardwareConfigurator


class HardwareConfiguratorTest(unittest.TestCase):

    def setUp(self):
        self.hc = HardwareConfigurator()

    def test_1_activate_cores(self):
        self.assertEqual(self.hc.activate_cores(),
                         "cores are activated")

if __name__ == '__main__':
    unittest.main()
