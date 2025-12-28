import time
from .infrastructure import Status

class Healer:
    def __init__(self):
        self.action_log = []

    def heal(self, alert):
        """Takes action based on the alert."""
        issue_type = alert["type"]
        server = alert["server"]

        if server.is_healing:
            return  # Monitor already caught this, healing in progress

        server.is_healing = True
        
        if issue_type == "SERVICE_HEALTH":
            service = alert["service"]
            action = f"Restarting service {service.name} on {server.name}"
            self._log_action(action)
            # Simulate restart time
            service.recover()
            server.is_healing = False
            return action

        elif issue_type == "RESOURCE_HIGH":
            measure = alert["measure"]
            action = f"Scaling up resources for {server.name} due to high {measure}"
            self._log_action(action)
            # Simulate cooling down
            if measure == "CPU":
                server.cpu_usage -= 30
            elif measure == "Memory":
                server.memory_usage -= 20
            server.is_healing = False
            return action

    def _log_action(self, action):
        timestamp = time.strftime("%H:%M:%S")
        self.action_log.append(f"[{timestamp}] {action}")
