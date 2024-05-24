"""
No rights reserved. All files in this repository are released into the public
domain.

This example shows how to attach EventExchanger (EVT-2) devices to the plugin.

Author: M. Stokroos
Date: May 2024
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas
from libopensesame.oslogging import oslogger
from time import sleep
from pyevt import EventExchanger # pyevt 2.0

# constant
_DEVICE_GROUP = u'EVT'

# global vars
open_devices = {} # store device handles.


class ExamplePluginEvt(Item):
    """An example plugin that shows a simple canvas. The class name
    should be the CamelCase version of the folder_name and file_name. So in
    this case both the plugin folder (which is a Python package) and the
    .py file (which is a Python module) are called example_plugin, whereas
    the class is called ExamplePlugin.
    """
    
    description = u"A plug-in to demonstrate the control of EVT-2 devices."

    global open_devices

    def reset(self):
        """Resets plug-in to initial values."""
        # Here we provide default values for the variables that are specified
        # in __init__.py. If you do not provide default values, the plug-in
        # will work, but the variables will be undefined when they are not
        # explicitly # set in the GUI.
        self.var.device = u'DUMMY'
        self.var.refresh_device_list = 'no'
        self.var.checkbox = 'yes'  # yes = checked, no = unchecked
        self.var.color = 'white'
        self.var.option = 'Option 1'
        self.var.file = ''
        self.var.text = 'Default text'
        self.var.spinbox_value = 1
        self.var.slider_value = 1
        self.var.script = 'print(10)'
        self.var.close_device = 'no'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        super().prepare()

        if self.var.device == u'DUMMY':
            oslogger.warning("Hardware configuration could have changed! Dummy prepare...")
        elif len(open_devices) == 0:
            # Create a shadow device list to find 'path' from the current selected device.
            # 'path' is an unique device ID.
            temp_evt = EventExchanger()
            sleep(1) # without a delay, the list will not always be complete.
            try:
                device_list = temp_evt.scan(_DEVICE_GROUP) # filter on allowed EVT types
                del temp_evt
                # oslogger.info("device list: {}".format(device_list))
                for d in device_list:
                    sleep(1) # without a delays, the device will not always be there.
                    composed_string = d['product_string'] + " s/n: " + d['serial_number']
                    open_devices[composed_string] = EventExchanger()
                    # Get evt device handle:
                    open_devices[composed_string].attach_id(d['path'])
                    oslogger.info('Device successfully attached as: {} s/n: {}'.format(
                        d['product_string'], d['serial_number']))
                    oslogger.info('        ...  and with device ID: {}'.format(open_devices[composed_string]))
            except:
                oslogger.warning("Connecting EVT-device failed! Device set to dummy.")
                self.var.device = u'DUMMY'

        # searching for selected device:
        self.current_device = None
        for dkey in open_devices:
            if self.var.device[:15] in dkey:
                self.current_device = dkey # assign to value that belongs to the key.
        if self.current_device is None:
            oslogger.warning("EVT-device not found! Device set to dummy.")
            self.var.device = u'DUMMY'
        else:
            oslogger.info('Preparing device: {}'.format(open_devices[self.current_device]))
            open_devices[self.current_device].write_lines(0) # clear lines

        # pass device var to experiment as global:
        var_name = "self.experiment.var.connected_device_" + self.name
        exec(f'{var_name} = "{self.var.device}"')

    def run(self):
        """The run phase of the plug-in goes here."""
        if self.var.device == u'DUMMY':
            oslogger.info('Dummy run')
        else:
            # Do your thing with EVT here.
            open_devices[self.current_device].pulse_lines(170, 1000) # value=170, duration=1s, non-blocking!

        # close the device?
        if self.var.close_device == 'yes':
            for dkey in open_devices:
                try:
                    open_devices[dkey].close()
                    oslogger.info('Device: {} successfully closed!'.format(open_devices[dkey]))
                except:
                    oslogger.warning('Device {} for closing not found!'.format(open_devices[dkey]))


class QtExamplePluginEvt(ExamplePluginEvt, QtAutoPlugin):
    """This class handles the GUI aspect of the plug-in. The name should be the
    same as that of the runtime class with the added prefix Qt.
    
    Important: defining a GUI class is optional, and only necessary if you need
    to implement non-standard interfaces or interactions. In this case, we use
    the GUI class to dynamically enable/ disable some controls (see below).
    """

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors. Since the parent constructures take different arguments
        # we cannot use super().
        ExamplePluginEvt.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        """Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """
        # First, call the parent constructor, which constructs the GUI controls
        # based on __init_.py.
        super().init_edit_widget()
        
        self.combobox_add_devices() # first time fill the combobox

        # Event triggered calls:
        self.refresh_checkbox_widget.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox_widget.currentIndexChanged.connect(self.update_combobox_device)
        self.close_device_checkbox_widget.stateChanged.connect(self.close_device)

    def refresh_combobox_device(self):
        if self.refresh_checkbox_widget.isChecked():
            # renew list:
            self.combobox_add_devices()

    def update_combobox_device(self):
        self.refresh_checkbox_widget.setChecked(False)
        
    def combobox_add_devices(self):
        self.device_combobox_widget.clear()
        self.device_combobox_widget.addItem(u'DUMMY', userData=None)
        
        # Create the EVT device list
        sleep(1) # delay after possible init of a previous instance of this plugin. 
        myevt = EventExchanger()
        try:
            device_list = myevt.scan(_DEVICE_GROUP) # filter on allowed EVT types
            del myevt
        except:
            device_list = {}
        
        try:
            previous_device_found = False
            for d in device_list:
                product_string = d['product_string']
                serial_string = d['serial_number']
                composed_string = product_string[15:] + " s/n: " + serial_string
                # add device id to combobox:
                self.device_combobox_widget.addItem(composed_string)
                # previous used device present?
                if self.var.device[:15] in product_string:
                    self.var.device = composed_string
                    previous_device_found = True       
        except:
            self.var.device = u'DUMMY'
            oslogger.warning("No devices found! Switching to dummy.")

        if previous_device_found is False:
            self.var.device = u'DUMMY'
            oslogger.warning("The hardware configuration has been changed since the last run! Switching to dummy.")
            
    def close_device(self):
        if self.close_device_checkbox_widget.isChecked():
            self.var.close_device = 'yes'
        else:
            self.var.close_device = 'no'
