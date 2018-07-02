# -*-coding:utf-8 -*-
#  for a+b demo 20180504 clone from chi
import datetime
import time
import json
import traceback
import requests
import os, sys
import pandas as pd



class flow:
    mode = None # mode for switch data and constrant
        # {parser, node}
    mode_type = {
        'parser': 'parser',
        'node': 'node'
    }   # mode type for setting mode value

    flow_id = None  # Node-RED flow id
    flow_list = None  # Node-RED all nodes in flow
    current_node_id = None  # Node-RED current node id
    current_node_obj = None  # Node-RED current node config
    host_url = None  # host url for Node-RED

    sso_host_url = None # host url for sso
    afs_host_url = None # host url for afs
    afs_instance_id = None  # afs instance id

    # message
    ERR_MSG_NEXT_LIST_TYPE = '' # list of next node data type is error.
    ERR_MSG_NUMBER_OF_FIREHOSE = '' # number of firehose is error. (spec: 1 firehose in 1 flow)
    ERR_MSG_CONFIG_PARAM_NOT_FOUND = '' # config param is not found. (flow_id, node_id, host_url)



    def __init__(self, mode='node'):
        """
        Initialize.
        """
        # set initial value
        self.mode = mode;   # mode for switch data and constrant

        self.flow_id = None  # Node-RED flow id
        self.flow_list = None    # Node-RED all nodes in flow
        self.current_node_id = None  # Node-RED current node id
        self.current_node_obj = None # Node-RED current node config
        self.host_url = None # host url for Node-RED

        self.sso_host_url = 'https://portal-sso.iii-arfa.com'   # host url for sso
        self.afs_host_url = 'https://portal-afs-develop.iii-arfa.com'   # host url for afs
        self.afs_instance_id = 'cf127500-3520-4d3b-8676-4129258b1d41'   # afs instance id


        # set message
        self.ERR_MSG_NEXT_LIST_TYPE = 'List of next node data type is error.'
        self.ERR_MSG_NUMBER_OF_FIREHOSE = 'Number of firehose is error.'
        self.ERR_MSG_CONFIG_PARAM_NOT_FOUND = 'Need param is not found.'



    def set_flow_config(self, obj):
        """
        Set config(class properties value) of flow.

        :param  obj: (dict) request headers.
                    {flow_id, node_id, host_url}

        :return is_success: (bool) flow config information is setting success.
            True: setting success.
            False: lose config information.
        """

        # set flow_id
        if 'flow_id' in obj:
            self.flow_id = obj['flow_id']
        else:
            raise AssertionError(self.ERR_MSG_CONFIG_PARAM_NOT_FOUND + ' flow_id')
            return False

        # set node_id
        if 'node_id' in obj:
            self.current_node_id = obj['node_id']
        else:
            if self.mode==self.mode_type['parser']: # parser api
                pass
            else:
                raise AssertionError(self.ERR_MSG_CONFIG_PARAM_NOT_FOUND + ' node_id')
                return False

        # set host url
        if 'host_url' in obj:
            self.host_url = obj['host_url']
        else:
            raise AssertionError(self.ERR_MSG_CONFIG_PARAM_NOT_FOUND + ' host_url')
            return False

        return True



    def get_flow_list(self):
        """
        Call Node-RED api to get flow list.

        needed variable: flow_id, host_url

        generate: flow_list (list) all nodes in this flow_id.
            if not exist, variable will be None.
        
        :return flow_list: (list) flow list from Node-RED
            (if can not get flow list from Node-RED api, return None.)
        """
        if (self.host_url != None) and (self.flow_id != None):
            url = self.host_url + 'flow/' + str(self.flow_id)

            # get flow list
            try:
                result = requests.get(url)  # GET

            except Exception as err:
                self.flow_list = None
                return None

            
            # parse response json
            try:
                result = json.loads(result.text)

            except ValueError as err:
                return None
            
            else:
                # set flow_list
                if 'nodes' in result:
                    self.flow_list = result['nodes']
                    return self.flow_list
                else:
                    self.flow_list = None
                    return None
            
        else:
            self.flow_list = None
            return None



    def get_node_item(self, select_node_id, is_current_node=True):
        """
        Get Node-RED item from flow_list.

        :param  select_node_id: (string) node id in Node-RED, for select node.
        :param  is_current_node: (bool) This node id is current node.
            True: Set this node information into node_obj.
            False: Do not set this node information into node_obj.

        :return node: (dict) get this node setting information.
            if not exist, return None.
        """
        if self.flow_list != None:
            for item in self.flow_list:
                if str(item['id']) == str(select_node_id):
                    if is_current_node == True:
                        self.current_node_obj = item  # set into variable

                    return item
                else:
                    continue

        return None



    def get_firehose_node_id(self):
        """
        Find node id of firehose type in flow.
        (check for key name: _node_type)

        :return node_id: (string) node id of firehose
            if do not find node_id, function will return ''.
        """
        node_id = ''


        if self.flow_list!=None:
            for item in self.flow_list:
                # whether _node_type is firehose
                if ('_node_type' in item) and (str(item['_node_type'])=='firehose'):
                    node_id = item['id']
                    break


        return node_id

    

    def get_sso_node_id(self):
        """
        Find node id of sso_setting type in flow.
        (check for key-value: type=sso_setting)

        :return node_id: (string) node id of sso
            if do not find node_id, function will return ''.
        """
        node_id = ''


        if self.flow_list!=None:
            for item in self.flow_list:
                # whether type=sso_setting
                if ('type' in item) and (str(item['type'])=='sso_setting'):
                    node_id = item['id']
                    break


        return node_id



    def set_headers(self):
        """
        Generate headers object for request headers.

        :return obj: (dict) request headers object.
            {Content-Type, flow_id, node_id, host_url}
        """
        obj = {
            'Content-Type': 'application/json',
            'flow_id': self.flow_id,
            'node_id': '',  # need to set
            'host_url': self.host_url
        }

        return obj



    def exe_next_node(self, data, next_list=None, debug=False):
        """
        Request next node api to execute.
        Dependency: get_node_item(), set_headers()

        :param  next_list: (list) list of next nodes.
        :param  data: (dict) data will send to next node. (dataframe dict)
        :param  debug: (bool) whether for debug use. (default=False)

        :return error_node: (string) node id with error occur.
        """
        error_node = '0'    # node with error occur
        error_msg = ''  # error message

        # check for next node is firehose
        if self.mode==self.mode_type['parser']:
            if type(next_list)!=list: # input param occur type error
                error_node = self.current_node_id
                error_msg = self.ERR_MSG_NEXT_LIST_TYPE
                return error_node, error_msg

            elif len(next_list)!=1:
                error_node = self.current_node_id
                error_msg = self.ERR_MSG_NUMBER_OF_FIREHOSE
                return error_node, error_msg

        else:
            next_list = self.current_node_obj['wires'][0]
        
        headers_obj = self.set_headers()    # request headers
        #data = {'data': data}   # dataframe dict set value into key:data


        # POST to each next node
        for item in next_list:
            next_node_obj = self.get_node_item(item, is_current_node=False) # get next node
            headers_obj['node_id'] = item   # set request headers

            if 'url' in next_node_obj:
                # request next node to execute
                try:
                    result = requests.post(next_node_obj['url'], headers=headers_obj, json=data)    # POST

                    if debug==True:
                        print(result.text)

                except Exception as err:
                    error_node = item
                    error_msg = str(err)
                    return error_node, error_msg

                # parse result(json) from response
                try:
                    resp_json = json.loads(result.text)   # trans POST response to json
                
                except ValueError as err:
                    error_node = item
                    error_msg = result.text
                    return error_node, error_msg

                else:
                    if result.status_code != requests.codes.ok: # not success
                        # whether error_node exists
                        if 'error_node' in resp_json:
                            error_node = resp_json['error_node']
                        else:
                            error_node = item

                        # whether error_msg exists
                        if 'error_msg' in resp_json:
                            error_msg = resp_json['error_msg']
                        else:
                            error_msg = result.text
                        
                        return error_node, error_msg

                    elif result.status_code == requests.codes.ok:   # success
                        if ('error_node' in resp_json) and (resp_json["error_node"]!='0'):  # if error_node is not default value
                            error_node = resp_json['error_node']
                            error_msg = resp_json['error_msg']

                        return error_node, error_msg

            else:
                continue
            
        return error_node, error_msg



    def get_sso_token(self, req_body):
        """
        Get SSO token.

        :param  req_body: (dict) request body for request sso api.
            {username, password}

        :return resp: (string) response sso token
        :return status: (int) status code
        """
        sso_url = self.sso_host_url + '/v1.5/auth/native'
        headers_obj = {
            'Content-Type': 'application/json'
        }


        try:
            result = requests.post(sso_url, headers=headers_obj, json=req_body)    # POST

        except Exception as err:
            resp = str(err)
            status = 500
            return resp, status
        
        
        # parse result(json) from response
        try:
            resp_json = json.loads(result.text)   # trans POST response to json
        
        except ValueError as err:
            resp = str(err)
            status = 500
            return resp, status


        # return
        if 'accessToken' in resp_json:
            resp = resp_json['accessToken']
            status = 200
            return resp, status
        else:
            resp = resp_json['message']
            status = 500
            return resp, status



    def get_afs_credentials(self, sso_token):
        """
        Get AFS credentials about service name, service key.

        :param  sso_token:  (string) sso token

        :return resp: (string) response afs credentials list
        :return status: (int) status code
        """
        afs_url = self.afs_host_url + "/v1/" + self.afs_instance_id + "/services"
        headers_obj = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + sso_token
        }


        try:
            result = requests.get(afs_url, headers=headers_obj) # GET

        except Exception as err:
            resp = str(err)
            status = 500
            return resp, status
        
        
        # parse result(json) from response
        try:
            resp_json = json.loads(result.text)   # trans POST response to json
        
        except ValueError as err:
            resp = str(err)
            status = 500
            return resp, status


        # return
        resp = resp_json
        status = 200
        return resp, status




    # ------
    def get_flow_list_ab(self, result):
        # set flow_list
        if 'nodes' in result:
            self.flow_list = result['nodes']
        else:
            raise AssertionError('Dict has no key name "node"')
            self.flow_list = None
    

