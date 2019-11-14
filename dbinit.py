
from app import DB 
from data.db_init.module import * 

DB().rbac_init()


if __name__ == "__main__":
    from configs.setting import RBAC_NAME
    from oslo.db.module import mysqlHanlder    
    engin = mysqlHanlder().get_engin(RBAC_NAME)
    Base.metadata.create_all(engin)