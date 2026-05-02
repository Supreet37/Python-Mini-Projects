import psutil
import time
import sys
import os

def check_battery():
    """Check battery status and show notifications"""
    
    # Check if psutil is available
    try:
        import psutil
    except ImportError:
        print("❌ psutil module not installed!")
        print("Please run: pip install psutil")
        return
    
    # Check if battery exists
    battery = psutil.sensors_battery()
    if battery is None:
        print("❌ No battery found on this system!")
        print("This script is designed for laptops with batteries.")
        return
    
    print("\n" + "="*50)
    print("🔋 BATTERY MONITOR")
    print("="*50)
    print(f"✓ Battery detected! Monitoring started...")
    print("Press Ctrl+C to stop\n")
    
    notification_count = 0
    low_battery_notified = False
    high_battery_notified = False
    
    try:
        while True:
            # Get battery status
            battery = psutil.sensors_battery()
            percent = battery.percent
            plugged = battery.power_plugged
            
            # Clear screen occasionally (optional)
            # os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display current status
            if plugged:
                plug_icon = "🔌 CHARGING"
            else:
                plug_icon = "🔋 DISCHARGING"
            
            # Create visual battery bar
            bar_length = 30
            filled = int(bar_length * percent / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"\r[{bar}] {percent:3.0f}% {plug_icon}", end="", flush=True)
            
            # Check for low battery (below 20%)
            if percent < 20 and not plugged:
                if not low_battery_notified:
                    print("\n⚠️  WARNING: Battery is LOW! ({:.0f}%)".format(percent))
                    print("Please plug in your charger!")
                    
                    # Try to show system notification (Windows)
                    if os.name == 'nt':  # Windows
                        try:
                            from plyer import notification
                            notification.notify(
                                title="Low Battery Warning",
                                message=f"Battery is at {percent}%. Please plug in your charger.",
                                timeout=10
                            )
                        except:
                            pass
                    
                    low_battery_notified = True
                notification_count += 1
            else:
                low_battery_notified = False
            
            # Check for critical battery (below 10%)
            if percent < 10 and not plugged:
                print("\n🚨 CRITICAL: Battery is VERY LOW! ({:.0f}%)".format(percent))
                print("Plug in charger IMMEDIATELY!")
                if notification_count % 5 == 0:  # Repeat every 5th time
                    print("🔊 SOUND ALERT: Battery critical!")
            
            # Check for fully charged (above 90% while plugged)
            if percent > 90 and plugged:
                if not high_battery_notified:
                    print("\n✅ Battery is fully charged! ({:.0f}%)".format(percent))
                    print("You can unplug the charger to save battery life.")
                    high_battery_notified = True
            else:
                high_battery_notified = False
            
            # Wait before next check (30 seconds)
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*50)
        print(" Battery monitor stopped!")
        print("="*50)
        print(f"Total notifications shown: {notification_count}")
        
        # Show final battery status
        battery = psutil.sensors_battery()
        print(f"\nFinal battery status: {battery.percent}%")
        if battery.power_plugged:
            print("Status: Connected to power")
        else:
            remaining = battery.secsleft
            if remaining != -1:
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                print(f"Estimated time remaining: {hours}h {minutes}m")
            else:
                print("Status: Running on battery")

def show_battery_info():
    """Display detailed battery information"""
    battery = psutil.sensors_battery()
    
    if battery is None:
        print("No battery detected!")
        return
    
    print("\n" + "="*50)
    print("🔋 BATTERY INFORMATION")
    print("="*50)
    print(f"Battery Percentage: {battery.percent}%")
    print(f"Power Plugged: {'Yes' if battery.power_plugged else 'No'}")
    
    if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
        if battery.secsleft != psutil.POWER_TIME_UNKNOWN:
            hours = battery.secsleft // 3600
            minutes = (battery.secsleft % 3600) // 60
            print(f"Time Remaining: {hours}h {minutes}m")
        else:
            print("Time Remaining: Unknown")
    else:
        print("Time Remaining: Unlimited (plugged in)")
    
    print("="*50)

if __name__ == "__main__":
    try:
        # First show battery info
        show_battery_info()
        
        # Ask user if they want to monitor
        print("\nOptions:")
        print("1. Monitor battery continuously")
        print("2. Just show current status and exit")
        
        choice = input("\nChoose (1 or 2): ").strip()
        
        if choice == '1':
            check_battery()
        else:
            print("\n✓ Battery check complete!")
            
    except KeyboardInterrupt:
        print("\n\n Goodbye!")
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure psutil is installed: pip install psutil")
        print("2. This script works only on laptops with batteries")
        print("3. Run with appropriate permissions")