import psycopg2
import logging
from psycopg2.sql import SQL, Identifier
from time import gmtime, localtime, strftime
from typing import Dict, List, Optional, Any

from config_db import config_database


root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('tik_tok.log', 'w', 'utf-8')
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
root_logger.addHandler(handler)


def create_new_user(user_data: Dict[str, str]) -> bool:
    conn = None
    try:
        params = config_database()
        
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        if user_data['role'] == "user":
            create_user_sql = "insert into users ( tik_tok_name,\
                                                   tik_tok_id,\
                                                   role,\
                                                   login,\
                                                   password,\
                                                   status,\
                                                   chat_id) values (%s, %s, %s, %s, %s, %s, %s);"

            cur.execute(create_user_sql, ( user_data['tik_tok_name'], 
                                           user_data['tik_tok_id'], 
                                           user_data['role'], 
                                           user_data['login'], 
                                           user_data['password'], 
                                           user_data['status'], 
                                           user_data['chat_id']))
            
            cur.close()
            
            conn.commit()
            
            current_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
            logging.info(f"{current_time}---NEW USER | {user_data['tik_tok_name']} | created successfully")

            return True
        
        elif user_data['role'] == "admin":
            
            update_user_sql = SQL("update users set {} = %s,\
                                                    {} = %s,\
                                                    {} = %s,\
                                                    {} = %s where login = %s;").format(Identifier("tik_tok_name"),
                                                                                    Identifier("tik_tok_id"), 
                                                                                    Identifier("status"), 
                                                                                    Identifier("chat_id"))

            cur.execute(update_user_sql, ( user_data['tik_tok_name'], 
                                           user_data['tik_tok_id'],  
                                           user_data['status'], 
                                           user_data['chat_id'],
                                           user_data['login']))
            
            cur.close()
            
            conn.commit()
            
            current_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
            logging.info(f"{current_time}---ADMIN LOGGED IN | {user_data['tik_tok_name']} | logged in successfully")

            return True

    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception("Exception occurred")
        return False
    finally:
        if conn is not None:
            conn.close()


def check_users_login_password_role(user_data: Dict[str, str]) -> bool:
    conn = None
    try:
        params = config_database()
        
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        check_user_login_password_role_sql = "select users.login,\
                                              users.password,\
                                              users.role from users where users.login=%s limit 1;"

        cur.execute(check_user_login_password_role_sql, ( 
            user_data['login'],
        ))

        is_exist = cur.fetchone()

        cur.close()
        
        conn.commit()

        if not is_exist:
            return False

        if is_exist[1] == user_data['password']:
            if is_exist[2] == user_data['role']:
                return True
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception("Exception occurred")
        return False
    finally:
        if conn is not None:
            conn.close()