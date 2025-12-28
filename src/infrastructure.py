import random
from enum import Enum

class Status(Enum):
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"

class Service:
    def __init__(self, name, version="1.0"):
        self.name = name
        self.version = version
        self.status = Status.RUNNING
        self.uptime = 0

    def fail(self):
        """Simulate a failure."""
        self.status = Status.DOWN

    def degrade(self):
        """Simulate performance degradation."""
        self.status = Status.DEGRADED

    def recover(self):
        """Recover the service."""
        self.status = Status.RUNNING

    def __repr__(self):
        return f"Service({self.name}, {self.status.value})"

class Server:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.cpu_usage = 0
        self.memory_usage = 0
        self.services = []
        self.is_healing = False

    def add_service(self, service):
        self.services.append(service)

    def simulate_load(self):
        """Simulate random load fluctuation and potential failures."""
        self.cpu_usage = max(0, min(100, self.cpu_usage + random.randint(-10, 15)))
        self.memory_usage = max(0, min(100, self.memory_usage + random.randint(-5, 10)))

        # Random chaos: services might fail
        if random.random() < 0.05:  # 5% chance of severe failure
            if self.services:
                victim = random.choice(self.services)
                victim.fail()
        
        # High load can cause degradation
        if self.cpu_usage > 90:
             for service in self.services:
                 service.degrade()
