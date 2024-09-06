import unittest
from loguru import logger

from modules.env import Env
from modules.users import Users

class Tests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_info = {
            'user_id': 23456712,
            'user_fullname': 'Test User',
            'referral_link': 'https://t.me/bot?start=23456712'
        }
        
    def setUp(self):
        pass
        
    def test_1(self):
        create_environment_response = Env.create()
        self.assertTrue(create_environment_response)
        
    async def test_2(self):
        with Users() as module:
            save_new_user_response = await module.save_new_user(
                cls.user_info.get('user_id'),
                cls.user_info.get('user_fullname'),
                cls.user_info.get('referral_link'),
            )
            
            logger.debug(save_new_user_response)
            
            status = save_new_user_response['status']
            self.assertTrue(status)
        
    async def test_3(self):
        with Users() as module:
            select_user_info_response = await module.select_user_info(
                cls.user_info.get('user_id')
            )
            
            logger.debug(select_user_info_response)
            
            status = select_user_info_response['status']
            self.assertTrue(status)
        
    async def test_4(self):
        with Users() as module:
            add_bonuse_response = await module.add_bonuse(
                cls.user_info.get('user_id'),
                10
            )
            
            logger.debug(add_bonuse_response)
            
            status = add_bonuse_response['status']
            self.assertTrue(status)
        
    async def test_5(self):
        with Users() as module:
            delete_user_response = await module.delete_user(
                cls.user_info.get('user_id')
            )
            
            logger.debug(delete_user_response)
            
            status = delete_user_response['status']
            self.assertTrue(status)
        
    def tearDown(self):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass
        
if __name__ == '__main__':
    unittest.main()
