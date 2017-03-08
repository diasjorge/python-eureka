import unittest
import os
import time
from eureka_client import EurekaClient


class TestEurekaClient(unittest.TestCase):

    def setUp(self):
        if not os.environ.get("EUREKA_URL"):
            raise unittest.case.SkipTest('Please Provide EUREKA_URL for tests')

        self.eureka_client = EurekaClient(
            "MyApplication",
            eureka_url=os.environ.get("EUREKA_URL"),
            use_dns=False,
            host_name="my-app.server",
            data_center="MyOwn",
            ip_address="127.0.0.1",
            vip_address="http://my-app.example.com/",
            port=80,
            secure_vip_address="https://my-app.example.com/",
            secure_port=443,
            home_page_url="http://my-app.example.com/home",
            status_page_url="http://my-app.example.com/status",
            health_check_url="http://my-app.example.com/healthCheck",
            app_group_name="appgroup",
            asg_name="asgname",
            metadata={
                "key": "value"
            }
        )

    def test_registration(self):
        self.eureka_client.register()

        self.assertEqual("MYAPPLICATION", self._get_app_info().get('name'))

    def test_instance_info(self):
        app_info = self._get_app_info()
        instance_info = app_info.get('instance')[0]

        self.assertEqual("my-app.server", instance_info.get('hostName'))
        self.assertEqual({"key": "value"}, instance_info.get('metadata'))
        self.assertEqual("asgname", instance_info.get('asgName'))
        self.assertEqual("APPGROUP", instance_info.get('appGroupName'))
        self.assertEqual("127.0.0.1", instance_info.get('ipAddr'))
        self.assertEqual(80, instance_info.get('port').get('$'))
        self.assertEqual(443, instance_info.get('securePort').get('$'))
        self.assertEqual("https://my-app.example.com/",
                         instance_info.get('secureVipAddress'))
        self.assertEqual("http://my-app.example.com/",
                         instance_info.get('vipAddress'))
        self.assertEqual("http://my-app.example.com/healthCheck",
                         instance_info.get('healthCheckUrl'))
        self.assertEqual("http://my-app.example.com/home",
                         instance_info.get('homePageUrl'))
        self.assertEqual("http://my-app.example.com/status",
                         instance_info.get('statusPageUrl'))

    def _get_app_info(self):
        for attempt in range(10):
            try:
                return self.eureka_client.get_app("MYAPPLICATION") \
                                         .get('application')
            except:
                print 'sleep'
                time.sleep(1)
        else:
            raise RuntimeError('Application info not found')


if __name__ == '__main__':
    unittest.main()
