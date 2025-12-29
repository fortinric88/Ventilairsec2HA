# How to Add This Repository to Home Assistant

Follow these steps to add the Ventilairsec2HA addon repository to your Home Assistant installation:

## Method 1: Web UI (Recommended)

### Steps:

1. **Open Home Assistant Settings**
   - Go to `http://your-home-assistant-ip:8123`
   - Navigate to **Settings** → **Add-ons & Services** → **Add-ons** tab

2. **Access Repository Manager**
   - Click the **⋮ (three dots)** menu button in the top right corner
   - Select **Repositories**

3. **Add New Repository**
   - Paste this URL in the text field:
     ```
     https://github.com/fortinric88/Ventilairsec2HA
     ```
   - Click **Create**

4. **Confirm Addition**
   - You should see "Ventilairsec Home Assistant Addons" appear in your list
   - The repository is now available

## Method 2: Configuration File (Advanced)

If the web UI method doesn't work, you can manually edit the configuration:

1. **SSH into Home Assistant** or use the VS Code add-on
2. **Edit** `/root/.homeassistant/configuration.yaml`
3. **Add** the following section:
   ```yaml
   homeassistant:
     community_addons_repositories:
       - https://github.com/fortinric88/Ventilairsec2HA
   ```
4. **Restart Home Assistant**

## Installing the Addon

Once the repository is added:

1. **Refresh** the Add-ons page (clear browser cache if needed)
2. **Find** "Ventilairsec Enocean" in the available addons
3. **Click** on it to view details
4. **Click** "Install" button
5. **Wait** for installation to complete

## First Configuration

After installation:

1. **Go to** Add-ons & Services → Add-ons
2. **Find** "Ventilairsec Enocean" in the installed list
3. **Click** it to open the addon details
4. **Click** "Configuration" tab
5. **Select** your USB serial port (usually `/dev/ttyUSB0`)
6. **Click** "Save"
7. **Click** "Start" to begin the addon

## Troubleshooting

### Repository Not Showing
- Clear browser cache (Ctrl+Shift+Del)
- Refresh the page or restart Home Assistant
- Check your internet connection
- Ensure Home Assistant version is 2023.10.0+

### Can't Find Serial Port
```bash
# List available serial ports
ls -la /dev/tty* | grep -E "USB|ACM|AMA"
```

### Check Addon Logs
1. Go to Add-ons & Services → Ventilairsec Enocean
2. Click the "Logs" button to see any error messages

### Addon Won't Start
- Check that you have a valid serial port selected
- Verify the USB dongle is connected
- Check logs for specific error messages

## Next Steps

- [Configuration Guide](./addons/ventilairsec_enocean/README.md)
- [Device Pairing Instructions](./addons/ventilairsec_enocean/MANIFEST.md#supported-devices)
- [Troubleshooting](./addons/ventilairsec_enocean/README.md#troubleshooting)

---

**Need help?** Check the [GitHub Issues](https://github.com/fortinric88/Ventilairsec2HA/issues)
