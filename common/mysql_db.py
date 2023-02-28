# coding=utf8
import pymysql.cursors

# ======== MySql base operating ===================
class mysqlDB:

    def __init__(self, kw):
        try:
            # Connect to the database
            self.connection = pymysql.connect(host=kw["host"],
                                              port=int(kw["port"]),
                                              user=kw["user"],
                                              password=kw["password"],
                                              db=kw["db"],
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # clear table data
    def clear(self, table_name):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

    # insert sql statement
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        # print(real_sql)

        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)

        self.connection.commit()

    # close database
    def close(self):
        self.connection.close()

    # init data
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':

    kw = {}
    db = mysqlDB(**kw)
    table_name = "trade_relation_config"
    data = {'id': 1, 'demand_id': 1, 'supply_id': 1, 'trade_value': 11, 'weight_id': 68}

    db.clear(table_name)
    db.insert(table_name, data)
    db.close()
