from DataAccess.BaseDataObject import BaseDataObject, DataException
from DataAccess.RDBDataObject import RDBDataObject
import pymysql
import DataAccess.DataAdaptor as data_adaptor


class UsersRDB(RDBDataObject):


    @classmethod
    def _get_table_info(cls):

        info = {
            "table_name": "e6156.users"
        }
        return info

    @classmethod
    def get_table_name(cls):
        t_info = cls._get_table_info()
        result = t_info['table_name']
        return result

    @classmethod
    def get_by_email(cls, email):

        sql = "select * from e6156.users where email=%s"
        res, data = data_adaptor.run_q(sql=sql, args=(email), fetch=True)
        if data is not None and len(data) > 0:
            result =  data[0]
        else:
            result = None

        return result


    @classmethod
    def create_user(cls, user_info):

        result = None

        try:
            sql, args = data_adaptor.create_insert(table_name="users", row=user_info)
            res, data = data_adaptor.run_q(sql, args)
            if res != 1:
                result = None
            else:
                result = user_info['id']
        except pymysql.err.IntegrityError as ie:
            if ie.args[0] == 1062:
                raise (DataException(DataException.duplicate_key))
            else:
                raise DataException()
        except Exception as e:
            raise DataException()

        return result

    @classmethod
    def delete_user(cls, email):

        sql = "delete from e6156.users where email=%s"
        res, data = data_adaptor.run_q(sql=sql, args=email, fetch=True)
        if res:
            res = "Successful delete"
        else:
            res = "Failed"

        return res

    @classmethod
    def update_user(cls, user_info, email):

        sql, arg = data_adaptor.create_update(table_name="users", new_values=user_info, template={'email': email})
        res, data = data_adaptor.run_q(sql=sql, args=arg, fetch=True)
        if res:
            res = "Successful update"
        else:
            res = "Failed"

        return res
