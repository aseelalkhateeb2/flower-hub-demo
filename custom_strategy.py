from typing import Iterable
from flwr.serverapp import Grid
from flwr.serverapp.strategy import FedAdagrad, Strategy
from flwr.app import ArrayRecord, ConfigRecord, Message, MessageType, RecordDict, MetricRecord

from typing import Iterable, Optional


class CustomStrategy(Strategy):

    nodes_metadata = []

    europe_countries = ["France", "Germany", "Ireland", "Italy", "Spain", "Switzerland"]

    policy = {
        2: "Full",
        1: "Restricted",
        0: "No-join",
    }

    def configure_train(self, server_round, arrays, config, grid):

        if server_round == 1:
            selected_ids = grid.get_node_ids()
        else:
            selected_ids = []
            for row in self.nodes_metadata:
                node_id = int(row["nodeid"])

                if not self.meets_app_requirements(row):
                    status = "No-join"
                else:
                    status = self.negotiate(row)

                print(
    f"NodeID: {row['nodeid']:<22} "
    f"Geography: {row.get('geography', '-'):<10} "
    f"Signature: {row.get('signature', '-'):<15} "
    f"Capacity: {row.get('capacity', '-'):<5} "
    f"-> {status}"
)

                if status != "No-join":
                    selected_ids.append(node_id)

        record = RecordDict({"arrays": arrays, "config": ConfigRecord({"round": server_round})})

        messages = []
        for node_id in selected_ids:
            message = Message(
                content=record,
                message_type=MessageType.TRAIN,
                dst_node_id=node_id,
            )
            messages.append(message)

        return messages

    def aggregate_train(self, server_round, replies):

        winner_node = None
        winner_value = 0

        node_rows = []

        for reply in replies:
            if reply.has_content():

                config = reply.content["config"]

                if server_round == 1:
                    row = {"nodeid": str(reply.metadata.src_node_id)}
                    for key, value in config.items():
                        row[str(key)] = str(value)
                    node_rows.append(row)

                else:
                    print(config["node_name"], config["random_value"])

                    if winner_node is None:
                        winner_node = config["node_name"]
                        winner_value = config["random_value"]
                    elif winner_value < config["random_value"]:
                        winner_node = config["node_name"]
                        winner_value = config["random_value"]

        if server_round == 1:
            self.nodes_metadata = node_rows
        else:
            print("Winner node:", winner_node)
            print("=======================================================")

        return (None, None)

    def configure_evaluate(self, server_round, arrays, config, grid):
        pass

    def aggregate_evaluate(self, server_round, replies):
        pass

    def summary(self):
        print("CustomStrategy: This is a custom strategy!")

    def meets_app_requirements(self, client):
        return int(client.get("capacity", 0)) > 30

    def negotiate(self, client):
        location_ok = client.get("geography") in self.europe_countries
        signature_ok = client.get("signature") == "trusted-party"

        matched = int(location_ok) + int(signature_ok)

        return self.policy[matched]