#!/usr/bin/env python
#   Copyright (c) 2006-2007 Open Source Applications Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import windmill
import sys, os, logging

logger = logging.getLogger(__name__)

jsonrpc_client = windmill.tools.make_jsonrpc_client()
xmlrpc_client = windmill.tools.make_xmlrpc_client()

def clear_queue():
    response = jsonrpc_client.next_action()
    while response['result']['method'] != 'defer':
        response = jsonrpc_client.next_action()
        
windmill.settings['controllers'] = []
        
def start_firefox():
    controller = windmill.browser.get_firefox_controller()
    controller.start()
    windmill.settings['controllers'].append(controller)
    return controller
    
def run_test_file(filename):
    f = open(filename)
    test_strings = f.read().splitlines()
    jsonrpc_client.run_json_tests(test_strings)
    logger.info('Added tests from %s' % filename)
    
def run_test_dir(directory):
    # Try to import test_conf
    sys.path.insert(0, os.path.abspath(directory))
    try:
        import test_conf
        test_list = test_conf.test_list
    except:
        print 'No test_conf.py for this directory, executing all test in directory'
        test_list = [test_name for test_name in os.listdir(os.path.abspath(directory)) if not test_name.startswith('.') and test_name.endswith('.json')]
        
    for test in test_list:
        run_test_file(os.path.abspath(directory)+os.path.sep+test)

def run_given_test_dir():
    run_test_dir(windmill.settings['TEST_DIR'])
    
    logger = logging.getLogger(__name__)

