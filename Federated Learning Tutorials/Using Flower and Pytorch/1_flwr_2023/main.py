import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(config_path="conf", config_name="base", version_base=None)
def main(cfg: DictConfig):

    ## 1. Parse config & get experiment output dir
    print(OmegaConf.to_yaml(cfg))
    
    ## 2. Prepare your dataset

    ## 3. Define your clients

    ## 4. Define your strategy

    ## 5. Start Simulation

    ## 6. Save your results

if __name__ == '__main__':
    main()