import datetime
import time
import json
import traceback
import requests
import os, sys
import pandas as pd


class flow:
    def __init__(self, mode='node'):
        """
        Initialize.
        """
        self.mode = mode
        # mode for switch data and constrant

        self.flow_id = None  # Node-RED flow id
        self.flow_list = None  # Node-RED all nodes in flow
        self.current_node_id = None  # Node-RED current node id
        self.current_node_obj = None  # Node-RED current node config
        self.host_url = None  # host url for Node-RED

    def set_flow_config(self, obj):
        """
        Set config(class properties value) of flow.

        :param dict obj: request headers. {flow_id, node_id, host_url}
        :return is_success: flow config information is setting success. True: setting success. False: lose config information.
        :rtype: bool
        """

        # set flow_id
        if 'flow_id' in obj:
            self.flow_id = obj['flow_id']
        else:
            raise AssertionError('flow_id not found.')

        # set node_id
        if 'node_id' in obj:
            self.current_node_id = obj['node_id']
        else:
            if self.mode == 'starter':  # parser api
                pass
            else:
                raise AssertionError('node_id not found.')

        # set host url
        if 'host_url' in obj:
            self.host_url = obj['host_url']
        else:
            raise AssertionError('host_url not found.')

        return True

    def get_flow_list(self):
        """
        Call Node-RED api to get flow list. Get flow_id and host_url from instance variable and assign flow_list to instance.
        flow_list is a list contain all nodes with this flow_id. if not exist, flow_list will be None.
        """
        if (self.host_url != None) and (self.flow_id != None):
            url = self.host_url + 'flow/' + str(self.flow_id)

            result = requests.get(url)  # GET
            result = json.loads(result.text)  # get response

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

        :param str select_node_id: node id in Node-RED, for select node.
        :param bool is_current_node: This node id is current node. True: Set this node information into node_obj. False: Do not set this node information into node_obj.
        :return node: get this node setting information. if not exist, return None.
        :rtype: dict
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
        Find node id of firehose type in flow. (check for key name: _node_type)

        :return node_id: node id of firehose
        :rtype: str
        """
        node_id = ''

        if self.flow_list != None:
            for item in self.flow_list:
                # whether _node_type is firehose
                if ('_node_type' in item) and (str(
                        item['_node_type']) == 'firehose'):
                    node_id = item['id']
                    break

        return node_id

    def set_headers(self):
        """
        Generate headers object for request headers.

        :return obj: request headers object. {Content-Type, flow_id, node_id, host_url}
        :rtype: dict
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

        :param list next_list: list of next nodes.
        :param data: data will send to next node. (dataframe dict)
        :type data: dict or pandas.Dataframe
        :return error_node: node id with error occur.
        :rtype: str
        """
        error_node = '0'  # node with error occur
        error_msg = ''  # error message

        # list of next nodes
        if next_list == None:
            next_list = self.current_node_obj['wires'][0]
        else:
            if type(next_list) != list:  # input param occur type error
                print(type(next_list))
                error_node = self.current_node_id
                error_msg = 'list of next node is error.'
                raise AssertionError('list of next node is error.')

        headers_obj = self.set_headers()
        # data = {'data': data}  # dataframe dict set value into key:data

        # POST to each next node
        for item in next_list:
            next_node_obj = self.get_node_item(
                item, is_current_node=False)  # get next node
            headers_obj['node_id'] = item  # set request headers

            if 'url' in next_node_obj:
                try:
                    result = requests.post(
                        next_node_obj['url'], headers=headers_obj,
                        json=data)  # POST
                    resp_json = json.loads(result.text)  # trans POST response

                    if debug == True:
                        return resp_json

                except Exception as err:
                    error_node = item
                    error_msg = str(err)
                    return error_node, error_msg

                if (result.status_code != 200) and (result.status_code !=
                                                    204):  # not success
                    error_node = item
                    error_msg = result.text
                    return error_node, error_msg

                elif (result.status_code == 200) or (
                        result.status_code == 204):
                    if ('error_node' in resp_json) and (
                            resp_json["error_node"] !=
                            '0'):  # if error_node is not default value
                        error_node = resp_json['error_node']
                        error_msg = resp_json['error_msg']

                    return error_node, error_msg

            else:
                continue

        return error_node, error_msg

        # error_node, error_msg = self.req_next_node(next_list, headers_obj)

        # return error_node, error_msg

    # def req_next_node(self, next_list, headers_obj, data={}):
    #     """
    #     Request next node api to execute.
    #     Dependency: get_node_item(), set_headers(), exe_next_node()

    #     :param  data: (list) data will send to next node.

    #     :return error_node: (string) node id with error occur.
    #     """
    #     error_node = '0'    # node with error occur
    #     error_msg = ''  # error message

    #     # POST to each next node
    #     for item in next_list:
    #         next_node_obj = self.get_node_item(item, is_current_node=False) # get next node
    #         headers_obj['node_id'] = item   # set request headers

    #         if 'url' in next_node_obj:
    #             try:
    #                 result = requests.post(next_node_obj['url'], headers=headers_obj, json=data)    # POST
    #                 resp_json = json.loads(result.text)   # trans POST response
    #             except Exception as err:
    #                 error_node = item
    #                 error_msg = str(err)
    #                 return error_node, error_msg

    #             if (result.status_code!=200) and (result.status_code!=204): # not success
    #                 error_node = item
    #                 error_msg = result.text
    #                 return error_node, error_msg

    #             elif (result.status_code==200) or (result.status_code==204):
    #                 if ('error_node' in resp_json) and (resp_json["error_node"]!='0'):  # if error_node is not default value
    #                     error_node = resp_json['error_node']
    #                     error_msg = resp_json['error_msg']

    #                 return error_node, error_msg

    #         else:
    #             continue

    #     return error_node, error_msg

    def get_flow_list_ab(self, result):
        # set flow_list
        if 'nodes' in result:
            self.flow_list = result['nodes']
        else:
            raise AssertionError('Dict has no key name "node"')
            self.flow_list = None
