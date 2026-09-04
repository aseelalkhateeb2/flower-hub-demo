"""@flwrlabs/demo: A Flower Hub Demo app."""

import numpy as np
from flwr.app import ArrayRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg
from flwr.serverapp.strategy import FedAdagrad


from quickstart_numpy.custom_strategy import CustomStrategy

# Create ServerApp
app = ServerApp()


@app.main()
def main(grid: Grid, context: Context) -> None:
    """Main entry point for the ServerApp."""

    # Initialize strategy
    strategy = CustomStrategy()

    # Start strategy
    result = strategy.start(
        grid=grid,
        num_rounds=4,
        initial_arrays=ArrayRecord(None)
    )
