# Etherscan and AVAX Snowtrace wallet monitor

Simple tool to monitor Ethereum and Avalanche wallets for new transactions. Uses [Etherscan](https://etherscan.io) and [Snowtrace](https://snowtrace.io). Can be easily extended to support Fantom ([FTMScan](https://ftmscan.com)), Binance ([BSCScan](https://bscscan.com)), Polygon ([Polygonscan](https://polygonscan.com)), Arbitrum([Arbiscan](https://arbiscan.io)), Moonriver ([Moonscan](https://moonriver.moonscan.io)), and more chains.

Script checks for new transactions every 60 secs (this can be changed easily by setting the `CHECK_FREQUENCY_SECONDS` variable).

To use:

1. Download repo. Install playsound v 1.2.2 python library (`pip install playsound==1.2.2`)  
2. Go to [etherscan.io](https://etherscan.io/apis) and [snowtrace.io](https://snowtrace.io/apis), and get your API key]
3. Go to `config_sample.yaml`, and add [1] your API keys and [2] for every wallet you want to monitor, enter the address, a name (used for identifying addresses), and the blockchain `networks` you want to monitor transactions for this wallet.
4. Rename `config_sample.yaml` to `config.yaml`
5. Run `monitor.py`. Script will continuously monitor until it is quit.

Acceptable network parameters (`network`) for YAML file:
* the network value must be a comma-separated array 
  * Example 1: `['eth', 'avax']`
  * Example 2: `['eth']`
* Can be one or more of `eth`, `avax`