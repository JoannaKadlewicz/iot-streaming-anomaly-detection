from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from domain.model.anomaly import Anomaly


class AnomalyEmailTemplate:
    def __init__(self):
        env = Environment(loader=FileSystemLoader("resources"))
        self.template = env.get_template("alert_email_template.html")

    def render(self, anomaly: Anomaly):
        return self.template.render(
            anomaly_id=anomaly.anomaly_id,
            account_id=anomaly.account_id,
            device_id=anomaly.device_id,
            metric=anomaly.metric,
            window_start=anomaly.window_start,
            window_end=anomaly.window_end,
            anomaly_reason=anomaly.anomaly_reason,
            generated_at=datetime.now(),
        )
