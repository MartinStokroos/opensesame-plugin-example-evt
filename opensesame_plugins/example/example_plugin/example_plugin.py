"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openexp.canvas import Canvas


class ExamplePlugin(Item):
    """An example plugin that shows a simple canvas. The class name
    should be the CamelCase version of the folder_name and file_name. So in
    this case both the plugin folder (which is a Python package) and the
    .py file (which is a Python module) are called example_plugin, whereas
    the class is called ExamplePlugin.
    """
    def reset(self):
        """Resets plug-in to initial values."""
        # Here we provide default values for the variables that are specified
        # in info.json. If you do not provide default values, the plug-in will
        # work, but the variables will be undefined when they are not
        # explicitly # set in the GUI.
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
        # Here simply prepare a canvas with a fixatio dot.
        self.c = Canvas(self.experiment)
        self.c.fixdot()

    def run(self):
        """The run phase of the plug-in goes here."""
        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().
        self.set_item_onset(self.c.show())


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
        # If you specify a 'name' for a control in __init__.py, this control
        # will be available self.[name]. The type of the object depends on
        # the control. A checkbox will be a QCheckBox, a line_edit will be a
        # QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
        # to the setEnabled() slot of the QLineEdit. This has the effect of
        # disabling the QLineEdit when the QCheckBox is uncheckhed. We also
        # explictly set the starting state.
        self.line_edit_widget.setEnabled(self.checkbox_widget.isChecked())
        self.checkbox_widget.stateChanged.connect(
            self.line_edit_widget.setEnabled)
