import socket
import sys

def get_hostname_IP():
    print("\nWebsite IP and Hostname Lookup")
    print("-" * 35)
    
    while True:
        hostname = input("\nEnter website address (or 'q' to quit): ").strip()
        
        if hostname.lower() == 'q':
            print("Goodbye!")
            break
        
        if not hostname:
            print("Please enter a valid hostname.")
            continue
        
        # Remove protocol if present
        hostname = hostname.replace('https://', '').replace('http://', '')
        hostname = hostname.split('/')[0]  # Remove path
        
        try:
            ip_address = socket.gethostbyname(hostname)
            print(f"\n{'Hostname:':<15} {hostname}")
            print(f"{'IP Address:':<15} {ip_address}")
            
            # Try to get all IPs (for load-balanced sites)
            try:
                addrinfo = socket.getaddrinfo(hostname, None)
                all_ips = set()
                for addr in addrinfo:
                    all_ips.add(addr[4][0])
                if len(all_ips) > 1:
                    print(f"{'All IPs:':<15} {', '.join(all_ips)}")
            except:
                pass
            
        except socket.gaierror:
            print(f"Error: Could not resolve '{hostname}'. Please check the spelling.")
        except Exception as e:
            print(f"Unexpected error: {e}")

def main():
    get_hostname_IP()

if __name__ == "__main__":
    main()