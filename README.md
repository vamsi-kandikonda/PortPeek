# PortPeek - macOS Port Monitor

In the fast-paced world of software development, where applications often rely on network communication for everything from API calls to local servers, keeping a vigilant eye on available ports is not just a best practice it's essential for efficiency, security, and seamless workflows. Imagine spinning up a new dev server only to face cryptic errors because a port is already occupied by another process, or worse, overlooking an unauthorized app hogging a critical port that could expose vulnerabilities. For developers, port conflicts can lead to wasted hours debugging, disrupted testing environments, and even production outages if not caught early. Monitoring ports ensures you can quickly identify and resolve these issues, maintain optimal resource allocation, and safeguard against potential security risks like port scanning attacks or rogue applications.

That's where PortPeek comes in a lightweight macOS status bar application that monitors active network ports and displays the applications using them. With PortPeek residing discreetly in your Mac's menu bar, a simple click reveals a real-time list of all open ports and the exact apps or processes utilizing them. No more digging through Terminal commands like lsof or netstat.

PortPeek delivers instant insights right at your fingertips, allowing you to spot conflicts, kill unnecessary processes, or verify port availability without interrupting your flow. Whether you're running multiple microservices, testing web apps, or just ensuring your setup is secure, PortPeek empowers you to stay in control and focus on what matters building great software. Download it today and peek into your ports with ease!

## Features

- **Status Bar Integration**: Custom network icon in the macOS status bar
- **Real-time Port Monitoring**: Shows active listening and established connections
- **Application Detection**: Identifies which applications are using each port
- **Visual Indicators**: 🟢 for listening ports, 🔵 for established connections
- **One-click Refresh**: Easy refresh functionality to update the port list
- **No Permissions Required**: Works immediately without Full Disk Access
- **Minimal Resource Usage**: Lightweight and efficient

## Installation

### 🚀 Quick Start (Fastest Method)

**Ready to use immediately!** Download the pre-built installer:

1. **Download** [`PortPeek-Installer.dmg`](PortPeek-Installer.dmg) from this repository
2. **Double-click** to mount the disk image
3. **Double-click** "Install PortPeek.command"
4. **Done!** PortPeek appears in your menu bar

⚡ **No compilation, no dependencies, no permissions required** - just download and run!

### Alternative: Build from Source

### For Developers

1. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run from Source**:
   ```bash
   python port_monitor_lsof.py
   ```

## Usage

1. Launch PortPeek (installed in Applications folder)
2. Look for the network icon in your macOS status bar
3. Click the icon to view active ports and applications
4. 🟢 indicates listening ports, 🔵 indicates established connections
5. Use "Refresh" to update the port list

## Creating Distribution

To create the installer DMG:

```bash
python create_one_click_installer.py
```

This creates `PortPeek-Installer.dmg` ready for distribution.

## Requirements

- macOS (required for rumps library)
- Python 3.6+
- rumps 0.3.0
- psutil 5.9.5

## How It Works

The application uses:

- **rumps**: Creates the macOS status bar interface
- **psutil**: Monitors network connections and processes
- Filters for `LISTEN` and `ESTABLISHED` connections
- Maps ports to their corresponding applications using process IDs

## Troubleshooting

- **Permission Issues**: On macOS, the app may require elevated permissions to access network connections
  - If you see "Permission denied" in the menu, try running with `sudo python port_monitor.py`
  - Or grant permissions in System Preferences > Security & Privacy > Privacy > Full Disk Access
- **Unknown Applications**: Processes that can't be accessed will show as "Unknown"
- **No Connections**: If no active connections are found, the menu will display a message
- **Virtual Environment**: Make sure to activate the virtual environment before running: `source venv/bin/activate`

## Building for Distribution

### Creating a Standalone App Bundle

To create a double-clickable macOS application bundle using PyInstaller:

1. **Install PyInstaller** (in your virtual environment):

   ```bash
   source venv/bin/activate
   pip install pyinstaller
   ```

2. **Build the App Bundle**:

   ```bash
   pyinstaller --onefile --windowed --name="PortPeek" port_monitor.py
   ```

3. **Find Your App**: The standalone app will be created in the `dist/` folder:
   - `PortPeek.app` - Double-clickable macOS application bundle
   - You can drag this to your Applications folder or run it directly

### Alternative: Using py2app

You can also use py2app for a more native macOS build:

```bash
pip install py2app
python setup.py py2app
```

## Developer

**Developed by:** Vamsi Kandikonda  
**Company:** Founder @ Spicyfy  
**Contact:** [GitHub Profile](https://github.com/vamsikandikonda)

## License

This project is open source and available under the [MIT License](LICENSE).

### MIT License Summary

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.**

## Legal Notice

PortPeek is provided as-is without any warranties. Users are responsible for compliance with their local laws and regulations regarding network monitoring tools. This software is intended for legitimate network administration and troubleshooting purposes only.

## Third-Party Dependencies

This project uses the following open-source libraries:

- **rumps** - BSD License - For macOS menu bar integration
- **PyInstaller** - GPL License - For application packaging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Disclaimer

This software is provided for educational and legitimate network administration purposes. Users must ensure they have proper authorization before monitoring network activities. The developer assumes no responsibility for misuse of this software.
