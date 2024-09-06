import os
from loguru import logger

class Env:
    file_dir = '.env'

    @classmethod
    def create(cls) -> bool:
        if not os.path.exists(cls.file_dir):
            logger.error('.env file did not found!')
            return False
            
        with open(cls.file_dir, mode='r') as file:
            list_data = file.readlines()
            
        if len(list_data) == 0:
            logger.debug('No data in .env file.')
            return True
            
        json_data = {
            value.split('=')[0].strip() : value.split('=')[1].strip().replace('\n', '')
            for value in list_data if '=' in value
        }
        
        for key in json_data.keys():
            value = json_data[key]
            os.environ[key] = value
            
        logger.debug('Environment created.')
        return True
