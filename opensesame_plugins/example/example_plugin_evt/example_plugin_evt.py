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
from pyevt import EventExchanger # pyevt 2.0


class ExamplePluginEvt(Item):
    """An example plugin that shows a simple canvas. The class name
    should be the CamelCase version of the folder_name and file_name. So in
    this case both the plugin folder (which is a Python package) and the
    .py file (which is a Python module) are called example_plugin, whereas
    the class is called ExamplePlugin.
    """
    
    description = u"A plug-in to demonstrate the control of EVT-2 devices."
    
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
        # Here open the EVT device
        self.myevt = EventExchanger()

        # Dynamically load an EVT device
        try:
            device_list = self.myevt.scan()
        except:
            oslogger.warning("Connecting EVT device failed!")
        # Create a shadow device list below, to find 'path' from the selected device.
        # 'path' is the unique device ID.
        d_count = 1
        for d in device_list:
            if int(self.var.device[:1]) == 0:
                self.var.device = u'0: DUMMY'
                oslogger.warning("Dummy mode.")
                break
            elif int(self.var.device[:1]) == d_count: 
                self.myevt.attach_id(d['path'])
                oslogger.info('Device successfully attached as:{} s/n:{}'.format(
                    d['product_string'], d['serial_number']))
                break
            d_count += 1

    def run(self):
        """The run phase of the plug-in goes here."""
        # Do your thing with EVT here.
        self.myevt.write_lines(0) # clear lines
        self.myevt.pulse_lines(170, 1000) # value=170, duration=1s, non-blocking!
        self.myevt.close()


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
        self.myevt = EventExchanger()
        self.combobox_add_devices()
        # Prevents hangup if the same device is not found after re-opening the project:
        if not self.var.device in self.device_list: 
            self.var.device = u'0: DUMMY'

        # event based calls:
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
        self.device_list = self.myevt.scan() # Default scans for all 'EventExchanger' devices.
        if self.device_list:
            d_count = 1
            for d in self.device_list:
                product_string = d['product_string']
                serial_number_string = d['serial_number']
                # add string to combobox:
                self.device_combobox.addItem(str(d_count) + ": " + \
                    product_string[15:] + " s/n:" + serial_number_string)
                d_count += 1
                if d_count > 9:
                    break
        else:
            self.var.device = u'0: DUMMY'