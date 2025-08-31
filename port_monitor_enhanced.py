import rumps
import psutil
import os
import subprocess


class PortMonitorApp(rumps.App):
    """
    A macOS status bar application that monitors active network ports.
    Enhanced version with automated permission handling for distribution.
    """
    def __init__(self):
        # Initialize the app with a title and custom icon.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icons", "menu_icon.png")
        if os.path.exists(icon_path):
            super(PortMonitorApp, self).__init__("Port Monitor", icon=icon_path)
        else:
            super(PortMonitorApp, self).__init__("Port Monitor", title="🔌")
        
        # Set up the initial menu with a "Refresh" button.
        self.menu = ["Refresh"]
        self.refresh_ports(None) # Call refresh on startup to populate the menu

    @rumps.clicked("Refresh")
    def refresh_ports(self, _):
        """
        Refreshes the list of ports and applications in the menu.
        """
        # Clear existing menu items and add the "Refresh" button back.
        self.menu.clear()
        self.menu.add("Refresh")
        self.menu.add(rumps.separator)

        # Always use the force refresh method to bypass permission issues
        self.force_refresh_internal()

    def open_settings(self, _):
        """
        Open System Preferences to Privacy settings with user guidance
        """
        try:
            # Show user-friendly dialog first
            applescript = '''
            display dialog "PortPeek will now open System Preferences.

Please follow these steps:
1. Click the lock icon and enter your password
2. Click the '+' button
3. Find and select PortPeek.app
4. Make sure the toggle is ON

This is a one-time setup." buttons {"Cancel", "Open Settings"} default button "Open Settings"
            
            if button returned of result is "Open Settings" then
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
            end if
            '''
            subprocess.run(['osascript', '-e', applescript])
        except:
            # Fallback to opening System Preferences normally
            subprocess.run(['open', '/System/Library/PreferencePanes/Security.prefPane'])

    def show_help(self, _):
        """
        Show help dialog for permission setup
        """
        applescript = '''
        display dialog "PortPeek Permission Setup Help

PortPeek needs Full Disk Access to monitor network ports and show which applications are using them.

To grant permission:
1. Go to System Preferences > Security & Privacy
2. Click Privacy tab
3. Select 'Full Disk Access' from the left
4. Click the lock and enter your password
5. Click '+' and select PortPeek.app
6. Make sure the toggle is ON

This is required only once." buttons {"OK"} default button "OK"
        '''
        subprocess.run(['osascript', '-e', applescript])


    def test_specific_permission(self):
        """
        Test if we can actually access network connections with a smaller scope
        """
        try:
            # Try to get just listening connections (less restrictive)
            connections = psutil.net_connections(kind='inet')
            return len(connections) > 0
        except:
            return False

    def refresh_ports_fallback(self):
        """
        Fallback method to show ports without process names if needed
        """
        try:
            connections = psutil.net_connections(kind='inet')
            ports_list = set()
            
            for conn in connections:
                if conn.status in ["LISTEN", "ESTABLISHED"] and conn.laddr:
                    if conn.laddr.port not in ports_list:
                        self.menu.add(f"Port {conn.laddr.port}: Active")
                        ports_list.add(conn.laddr.port)
                        
            if not ports_list:
                self.menu.add("No active connections found")
        except:
            self.menu.add("Unable to access network info")

    def force_refresh_internal(self):
        """
        Internal force refresh method that bypasses all permission checks
        """
        try:
            # Try basic network info first
            connections = psutil.net_connections(kind='inet')
            ports_found = False
            ports_list = set()
            
            for conn in connections:
                if conn.status in ["LISTEN", "ESTABLISHED"] and conn.laddr:
                    if conn.laddr.port not in ports_list:
                        ports_found = True
                        try:
                            # Try to get process name
                            if conn.pid:
                                p = psutil.Process(conn.pid)
                                app_name = p.name()
                            else:
                                app_name = "System"
                            self.menu.add(f"Port {conn.laddr.port}: {app_name}")
                        except:
                            # Fallback to just showing the port
                            self.menu.add(f"Port {conn.laddr.port}: Active")
                        ports_list.add(conn.laddr.port)
            
            if not ports_found:
                self.menu.add("No active connections found")
                
        except Exception as e:
            self.menu.add("Network access limited")
            self.menu.add("Check Full Disk Access setting")

    def force_refresh(self, _):
        """
        Force refresh bypassing permission checks (menu callback)
        """
        self.menu.clear()
        self.menu.add("Refresh")
        self.menu.add(rumps.separator)
        self.force_refresh_internal()


if __name__ == "__main__":
    PortMonitorApp().run()
