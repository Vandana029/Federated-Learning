import hydra
from omegaconf import DictConfig, OmegaConf

import flwr as fl

from client import generate_client_fn
from dataset import prepare_dataset
from server import get_on_fit_config, get_evaluate_fn


# A decorator for Hydra. This tells hydra to by default load the config in conf/base.yaml
@hydra.main(config_path="conf", config_name="base", version_base=None)
def main(cfg: DictConfig):

    ## 1. Parse config & get experiment output dir
    print(OmegaConf.to_yaml(cfg))
    
    ## 2. Prepare your dataset
    trainloaders, validationloaders, testloader = prepare_dataset(
        cfg.num_clients, cfg.batch_size
    )

    print(len(trainloaders), len(trainloaders[0].dataset))

    ## 3. Define your clients
    client_fn = generate_client_fn(trainloaders, validationloaders, cfg.num_classes)

    ## 4. Define your strategy
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=0.0,  # in simulation, since all clients are available at all times, we can just use `min_fit_clients` to control exactly how many clients we want to involve during fit
        min_fit_clients=cfg.num_clients_per_round_fit,  # number of clients to sample for fit()
        fraction_evaluate=0.0,  # similar to fraction_fit, we don't need to use this argument.
        min_evaluate_clients=cfg.num_clients_per_round_eval,  # number of clients to sample for evaluate()
        min_available_clients=cfg.num_clients,  # total clients in the simulation
        on_fit_config_fn=get_on_fit_config(
            cfg.config_fit
        ),  # a function to execute to obtain the configuration to send to the clients during fit()
        evaluate_fn=get_evaluate_fn(cfg.num_classes, testloader),
    )  # a function to run on the server side to evaluate the global model.

    ## 5. Start Simulation

    ## 6. Save your results

if __name__ == '__main__':
    main()