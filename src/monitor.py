from .infrastructure import Status

class Monitor:
    def __init__(self):
        self.alerts = []

    def scan(self, servers):
        """Scans the infrastructure for issues."""
        self.alerts = []
        for server in servers:
            # Check resource usage
            if server.cpu_usage > 90:
                self.alerts.append({
                    "type": "RESOURCE_HIGH",
                    "server": server,
                    "measure": "CPU",
                    "value": server.cpu_usage
                })
            
            if server.memory_usage > 90:
                self.alerts.append({
                    "type": "RESOURCE_HIGH",
                    "server": server,
                    "measure": "Memory",
                    "value": server.memory_usage
                })

            # Check service health
            for service in server.services:
                if service.status != Status.RUNNING:
                    self.alerts.append({
                        "type": "SERVICE_HEALTH",
                        "server": server,
                        "service": service,
                        "status": service.status
                    })
        return self.alerts
