import random

import numpy as np

from flwr.app import ArrayRecord, Context, Message, MetricRecord, RecordDict, ConfigRecord
from flwr.clientapp import ClientApp

app = ClientApp()


@app.train()
def train(msg: Message, context: Context):

    incoming_round = msg.content["config"]["round"]

    if incoming_round == 1:
        config = ConfigRecord({
            "geography": context.node_config["geography"],
            "signature": context.node_config["signature"],
            "capacity": str(context.node_config["capacity"]),
        })
    else:
        config = ConfigRecord({"random_value": random.randint(1, 10)})

    content = RecordDict({
        "arrays": msg.content["arrays"],
        "metrics": MetricRecord({"random_metric": np.random.rand(), "num-examples": 1}),
        "config": config,
    })

    return Message(content=content, reply_to=msg)