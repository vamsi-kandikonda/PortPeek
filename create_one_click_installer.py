#!/usr/bin/env python3
"""
Create a one-click installer package for PortPeek
Uses native macOS tools for a seamless installation experience
"""
import os
import shutil
import subprocess

def create_one_click_installer():
    """Create a one-click installer using native macOS tools"""
    
    # Create installer directory
    installer_name = "PortPeek-OneClick-Installer"
    if os.path.exists(installer_name):
        shutil.rmtree(installer_name)
    
    os.makedirs(installer_name)
    
    # Build the app using PyInstaller with the new lsof-based version
    print("Building PortPeek app...")
    result = subprocess.run([
        'pyinstaller', '--onefile', '--windowed', '--name=PortPeek',
        '--icon=icons/PortPeek.icns', '--add-data=icons:icons',
        'port_monitor_lsof.py'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ PyInstaller failed: {result.stderr}")
        return False
    
    # Copy the built app to the installer directory
    app_source = "dist/PortPeek.app"
    app_dest = os.path.join(installer_name, "PortPeek.app")
    
    if os.path.exists(app_source):
        if os.path.exists(app_dest):
            shutil.rmtree(app_dest)
        shutil.copytree(app_source, app_dest)
        print("✅ Copied PortPeek.app")
    else:
        print("❌ PortPeek.app not found")
        return False
    
    # Create a simple installer script that users can double-click
    installer_script = f'''#!/bin/bash
# PortPeek One-Click Installer
# Double-click this file to install PortPeek

SCRIPT_DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" &> /dev/null && pwd )"
INSTALL_DIR="/Applications"

# Function to show dialog
show_dialog() {{
    osascript -e "display dialog \\"$1\\" buttons {{\\"OK\\"}} default button \\"OK\\""
}}

# Function to show yes/no dialog
show_yes_no_dialog() {{
    osascript -e "display dialog \\"$1\\" buttons {{\\"No\\", \\"Yes\\"}} default button \\"Yes\\""
}}

# Welcome message
if ! show_yes_no_dialog "Welcome to PortPeek Installer!

PortPeek is a lightweight macOS status bar application that monitors active network ports.

This installer will:
• Install PortPeek to your Applications folder
• Set up permissions automatically
• Launch the application

Do you want to continue?"; then
    exit 0
fi

# Create Applications directory
mkdir -p "$INSTALL_DIR"

# Install PortPeek
echo "Installing PortPeek..."
if [ -d "$SCRIPT_DIR/PortPeek.app" ]; then
    # Remove existing installation
    if [ -d "$INSTALL_DIR/PortPeek.app" ]; then
        sudo rm -rf "$INSTALL_DIR/PortPeek.app"
    fi
    
    # Copy new version (with admin privileges for /Applications)
    sudo cp -R "$SCRIPT_DIR/PortPeek.app" "$INSTALL_DIR/"
    sudo chmod +x "$INSTALL_DIR/PortPeek.app/Contents/MacOS/PortPeek"
    sudo chown -R $(whoami):staff "$INSTALL_DIR/PortPeek.app"
    
    show_dialog "PortPeek has been installed successfully!

The app is now in your Applications folder."
    
    # Ask about permissions setup
    if show_yes_no_dialog "PortPeek needs Full Disk Access permission to monitor network ports.

Would you like to set this up now?

(You can also do this later from within the app)"; then
        # Open System Preferences
        osascript -e '
        tell application "System Preferences"
            activate
            set current pane to pane "com.apple.preference.security"
            delay 1
            tell application "System Events"
                tell process "System Preferences"
                    click button "Privacy" of tab group 1 of window 1
                    delay 0.5
                    select row 10 of table 1 of scroll area 1 of group 1 of tab group 1 of window 1
                    delay 0.5
                end tell
            end tell
        end tell
        '
        
        show_dialog "In System Preferences:

1. Click the lock icon and enter your password
2. Click the '+' button
3. Navigate to Applications and select PortPeek.app
4. Make sure the toggle next to PortPeek is ON

This is a one-time setup."
    fi
    
    # Ask to launch
    if show_yes_no_dialog "Installation complete!

Would you like to launch PortPeek now?"; then
        open "$INSTALL_DIR/PortPeek.app"
    fi
    
else
    show_dialog "Error: PortPeek.app not found in installer package.

Please download a fresh copy of the installer."
    exit 1
fi
'''
    
    # Write the installer script
    installer_script_path = f"{installer_name}/Install PortPeek.command"
    with open(installer_script_path, 'w') as f:
        f.write(installer_script)
    
    # Make it executable
    os.chmod(installer_script_path, 0o755)
    
    # Create a README for the installer
    readme_content = """# PortPeek One-Click Installer

## How to Install

Simply double-click "Install PortPeek.command" and follow the prompts.

The installer will:
1. Install PortPeek to your Applications folder
2. Guide you through permission setup
3. Launch the application

## What is PortPeek?

PortPeek is a lightweight macOS status bar application that monitors active network ports and displays the applications using them.

Features:
• Custom network icon in menu bar
• Real-time port monitoring
• Application detection
• Automated permission setup
• Minimal resource usage

## System Requirements

• macOS 10.13 or later
• No additional software required

## Troubleshooting

If you see "Permission denied" in the app menu:
1. Click "Grant Permission" in the app
2. Follow the guided setup in System Preferences

For other issues, try reinstalling by running the installer again.
"""
    
    with open(f"{installer_name}/README.txt", 'w') as f:
        f.write(readme_content)
    
    # Create a disk image for even easier distribution
    create_dmg(installer_name)
    
    print(f"✅ One-click installer created: {installer_name}/")
    print(f"✅ Users can double-click 'Install PortPeek.command' to install")
    print(f"✅ DMG file created for distribution")
    
    return True

def create_dmg(installer_dir):
    """Create a DMG file for easy distribution"""
    dmg_name = "PortPeek-Installer.dmg"
    
    # Remove existing DMG
    if os.path.exists(dmg_name):
        os.remove(dmg_name)
    
    try:
        # Create DMG
        subprocess.run([
            'hdiutil', 'create', 
            '-volname', 'PortPeek Installer',
            '-srcfolder', installer_dir,
            '-ov', '-format', 'UDZO',
            dmg_name
        ], check=True, capture_output=True)
        
        print(f"✅ Created {dmg_name}")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Could not create DMG: {e}")
        print("The installer folder is still available for distribution")

if __name__ == "__main__":
    create_one_click_installer()
