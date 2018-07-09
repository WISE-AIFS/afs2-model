
import boto
import boto.s3.connection
from boto.s3.key import Key
import pandas as pd
from pandas.io.json import json_normalize
import numpy
import os
import json
import datetime
import time
import random
import requests
import base64
from influxdb import DataFrameClient

class GetJointTable(object):

    def __call__(self, query_date, grafana_dict, idb_dict, tag):

        """
test
        """
    
        GRAFANA_HOST = grafana_dict['GRAFANA_HOST']
        GRAFANA_REQUEST_ANNO_QUERY = '/api/annotations'
        GRAFANA_USERNAME = grafana_dict['GRAFANA_USERNAME']
        GRAFANA_PASSWORD = grafana_dict['GRAFANA_PASSWORD']
        GRAFANA_FROM = query_date['DATE_FROM'] + '000'
        GRAFANA_TO =   query_date['DATE_TO'] + '000'
        GRAFANA_TAG1 = grafana_dict['GRAFANA_TAG1']
        GRAFANA_TAG2 = grafana_dict['GRAFANA_TAG2']
        #GRAFANA_PANEL_ID = '16'
        #GRAFANA_DASHBOARD_ID = '15'

        IDB_HOST = idb_dict['IDB_HOST']
        IDB_PORT = idb_dict['IDB_PORT']
        IDB_DBNAME = idb_dict['IDB_DBNAME']
        IDB_CHANNEL = tag
        IDB_USER = idb_dict['IDB_USER']
        IDB_PASSWORD = idb_dict['IDB_PASSWORD']
        KEYWORD = ''

        
        def read_influxdb_data(host='192.168.123.245', 
                       port=8086, 
                       dbname = 'c9377a95-82f3-4af3-ac14-40d14f6d2abe', 
                       ChannelName='1Y520210100', 
                       time_start='', 
                       time_end='', 
                       user = 'c6e23c03-dd57-4c8f-a6e2-b683ad76e8e4', 
                       password = 'NSr8dUZ6meiRlal8zqGcV6avK',
                       keyword=''):

            client = DataFrameClient(host, port, user, password, dbname)
            measurements = client.get_list_measurements()
    
            if keyword is None: keyword = ''
        
            if keyword=='':
                measurement = [mea.get(u'name') for mea in measurements if mea.get(u'name').find(ChannelName)>=0]
            else:
                measurement = [mea.get(u'name') for mea in measurements if mea.get(u'name').find(ChannelName)>=0 and mea.get(u'name').find(keyword)>=0]
    
            if len(measurement)==0: 
                print('No data retrieved.')
                return None
    
            measurement = measurement[-1]
            time_end = 'now()' if time_end=='' else "'" + time_end + "'"    
            time_start = 'now()' if time_start=='' else "'" + time_start + "'"
            querystr = 'select * from "{}" where time > {} and time < {}'.format(measurement,time_start,time_end)
            #print(querystr)
    
            df = client.query(querystr).get(measurement)
            client.close()
    
            if df is None: 
                print('InfluxDB no data retrieved.')
                return None    
    
            dff = df.groupby('id')
            columns = [name for name, group in dff]
            groups = [group['val'] for name, group in dff]
    
            #check datatime alginment: all([all(groups[i].index==groups[0].index) for i in range(1,len(groups))])
            result = pd.concat(groups,axis=1)
            result.columns = columns
            result.index = groups[0].index

            return measurement, result
        

        def encode_base64(username, password):
            str_user = username + ':' + password    
            str_user_byte = str_user.encode('utf8')  # string to byte
            str_user_encode64 = base64.b64encode(str_user_byte)    # encode by base64
            str_user_string = str_user_encode64.decode('utf8')    # byte to string
            str_auth = 'Basic ' + str(str_user_string)
            return str_auth

        ## Request Annotation list from Grafana ##
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": encode_base64(GRAFANA_USERNAME, GRAFANA_PASSWORD)}

        url = GRAFANA_HOST + GRAFANA_REQUEST_ANNO_QUERY + '?' +\
                                                          '&tags=' + GRAFANA_TAG1 +\
                                                          '&tags=' + GRAFANA_TAG2 +\
                                                          '&from=' + GRAFANA_FROM +\
                                                          '&to=' + GRAFANA_TO
        
        print(url)
        print(headers)

        req = requests.get(url, headers=headers)
        req_data_json = req.json()
        req_data_pd = json_normalize(req_data_json)
        
        #print (req_data_pd)
        
        # which means grafana retrieve no data from API
        #if 'timestamp' not in req_data_pd.index:
        #    return 'no data retrieve from Grafana'
        
        #GMT+8
        annotation = req_data_pd[['regionId', 'tags', 'time']]
        annotation = annotation.sort_values(by=['regionId', 'time'])
        annotation['time'] = pd.to_datetime(annotation['time'], unit='ms')
        annotation.rename(index=str, columns={'time': 'timestamp'}, inplace=True)
        
        
        ## Request SCADA eigen value from InfluxDB ##
        #scada_idb = pd.read_csv('test.csv')
        #scada_idb['Unnamed: 0'] = scada_idb['Unnamed: 0'].astype(str).str[:-6]
        #scada_idb.rename(index=str, columns={'Unnamed: 0': 'timestamp'}, inplace=True)
        #cada_idb = scada_idb.sort_values(by=['timestamp'])
        
        IDB_TIME_START = datetime.datetime.fromtimestamp(int(query_date['DATE_FROM'])).strftime('%Y-%m-%d %H:%M:%S')
        IDB_TIME_END = datetime.datetime.fromtimestamp(int(query_date['DATE_TO'])).strftime('%Y-%m-%d %H:%M:%S')
        
        measurement, scada_idb = read_influxdb_data(host = IDB_HOST,
                                       port = IDB_PORT,
                                       dbname = IDB_DBNAME,
                                       ChannelName = IDB_CHANNEL,
                                       time_start = IDB_TIME_START,
                                       time_end = IDB_TIME_END,
                                       user = IDB_USER,
                                       password = IDB_PASSWORD
                                      )
        scada_idb['timestamp'] = scada_idb.index
        scada_idb['timestamp'] = scada_idb['timestamp'].astype(str).str[:-6]

        
        # which means SCADA retrieve no data from InfluxDB
        if len(scada_idb['timestamp']) == 0:
            return 'no data retrieve from SCADA'

        ## Align SCADA and Grafana Dataframe ##
        label_df = pd.DataFrame()
        for regionID in annotation.regionId.unique():

            tags_list = annotation[annotation['regionId'] == regionID]['tags'].iloc[0]
            label_start_time = str(annotation[annotation['regionId'] == regionID]['timestamp'].iloc[0])
            label_end_time = str(annotation[annotation['regionId'] == regionID]['timestamp'].iloc[1])
            label_start_time = datetime.datetime.strptime(label_start_time, '%Y-%m-%d %H:%M:%S')
            label_end_time = datetime.datetime.strptime(label_end_time, '%Y-%m-%d %H:%M:%S')

            # loop scada_idb, if timestamp + 8 hours + 6 days(testing) > start and < end, set value of tags
            for i in range(len(scada_idb['timestamp'])):
                datetime_object = datetime.datetime.strptime(scada_idb['timestamp'][i], '%Y-%m-%d %H:%M:%S')
                #datetime_object = datetime_object + datetime.timedelta(hours=8) + datetime.timedelta(days=7)
                #label_df.at[i, tags]= 0
                label_df.at[i, 'timestamp'] = scada_idb['timestamp'][i]

                if (datetime_object > label_start_time) and (datetime_object < label_end_time):
                    for tags in tags_list:
                        #print (tags)
                        label_df.at[i, tags] = 1
                else:
                    for tags in tags_list:
                        #print (tags)
                        label_df.at[i, tags] = -1

            #print (label_start_time, label_end_time, datetime_object)
            
        #label_df.drop('x', axis=1, inplace=True)
        output_df = pd.merge(scada_idb, label_df.fillna(-1), on=['timestamp'])
        
        return output_df

get = GetJointTable()
