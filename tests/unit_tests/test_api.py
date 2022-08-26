#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import unittest

import urllib

from decentra_network.api.main import start
from decentra_network.lib.clean_up import CleanUp_tests

import multiprocessing

class Test_API(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()
        backup = sys.argv
        sys.argv = [sys.argv[0]]
        cls.proc = multiprocessing.Process(target=start, args=("7777",))
        cls.proc.start()
        sys.argv = backup
        time.sleep(2)
    
    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()

    def test_api_debug_by_response_status_code(self):
        response = urllib.request.urlopen("http://0.0.0.0:7777/wallet/print")
        self.assertEqual(response.status, 200, "A problem on the API.")


unittest.main(exit=False)
