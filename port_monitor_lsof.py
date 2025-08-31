import rumps
import subprocess
import re
import os


class PortPeekApp(rumps.App):
    """
    A macOS status bar application that monitors active network ports using lsof.
    This version bypasses psutil permission issues by using system commands.
    """
    def __init__(self):
        # Initialize the app with a title and custom icon.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icons", "menu_icon.png")
        
        # Try to use custom icon, fallback to emoji if not found
        if os.path.exists(icon_path):
            super(PortPeekApp, self).__init__("PortPeek", icon=icon_path)
        else:
            super(PortPeekApp, self).__init__("🔍")
        
        # Add the initial menu items.
        self.menu = ["Refresh"]
        self.refresh_ports(None)

    @rumps.clicked("Refresh")
    def refresh_ports(self, _):
        """
        Refreshes the list of ports and applications in the menu using lsof.
        """
        # Clear existing menu items and add the "Refresh" button back.
        self.menu.clear()
        self.menu.add("Refresh")
        self.menu.add(rumps.separator)

        try:
            # Use lsof to get network connections
            result = subprocess.run(['lsof', '-i', '-n', '-P'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                self.menu.add("Unable to access network info")
                self.menu.add("Try running with admin privileges")
                return
            
            # Parse lsof output
            lines = result.stdout.strip().split('\n')
            ports_info = {}
            
            for line in lines[1:]:  # Skip header
                parts = line.split()
                if len(parts) >= 9:
                    command = parts[0]
                    pid = parts[1]
                    name_part = parts[8]
                    
                    # Extract port from formats like "*:8080" or "localhost:3000"
                    if ':' in name_part and ('LISTEN' in line or 'ESTABLISHED' in line):
                        try:
                            port_match = re.search(r':(\d+)', name_part)
                            if port_match:
                                port = int(port_match.group(1))
                                status = 'LISTEN' if 'LISTEN' in line else 'ESTABLISHED'
                                
                                # Store unique port info
                                if port not in ports_info:
                                    ports_info[port] = {
                                        'command': command,
                                        'pid': pid,
                                        'status': status
                                    }
                        except (ValueError, IndexError):
                            continue
            
            # Add ports to menu
            if ports_info:
                # Sort ports numerically
                for port in sorted(ports_info.keys()):
                    info = ports_info[port]
                    status_icon = "🟢" if info['status'] == 'LISTEN' else "🔵"
                    self.menu.add(f"{status_icon} Port {port}: {info['command']}")
            else:
                self.menu.add("No active network connections found")
                
        except subprocess.TimeoutExpired:
            self.menu.add("Network scan timed out")
        except subprocess.CalledProcessError as e:
            self.menu.add(f"Error accessing network info: {e}")
        except Exception as e:
            self.menu.add(f"Unexpected error: {str(e)}")
        
        # Add help menu
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("About PortPeek", callback=self.show_about))

    def show_about(self, _):
        """
        Show about dialog
        """
        applescript = '''
        display dialog "PortPeek - Network Port Monitor

A lightweight macOS menu bar app that shows active network ports and the applications using them.

🟢 = Listening ports
🔵 = Established connections

Version: 2.0
Developed by Vamsi Kandikonda
Founder @ Spicyfy

Open Source • MIT License
No special permissions required!" buttons {"OK"} default button "OK"
        '''
        try:
            subprocess.run(['osascript', '-e', applescript])
        except:
            pass


if __name__ == "__main__":
    PortPeekApp().run()
