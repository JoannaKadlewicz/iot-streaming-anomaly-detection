from datetime import datetime

import numpy as np

rng = np.random.default_rng(42)

def sensor_stream(sensor_id: str, temperature_unit: str = "C"):
    baseline = 21.0
    prev_temp = baseline
    spike_value = 0.0

    while True:
        now = datetime.now()

        second_of_day = now.hour * 3600 + now.minute * 60 + now.second
        daily_cycle = 2.5 * np.sin(2 * np.pi * second_of_day / 86400 - np.pi / 2)
        noise = rng.normal(0, 0.08)

        target = baseline + daily_cycle
        temp = 0.96 * prev_temp + 0.04 * target + noise

        if spike_value <= 0.1 and rng.random() < 0.0001:
            spike_value = rng.uniform(4, 8)

        temp += spike_value

        if spike_value > 0:
            spike_value *= 0.75

        prev_temp = temp


        yield {
            "sensor_id": sensor_id,
            "event_ts": now.isoformat(),
            "temperature_c": round(temp, 2)
        }
