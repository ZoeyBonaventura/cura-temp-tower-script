# -*- coding: utf-8 -*-

import json
import re

from ..Script import Script


class TempTower(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return json.dumps({
            'name': 'Temp Tower',
            'key': 'TempTower',
            'metadata': {},
            'version': 2,
            'settings': {
                'start_temperature': {
                    'label': 'Start Temperature',
                    'description': 'Initial nozzle temperature',
                    'unit': '°C',
                    'type': 'int',
                    'default_value': 265
                },
                'height_increment': {
                    'label': 'Height Increment',
                    'description': (
                        'Adjust temperature each time height param '
                        'changes by this much'
                    ),
                    'unit': 'mm',
                    'type': 'int',
                    'default_value': 10
                },
                'temperature_increment': {
                    'label': 'Temperature Increment',
                    'description': (
                        'Increase temperature by this much with each height increment. '
                        'Use negative values for towers that become gradually cooler.'
                    ),
                    'unit': '°C',
                    'type': 'int',
                    'default_value': -5
                },
                'start_height': {
                    'label': 'Start Height ',
                    'description': (
                        'Start the temperature tower at this height.'
                    ),
                    'unit': 'mm',
                    'type': 'float',
                    'default_value': 1.4
                },
                'layer_height': {
                    'label': 'Layer Height ',
                    'description': (
                        'The height of each layer.'
                    ),
                    'unit': 'mm',
                    'type': 'float',
                    'default_value': 0.2
                }
            }
        })

    def execute(self, data):
        start_temp = self.getSettingValueByKey('start_temperature')
        height_inc = self.getSettingValueByKey('height_increment')
        temp_inc = self.getSettingValueByKey('temperature_increment')
        start_height = self.getSettingValueByKey('start_height')
        layer_height = self.getSettingValueByKey('layer_height')

        final_layer = self.finalLayer(data)

        cmd_re = re.compile(
            r'G[0-9]+ '
            r'(?:F[0-9]+ )?'
            r'X[0-9]+\.?[0-9]* '
            r'Y[0-9]+\.?[0-9]* '
            r'Z(-?[0-9]+\.?[0-9]*)'
        )

        layer_re = re.compile(r';LAYER:([0-9]+)')

        # Set initial state
        current_temp = 0

        for i, layer in enumerate(data):
            layer_match = layer_re.match(layer)

            # We don't care about GCODE being run anywhere but on a layer
            if layer_match is None:
                continue

            current_layer = int(layer_match.groups()[0])
            current_layer_height = current_layer * layer_height

            if current_layer_height < start_height:
                continue

            new_temp = start_temp + int((current_layer_height - start_height) / height_inc) * temp_inc

            if new_temp != current_temp:
                current_temp = new_temp
                insert_index = layer.find('\n')

                data[i] = layer[:insert_index] + ('\n;TYPE:CUSTOM\nM104 S%d' % new_temp) + layer[insert_index:]

        return data

    # Gets the final layer number for the print to keep from doing an extra temperature change at the end
    def finalLayer(self, data):
        final_layer = 0
        layer_re = re.compile(r';LAYER:([0-9]+)')

        for i, layer in enumerate(data):
            layer_id = layer.split('\n', 1)[0]
            match = layer_re.match(layer_id)

            if match is not None:
                layer_num = int(match.groups()[0])
                final_layer = max(final_layer, layer_num)

        return final_layer