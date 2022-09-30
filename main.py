import cx_Oracle
import config as cfg
from datetime import datetime
import meraki
import pandas as pd

def insert_wifi():
    API_KEY = ''###
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
    network_id = '###'
    response_count = dashboard.wireless.getNetworkWirelessClientCountHistory(
        network_id, apTag='Cafeteria', resolution = 300, timespan = 300
    )
    return pd.DataFrame(response_count)

dataframe = insert_wifi()
a = dataframe.iloc[:, 0]
b = dataframe.iloc[:, 1]
c = dataframe.iloc[:, 2]

a = a.to_string(index = False)
b = b.to_string(index = False)
c = c.to_string(index = False)

if (c == 'None'):
    c = int(c.replace('None', '0'))
pass

    # construct an insert statement that add a new row to the meraki_wifi table
sql = ('insert into wifi_meraki_ap(startTs, endTs, clientCount) '
        'values(:a,:b,:c)')

    
try:
        # establish a new connection
        with cx_Oracle.connect(cfg.username,
                            cfg.password,
                            cfg.dsn,
                            encoding=cfg.encoding) as connection:
            # create a cursor
            with connection.cursor() as cursor:
                # execute the insert statement
                cursor.execute(sql,[a, b, c])
                # commit work
                connection.commit()
except cx_Oracle.Error as error:
    print('Error occurred:')
    print(error)   

if __name__ == '__main__':
    insert_wifi()
