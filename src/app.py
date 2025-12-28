import time
import random
import os
import sys
from colorama import init, Fore, Style
from .infrastructure import Server, Service, Status
from .monitor import Monitor
from .healer import Healer

# Initialize colorama
init(autoreset=True)

class Simulator:
    def __init__(self):
        self.monitor = Monitor()
        self.healer = Healer()
        self.servers = []
        self._setup_infrastructure()

    def _setup_infrastructure(self):
        """Initializes the simulation environment."""
        names = ["Alpha", "Beta", "Gamma", "Delta"]
        for i, name in enumerate(names):
            server = Server(f"Server-{name}", f"192.168.1.{10+i}")
            # Add some services
            server.add_service(Service("Web-Server", "nginx"))
            server.add_service(Service("Database", "postgres"))
            if i % 2 == 0:
                 server.add_service(Service("Cache", "redis"))
            self.servers.append(server)

    def run(self, cycles=100, delay=1.0):
        print(Fore.CYAN + Style.BRIGHT + "Initializing Self-Healing Infrastructure Simulator...")
        time.sleep(1)
        
        try:
            for cycle in range(cycles):
                self._clear_screen()
                print(Fore.YELLOW + f"--- Cycle {cycle+1}/{cycles} ---")
                
                # 1. Update Infrastructure State (Simulate Load/Chaos)
                for server in self.servers:
                    server.simulate_load()

                # 2. Monitor
                alerts = self.monitor.scan(self.servers)
                
                # 3. Heal
                healing_actions = []
                for alert in alerts:
                    action = self.healer.heal(alert)
                    if action:
                        healing_actions.append(action)

                # 4. Visualization
                self._print_dashboard(alerts, healing_actions)
                
                time.sleep(delay)

        except KeyboardInterrupt:
            print(Fore.RED + "\nSimulation stopped by user.")

    def _print_dashboard(self, alerts, healing_actions):
        print("\n" + Fore.WHITE + Style.BRIGHT + f"{'SERVER':<15} {'IP':<15} {'CPU':<8} {'MEM':<8} {'SERVICES':<30}")
        print("-" * 80)
        
        for server in self.servers:
            cpu_color = Fore.GREEN if server.cpu_usage < 70 else (Fore.YELLOW if server.cpu_usage < 90 else Fore.RED)
            mem_color = Fore.GREEN if server.memory_usage < 70 else (Fore.YELLOW if server.memory_usage < 90 else Fore.RED)
            
            services_status = []
            for s in server.services:
                color = Fore.GREEN if s.status == Status.RUNNING else (Fore.YELLOW if s.status == Status.DEGRADED else Fore.RED)
                services_status.append(color + s.name[0]) # First letter only for compactness

            print(f"{Fore.WHITE}{server.name:<15} {server.ip:<15} {cpu_color}{server.cpu_usage}%{Fore.RESET}    {mem_color}{server.memory_usage}%{Fore.RESET}    {' '.join(services_status)}")

        if alerts:
            print(Fore.RED + "\n[!] ALERTS DETECTED:")
            for alert in alerts:
                target = alert.get('server').name
                if 'service' in alert:
                    msg = f"Service {alert['service'].name} on {target} is {alert['status'].value}"
                else:
                    msg = f"High {alert['measure']} on {target}: {alert['value']}%"
                print(f" - {msg}")

        if healing_actions:
            print(Fore.GREEN + Style.BRIGHT + "\n[+] HEALING ACTIONS:")
            for action in healing_actions:
                print(f" -> {action}")

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    sim = Simulator()
    # Check for test mode arg
    if "--test-mode" in sys.argv:
        sim.run(cycles=10, delay=0.1)
    else:
        sim.run(cycles=9999, delay=2.0)
