import copy
import sqlalchemy
import os
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

from models.users import Users as model

class Users:
    st_response_json = {
        'status': 'error',
        'err_description': ''
    }
        
    def __enter__(self):
        self.session = Session(
            create_engine(
                os.environ.get('DB_CONNECT_LINK', 'mysql+mysqlconnector://root:@db:3306/db_test'),
                echo=False
            )
        )
        
        return self
        
    async def delete_user(self, user_id: int) -> dict:
        response_json = copy.deepcopy(self.st_response_json)
        
        try:
            stmt = select(model).where(model.user_id == user_id)
            for user in self.session.scalars(stmt):
                user.delete()
                self.session.commit()
                
                response_json['status'] = 'success'
                return response_json
            
            response_json['err_description'] = 'User did not found!'
        
        except Exception as e:
            response_json['err_description'] = str(e)
            self.session.rollback()
                        
        finally:
            return response_json
            
    async def select_user_info(self, user_id: int) -> dict:
        response_json = copy.deepcopy(self.st_response_json)
        
        try:
            stmt = select(model).where(model.user_id == user_id)
            for user in self.session.scalars(stmt):
                response_json['user'] = user
                response_json['status'] = 'success'
               
                return response_json
            
            response_json['err_description'] = 'User did not found!'
        
        except Exception as e:
            response_json['err_description'] = str(e)
            self.session.rollback()
                        
        finally:
            return response_json
            
    async def add_bonuse(self, user_id: int, bonuse: int) -> dict:
        response_json = copy.deepcopy(self.st_response_json)
        
        try:
            user_info = await self.select_user_info(user_id)
            if user_info['status'] == 'error':
                response_json['err_description'] = user_info['err_description']
                return response_json
                
            user = user_info['user']
            user.balance += bonuse
            
            stmt = update(model).where(model.user_id == user_id).values(balance = user.balance)
            self.session.execute(stmt)
            self.session.commit()
        
            response_json['status'] = 'success'
        
        except Exception as e:
            response_json['err_description'] = str(e)
            self.session.rollback()
                        
        finally:
            return response_json
        
    async def save_new_user(self, *args) -> dict:
        response_json = copy.deepcopy(self.st_response_json)
        
        try:
            if len(args) != 3:
                response_json['err_description'] = 'Not all parameters for continue process!'
                return response_json
                
            user_id, user_fullname, referral_link = args
            
            user = model(
                user_id=user_id,
                user_fullname=user_fullname,
                referral_link=referral_link
            )
            
            self.session.add(user)
            self.session.commit()
            
            response_json['status'] = 'success'
            
        except sqlalchemy.exc.IntegrityError as e:
            response_json['err_description'] = str(e)
            self.session.rollback()
            
            if 'duplicate entry' in str(e).lower():
                response_json['status'] = 'success'
        
        except Exception as e:
            response_json['err_description'] = str(e)
            self.session.rollback()
                        
        finally:
            return response_json
        
    def __exit__(self, *args):
        self.session.close()
        
        return self
