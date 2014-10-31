#!/usr/bin/env python2.7
#
# Copyright (C) 2013-2014 DNAnexus, Inc.
#
# This file is part of dx-toolkit (DNAnexus platform client libraries).
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not
#   use this file except in compliance with the License. You may obtain a copy
#   of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import sys, json

preamble = '''// Do not modify this file by hand.
//
// It is automatically generated by src/api_wrappers/generateJSAPIWrappers.py.
// (Run make api_wrappers to update it.)

var dx = require('DNAnexus');
'''

class_method_template = '''
exports.{method_name} = function(input_params) {{
  return dx.DXHTTPRequest('{route}', input_params);
}};
'''

object_method_template = '''
exports.{method_name} = function(object_id, input_params) {{
  return dx.DXHTTPRequest('/' + object_id + '/{method_route}', input_params);
}};
'''

app_object_method_template = '''
exports.{method_name} = function(app_id_or_name, input_params) {{
  return dx.DXHTTPRequest('/' + app_id_or_name + '/{method_route}', input_params);
}};

exports.{method_name}WithAlias = function(app_name, app_alias, input_params) {{
  return exports.{method_name}(app_name + '/' + app_alias, input_params);
}};
'''

print preamble

for method in json.loads(sys.stdin.read()):
    route, signature, opts = method
    method_name = signature.split("(")[0]
    if (opts['objectMethod']):
        root, oid_route, method_route = route.split("/")
        if oid_route == 'app-xxxx':
            print app_object_method_template.format(method_name=method_name, method_route=method_route)
        else:
            print object_method_template.format(method_name=method_name, method_route=method_route)
    else:
        print class_method_template.format(method_name=method_name, route=route)