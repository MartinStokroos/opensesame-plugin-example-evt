"""An example plugin to demonstrate the connection to EVT hardware"""

# The category determines the group for the plugin in the item toolbar
category = "RUG/BSS hardware"
# Defines the GUI controls
controls = [
    {
        "type": "combobox",
        "var": "device",
        "label": "Select device :",
        "options": [
            "DUMMY"
        ],
        "name": "device_combobox_widget",
        "tooltip": "Select the desired EVT-device or DUMMY."
    }, {
        "type": "checkbox",
        "var": "refresh_device_list",
        "label": "Refresh device list",
        "name": "refresh_checkbox_widget",
        "tooltip": "Refresch device list checkbox"
    }, {
        "type": "checkbox",
        "var": "checkbox",
        "label": "Example checkbox",
        "name": "checkbox_widget",
        "tooltip": "An example checkbox"
    }, {
        "type": "color_edit",
        "var": "color",
        "label": "Color",
        "name": "color_widget",
        "tooltip": "An example color edit"
    }, {
        "type": "combobox",
        "var": "option",
        "label": "Select option",
        "options": [
            "Option 1",
            "Option 2"
        ],
        "name": "combobox_widget",
        "tooltip": "An example combobox"
    }, {
        "type": "filepool",
        "var": "file",
        "label": "Select file",
        "name": "filepool_widget",
        "tooltip": "An example filepool widget"
    }, {
        "type": "line_edit",
        "var": "text",
        "label": "Enter text",
        "name": "line_edit_widget",
        "tooltip": "An example line_edit widget"
    }, {
        "type": "spinbox",
        "var": "spinbox_value",
        "label": "Enter value",
        "min_val": 0,
        "max_val": 100000,
        "name": "spinbox_widget",
        "prefix": "approx. ",
        "suffix": " ms",
        "tooltip": "An example spinbox widget"
    }, {
        "type": "slider",
        "var": "slider_value",
        "label": "Select value",
        "min_val": 0,
        "max_val": 100000,
        "name": "slider_widget",
        "left_label": "low",
        "right_label": "high",
        "tooltip": "An example slider widget"
    }, {
        "type": "text",
        "label": "Some non-interactive text"
    }, {
        "type": "editor",
        "var": "script",
        "label": "Python editor",
        "name": "editor_widget",
        "syntax": True,
        "tooltip": "An example editor widget"
    }, {
        "type": "checkbox",
        "var": "close_device",
        "label": "Auto close EVT-device(s). (Use this for the latter instance of the plugin or with a single instance of the plugin.)",
        "name": "close_device_checkbox_widget",
        "tooltip": "Close device list checkbox"
    }
]
