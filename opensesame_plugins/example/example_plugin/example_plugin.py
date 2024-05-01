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


class ExamplePlugin(Item):
    """An example plugin that shows a simple canvas. The class name
    should be the CamelCase version of the folder_name and file_name. So in
    this case both the plugin folder (which is a Python package) and the
    .py file (which is a Python module) are called example_plugin, whereas
    the class is called ExamplePlugin.
    """
    
    description = u"A plug-in to demonstrate the control on EVT-2 devices."
    
    def reset(self):
        """Resets plug-in to initial values."""
        # Here we provide default values for the variables that are specified
        # in __init__.py. If you do not provide default values, the plug-in
        # will work, but the variables will be undefined when they are not
        # explicitly # set in the GUI.
        self.var.device = u'DUMMY'
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
        # Here simply open the EVT device
        self.myevt = EventExchanger()
        if self.var.device != u'DUMMY':
            # Dynamically load an EVT device
            try:
                self.myevt.attach(self.var.device[0:15])
                oslogger.info("EVT-device connected.")
            except:
                self.var.device = u'DUMMY'
                oslogger.warning("Connecting EVT device failed! Switching to dummy-mode.")

    def run(self):
        """The run phase of the plug-in goes here."""
        # Do your thing with EVT here.
        self.myevt.write_lines(0) # clear lines
        self.myevt.pulse_lines(170, 1000) # value=170, duration=1s, non-blocking!
        clock.sleep(2000) # clock is not defined here?
        self.myevt.pulse_lines(85, 1000) # value=170, duration=1s


class QtExamplePlugin(ExamplePlugin, QtAutoPlugin):
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
        ExamplePlugin.__init__(self, name, experiment, script)
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
        list_of_devices = self.myevt.scan(u"EventExchanger")
        if list_of_devices:
            for i in list_of_devices:
                self.device_combobox.addItem(i)
        # Prevents hangup if the same device is not found after reopening the project:
        if not self.var.device in list_of_devices: 
            self.var.device = u'DUMMY'

        # event based calls:
        self.refresh_checkbox.stateChanged.connect(self.refresh_combobox_device)
        self.device_combobox.currentIndexChanged.connect(self.update_combobox_device)

    def refresh_combobox_device(self):
        if self.refresh_checkbox.isChecked():
            self.device_combobox.clear()
            # create new list:
            self.device_combobox.addItem(u'DUMMY', userData=None)
            list_of_devices = self.myevt.scan(u"EventExchanger")
            if list_of_devices:
                for i in list_of_devices:
                    self.device_combobox.addItem(i)

    def update_combobox_device(self):
        self.refresh_checkbox.setChecked(False)