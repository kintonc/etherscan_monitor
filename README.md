# Etherscan wallet monitor

Simple tool to monitor Ethereum wallets for new transactions. Uses [Etherscan](https://etherscan.io).

Script checks for new transactions every 60 secs (this can be changed easily).

To use:

1. Download repo
2. Go to [etherscan.org and get your API key](https://etherscan.io/apis)
3. Go to `config_sample.yaml`, and add [1] your API key and [2] the address and a name (used for identifying addresses) for the wallets you want to monitor.
4. Rename `config_sample.yaml` to `config.yaml`
5. Run `monitor.py`. Script will continuously monitor until it is quit.