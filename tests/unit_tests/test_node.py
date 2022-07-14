#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import copy
import time
import unittest

from decentra_network.node.server.server import server
from decentra_network.node.get_candidate_blocks import GetCandidateBlocks
from decentra_network.node.unl import Unl


class Test_Node(unittest.TestCase):

    def setUp(self):
        self.node_1 = server("127.0.0.1", 10001)
        self.node_2 = server("127.0.0.1", 10002)
        Unl.save_new_unl_node(self.node_1.id)
        Unl.save_new_unl_node(self.node_2.id)
        time.sleep(2)
        self.node_2.connect("127.0.0.1", 10001)

    def tearDown(self):
        self.node_2.stop()
        self.node_2.join()
        self.node_1.stop()
        self.node_1.join()
        server.connected_node_delete("id5")
        server.connected_node_delete("id2")


    def test_node_by_connection_saving_and_unl_nodes_system(self):
        
        time.sleep(2)
        connection_closing_deleting = True
        finded_node = False
        in_unl_list = False
        get_as_node = False

        nodes_list = server.get_connected_nodes()
        for element in nodes_list:
            if element == self.node_1.id or element == self.node_2.id:
                finded_node = True

                temp_unl_node_list = Unl.get_unl_nodes()
                temp_get_as_node_type = Unl.get_as_node_type(
                    temp_unl_node_list)
                for unl_element in temp_unl_node_list:
                    if unl_element == self.node_1.id or unl_element == self.node_2.id:
                        for node_element_of_unl in temp_get_as_node_type:
                            if (self.node_1.host == node_element_of_unl.host or
                                    self.node_2 == node_element_of_unl.host):
                                if (self.node_1.port
                                        == node_element_of_unl.port
                                        or self.node_2
                                        == node_element_of_unl.port):
                                    get_as_node = True
                        in_unl_list = True
                        Unl.unl_node_delete(unl_element)
                server.connected_node_delete(element)


        self.assertEqual(finded_node, True,
                         "Problem on connection saving system.")
        self.assertEqual(in_unl_list, True,
                         "Problem on UNL node saving system.")
        self.assertEqual(get_as_node, True,
                         "Problem on UNL get as node system.")

    def test_GetCandidateBlocks(self):

        self.node_1.candidate_block = True
        self.node_1.candidate_block_hash = True
        self.node_2.candidate_block = True
        self.node_2.candidate_block_hash = False
        nodes_list = [self.node_1, self.node_2]

        result = GetCandidateBlocks(nodes_list)
        self.assertEqual(result.candidate_blocks, [True, True])
        self.assertEqual(result.candidate_block_hashes, [True, False])


    def test_send_data_all(self):
        self.node_1.save_messages = True
        self.node_2.save_messages = True
        result = self.node_2.send({"action": "test"})
        print(result)
        time.sleep(2)

        self.assertEqual(len(self.node_1.messages), 1)
        self.assertEqual(self.node_1.messages[0], result)



unittest.main(exit=False)
