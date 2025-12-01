# Ventilairsec OpenEnocean Add-on

This Supervisor add-on runs the OpenEnocean daemon used by the Jeedom plugin to communicate with VMI devices (Purevent) and Enocean sensors.

Usage:
- Configure the add-on `device` (or leave `auto`), `port` (default 55006) and `apikey`.
- Install the companion Home Assistant integration `custom_components/ventilairsec_enocean` from this repository into your Home Assistant `custom_components` folder.

Notes:
- The Dockerfile copies the `openenoceand` script from the repository path `ExemplePluginJeedom/openenocean/resources/openenoceand`. Ensure it is present when building the add-on.
