# ~/managers/operatorsSimaudit/hardwareTest.py
import unittest

from hardware import HardwareConfigurator as hc


class HardwareConfiguratorTest(unittest.TestCase):

    def setUp(self):
        #self.hc = HardwareConfigurator()
        pass

    #@unittest.skip("reason for skipping")
    def test_1_activate_cores(self):
        self.assertEqual( hc.activate_cores(),
                         "cores are activated")

if __name__ == '__main__':
    unittest.main()
