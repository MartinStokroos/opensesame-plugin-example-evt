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

# global var
open_devices = {} # Store open device handles.


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
        self.var.device = u'0: DUMMY'
        self.var.refresh = 'no'
        self.var.checkbox = 'yes'  # yes = checked, no = unchecked
        self.var.color = 'white'
        self.var.option = 'Option 1'
        self.var.file = ''
        self.var.text = 'Default text'
        self.var.spinbox_value = 1
        self.var.slider_value = 1
        self.var.script = 'print(10)'

    def prepare(self):
        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        super().prepare()

        if int(self.var.device[:1]) == 0:
            oslogger.warning("Dummy prepare")
        else:
            # Create a shadow device list to find 'path' from the current selected device.
            # 'path' is an unique device ID.
            myevt = EventExchanger()
            sleep(0.1) # without a delay, the list will not always be complete.
            try:
                device_list = myevt.scan(_DEVICE_GROUP) # filter on allowed EVT types
                del myevt
                # oslogger.info("device list: {}".format(device_list))
            except:
                oslogger.warning("Connecting EVT device failed!")

            try:
                d_count = 1            
                for d in device_list:
                    if not d_count in open_devices: # skip if already open
                        # Dynamically load all EVT devices from the list
                        open_devices[d_count] = EventExchanger()
                        open_devices[d_count].attach_id(d['path']) # Get evt device handle
                        oslogger.info('Device successfully attached as:{} s/n:{}'.format(
                            d['product_string'], d['serial_number']))
                    d_count += 1
                oslogger.info('open devices: {}'.format(open_devices))
                self.current_device = int(self.var.device[:1])
                oslogger.info('Prepare - current device: {}'.format(self.current_device))
                open_devices[self.current_device].write_lines(0) # clear lines
            except:
                self.var.device = u'0: DUMMY'
                oslogger.warning("No device found! Switching to dummy.")

    def run(self):
        """The run phase of the plug-in goes here."""
        if self.var.device == u'0: DUMMY':
            oslogger.info('Dummy run')
        else:
            # Do your thing with EVT here.
            open_devices[self.current_device].pulse_lines(170, 1000) # value=170, duration=1s, non-blocking!
            # open_devices[self.current_device].close()
            # Not closing device, because more instances of this plugin might run.


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
        self.refresh_checkbox.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox.currentIndexChanged.connect(self.update_combobox_device)

    def refresh_combobox_device(self):
        if self.refresh_checkbox.isChecked():
            # renew list:
            self.combobox_add_devices()

    def update_combobox_device(self):
        self.refresh_checkbox.setChecked(False)
        
    def combobox_add_devices(self):
        self.device_combobox.clear()
        self.device_combobox.addItem(u'0: DUMMY', userData=None)
        
        # Create the EVT device list
        myevt = EventExchanger()
        sleep(0.5) # without a delay, the list will not always be complete.
        try:
            device_list = myevt.scan(_DEVICE_GROUP) # filter on allowed EVT types
            del myevt
        except:
            device_list = None
        
        added_item_list = {}
        if device_list:
            d_count = 1
            for d in device_list:
                product_string = d['product_string']
                serial_string = d['serial_number']
                composed_string = str(d_count) + ": " + \
                    product_string[15:] + " s/n: " + serial_string
                # add device string to combobox:
                self.device_combobox.addItem(composed_string)
                added_item_list[d_count] = composed_string
                d_count += 1
                if d_count > 9:
                    # keep number of digits 1
                    break
            # Prevents hangup if the old device is not found after reopening the project.
            # Any change of the hardware configuration can cause this.
            if not self.var.device in added_item_list.values():
                self.var.device = u'0: DUMMY'

