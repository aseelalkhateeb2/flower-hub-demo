# flower-hub-demo
Flower federated learning application

A demo Flower federated learning application implementing a custom node-selection and negotiation strategy on top of FedAdagrad/Strategy.

This project shows how to:

Configure a custom ServerApp strategy that filters and negotiates with clients based on metadata (geography, signature, capacity) reported in round 1.
Implement a ClientApp that reports node-specific configuration on the first round and randomized values on subsequent rounds.
Select a "winner" client each round based on reported metrics.
Project Structure
.
├── __init__.py            # Package marker
├── client_app.py          # Flower ClientApp: training logic run on each node
├── custom_strategy.py     # CustomStrategy: node selection, negotiation, aggregation
└── server_app.py          # Flower ServerApp: entry point that starts the strategy
How It Works
Round 1 — All available nodes are selected. Each client reports its geography, signature, and capacity back to the server.
Negotiation — For subsequent rounds, the server evaluates each node against:
meets_app_requirements: capacity must exceed a threshold.
negotiate: checks geography (must be in an approved list of European countries) and signature (must be "trusted-party") to assign a policy status (Full, Restricted, No-join).
Rounds 2+ — Only nodes that pass negotiation are re-selected. Each client returns a random value, and the server tracks the "winning" node with the highest value.
Requirements
Python 3.9+
flwr (Flower)
numpy

Install dependencies:

bash
pip install flwr numpy
Usage

Run the federated learning simulation using the Flower CLI (adjust according to your pyproject.toml / Flower app configuration):

bash
flwr run .

Note: This project assumes a Flower app package layout (e.g. quickstart_numpy). Make sure your pyproject.toml is configured with the correct [tool.flwr.app] entry points for server_app:app and client_app:app.

License

This project is open source, licensed under the MIT License.

Reproducibility

The full source code for this project is publicly available at: https://github.com/aseelalkhateeb2/flower-hub-demo
