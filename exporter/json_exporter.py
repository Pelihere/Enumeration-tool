import json
import os
import time

class JSONExporter:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir

    def export(self, target, ports, results):
        os.makedirs(self.output_dir, exist_ok=True)

        report = {
            "target": target,
            "open_ports": ports,
            "results": results
        }

        filename = f"{target}_{int(time.time())}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

        return filepath