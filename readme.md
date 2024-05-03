# OpenSesame example plugin including EVT-device connection

## About

EVT- or EventExchanger-devices are used for the purpose of event-triggering and event-marking and were developed by the Research Support group of the faculty of Behavioral and Social Science from the University of Groningen.

This is an example plugin for OpenSesame 4.0 or later. For more information about creating OpenSesame extensions, see the OpenSesame documentation site:

- http://osdoc.cogsci.nl/dev/plugin

You can package the extension as a `.whl` using [Poetry](https://python-poetry.org/):

```
poetry build
```

## Dependencies

Install pyevt with:

`pip install pyevt` or
`pip install --user pyevt` on managed computers.

**Note:** For now, use the latest python module from the 'develop' branch from the pyevt repository:

![https://github.com/MartinStokroos/pyevt/tree/develop](https://github.com/MartinStokroos/pyevt/tree/develop)

## License

No rights reserved. All files in this repository are released into the public domain.
