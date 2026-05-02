import subprocess
import platform
import sys

def get_wifi_passwords_windows():
    """Get saved WiFi passwords on Windows"""
    try:
        # Get all WiFi profiles
        profiles_data = subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"],
            shell=True,
            stderr=subprocess.DEVNULL
        ).decode("utf-8", errors="ignore").split("\n")
        
        profiles = []
        for line in profiles_data:
            if "All User Profile" in line:
                profile = line.split(":")[1].strip()
                profiles.append(profile)
        
        if not profiles:
            print("No WiFi profiles found")
            return []
        
        wifi_list = []
        
        for profile in profiles:
            try:
                # Get password for each profile
                results = subprocess.check_output(
                    ["netsh", "wlan", "show", "profile", profile, "key=clear"],
                    shell=True,
                    stderr=subprocess.DEVNULL
                ).decode("utf-8", errors="ignore").split("\n")
                
                password = None
                for line in results:
                    if "Key Content" in line:
                        password = line.split(":")[1].strip()
                        break
                
                wifi_list.append({
                    'SSID': profile,
                    'Password': password if password else "No password (Open network)"
                })
            except subprocess.CalledProcessError:
                wifi_list.append({
                    'SSID': profile,
                    'Password': "Access denied (Run as Administrator)"
                })
        
        return wifi_list
        
    except subprocess.CalledProcessError:
        print("Error: Unable to access WiFi profiles. Run as Administrator.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_wifi_passwords_mac():
    """Get saved WiFi passwords on macOS"""
    try:
        # Get WiFi profiles list
        profiles = subprocess.check_output(
            ["security", "find-generic-password", "-wa", "AirPort"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8").split("\n")
        
        # This is simplified - macOS needs keychain access
        print("macOS support requires keychain access")
        return []
    except:
        print("Unable to access WiFi passwords on macOS")
        return []

def get_wifi_passwords_linux():
    """Get saved WiFi passwords on Linux"""
    try:
        # Check if NetworkManager is used
        result = subprocess.check_output(
            ["nmcli", "connection", "show"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8").split("\n")
        
        wifi_list = []
        for line in result[1:]:  # Skip header
            if line.strip():
                parts = line.split()
                if len(parts) > 0:
                    ssid = parts[0]
                    try:
                        password_data = subprocess.check_output(
                            ["nmcli", "-s", "connection", "show", ssid],
                            stderr=subprocess.DEVNULL
                        ).decode("utf-8")
                        
                        password = None
                        for pwd_line in password_data.split("\n"):
                            if "802-11-wireless-security.psk:" in pwd_line:
                                password = pwd_line.split(":")[1].strip()
                                break
                        
                        wifi_list.append({'SSID': ssid, 'Password': password or "Not found"})
                    except:
                        wifi_list.append({'SSID': ssid, 'Password': "Access denied"})
        
        return wifi_list
    except:
        print("NetworkManager not found or not configured")
        return []

def save_to_file(wifi_list, filename="wifi_passwords.txt"):
    """Save WiFi passwords to file"""
    if not wifi_list:
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("SAVED WIFI NETWORKS AND PASSWORDS\n")
        f.write("="*60 + "\n\n")
        
        for wifi in wifi_list:
            f.write(f"SSID: {wifi['SSID']}\n")
            f.write(f"Password: {wifi['Password']}\n")
            f.write("-"*40 + "\n")
    
    print(f"\n✓ Saved to {filename}")

def main():
    print("\n" + "="*50)
    print("WIFI PASSWORD RETRIEVER")
    print("="*50)
    print("\nNote: Run as Administrator/root for best results\n")
    
    system = platform.system()
    
    if system == "Windows":
        wifi_list = get_wifi_passwords_windows()
    elif system == "Darwin":  # macOS
        wifi_list = get_wifi_passwords_mac()
    elif system == "Linux":
        wifi_list = get_wifi_passwords_linux()
    else:
        print(f"Unsupported operating system: {system}")
        return
    
    if not wifi_list:
        print("No WiFi passwords found or insufficient permissions")
        return
    
    # Display in console
    print("\n" + "="*60)
    print(f"{'SSID':<30} | {'PASSWORD':<25}")
    print("="*60)
    
    for wifi in wifi_list:
        password = wifi['Password'] if wifi['Password'] else "(No password)"
        print(f"{wifi['SSID']:<30} | {password:<25}")
    
    print("="*60)
    
    # Ask to save to file
    save_choice = input("\nSave to file? (y/n): ").lower()
    if save_choice == 'y':
        save_to_file(wifi_list)
    
    print(f"\n✓ Found {len(wifi_list)} saved WiFi networks")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
        sys.exit(0)