#-*-coding:utf-8 -*-
import datetime
import time
import json
import traceback
import requests
import os, sys
import pandas as pd



class flow:
    
    flow_id = None  # Node-RED flow id
    flow_list = None    # Node-RED all nodes in flow
    current_node_id = None  # Node-RED current node id
    current_node_obj = None # Node-RED current node config
    host_url = None # host url for Node-RED



    def __init__(self):
        """
        Initialize.
        """
        self.flow_id = None  # Node-RED flow id
        self.flow_list = None    # Node-RED all nodes in flow
        self.current_node_id = None  # Node-RED current node id
        self.current_node_obj = None # Node-RED current node config
        self.host_url = None # host url for Node-RED



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
            return False
        
        # set node_id
        if 'node_id' in obj:
            self.current_node_id = obj['node_id']
        else:
            return False
        
        # set host url
        if 'host_url' in obj:
            self.host_url = obj['host_url']
        else:
            return False
        
        return True



    def get_flow_list(self):
        """
        Call Node-RED api to get flow list.
        
        needed variable: flow_id, host_url
        
        generate: flow_list (list) all nodes in this flow_id.
            if not exist, variable will be None.
        """
        if (self.host_url!=None) and (self.flow_id!=None):
            url = self.host_url + 'flow/' + str(self.flow_id)

            result = requests.get(url)  # GET
            result = json.loads(result.text)    # get response

            # set flow_list
            if 'nodes' in result:
                self.flow_list = result['nodes']
            else:
                self.flow_list = None
        else:
            self.flow_list = None



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
        if self.flow_list!=None:
            for item in self.flow_list:
                if str(item['id']) == str(select_node_id):
                    if is_current_node==True:
                        self.current_node_obj = item    # set into variable

                    return item
                else:
                    continue

        return None



    def generate_headers(self):
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



    def exe_next_node(self, data):
        """
        Request next node api to execute.
        Dependency: get_node_item(), generate_headers()

        :param  data: (list) data will send to next node.

        :return error_node: (string) node id with error occur.
        """
        error_node = '0'    # node with error occur
        error_msg = ''  # error message
        next_list = self.current_node_obj['wires'][0]
        headers_obj = self.generate_headers()


        # POST to each next node
        for item in next_list:
            next_node_obj = self.get_node_item(item, is_current_node=False) # get next node
            headers_obj['node_id'] = item   # set request headers

            if 'url' in next_node_obj:
                try:
                    result = requests.post(next_node_obj['url'], headers=headers_obj, json=data)    # POST
                    resp_json = json.loads(result.text)   # trans POST response
                except Exception as err:
                    error_node = item
                    error_msg = str(err)
                    return error_node, error_msg

                if (result.status_code!=200) and (result.status_code!=204): # not success
                    error_node = item
                    error_msg = result.text
                    return error_node, error_msg

                elif (result.status_code==200) or (result.status_code==204):
                    if ('error_node' in resp_json) and (resp_json["error_node"]!='0'):  # if error_node is not default value
                        error_node = resp_json['error_node']
                        error_msg = resp_json['error_msg']

                    return error_node, error_msg
            
            else:
                continue
            
        return error_node, error_msg

