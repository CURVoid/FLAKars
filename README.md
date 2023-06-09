# FLAKars v0.1.3 | etherium network arbitrage bot
## Changelog
- Config files structure update
- Arbitrage bug fixes
## Technologies (Libraries)
- <a href="https://aave.com">flashloans</a>
- <a href="https://uniswap.org">uniswap v2 | v3 interfaces</a>
## Usage
- `python scripts/publish.py <config.json>` - deploys arbitrage contract and prints it address
- `python scripts/bot.py <config.json> <your-contract-address>` - runs deployed arbitrage contract
## Example config file
```json
{
    "LPA": "0xC911B590248d127aD18546B186cC6B324e99F02c",
    "node": "https://goerli.infura.io/v3/<your-infura-token>",
    "abi": "build/FLAKars.abi",
    "bytecode": "build/FLAKars.bin",
    "private_key": "<your-wallet-sk>",
    "weth": "wETH",
    "eth-dex": "uniswap v2",
    "routers": [
        {
            "dex": "uniswap v3",
            "address": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
            "estim": "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6",
            "avail": "0x1F98431c8aD98523631AE4a59f267346ea31F984"
        },
        { "dex": "uniswap v2", "address": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D" },
        { "dex": "sushiswap", "address": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506" },
        { "dex": "pancakeswap v2", "address": "0xeff92a263d31888d860bd50809a8d171709b7b1c" },
        {
            "dex": "pancakeswap v3",
            "address": "0x1b81D678ffb9C0263b24A97847620C99d213eB14",
            "estim": "0xbC203d7f83677c7ed3F7acEc959963E7F4ECC5C2",
            "avail": "0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865"
        }
    ],
    "fl": [
        "USDC aave",
        "wETH aave",
        "wBTC aave",
        "DAI aave",
        "USDT aave",
        "LINK aave"
    ],
    "tokens": [
        { "symbol": "USDC", "address": "0x07865c6e87b9f70255377e024ace6630c1eaa37f" },
        { "symbol": "wETH", "address": "0xb4fbf271143f4fbf7b91a5ded31805e42b2208d6" },
        { "symbol": "wBTC", "address": "0xc04b0d3107736c32e19f1c62b2af67be61d63a05" },
        { "symbol": "DAI", "address": "0xdc31Ee1784292379Fbb2964b3B9C4124D8F89C60" },
        { "symbol": "USDT", "address": "0xc2c527c0cacf457746bd31b2a698fe89de2b6d49" },
        { "symbol": "LINK", "address": "0x326C977E6efc84E512bB9C30f76E30c160eD06FB" },
        { "symbol": "UNI", "address": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984" },
        { "symbol": "USDC aave", "address": "0x65aFADD39029741B3b8f0756952C74678c9cEC93" },
        { "symbol": "wETH aave", "address": "0xCCB14936C2E000ED8393A571D15A2672537838Ad" },
        { "symbol": "wBTC aave", "address": "0x45AC379F019E48ca5dAC02E54F406F99F5088099" },
        { "symbol": "DAI aave", "address": "0xBa8DCeD3512925e52FE67b1b5329187589072A55" },
        { "symbol": "USDT aave", "address": "0x2E8D98fd126a32362F2Bd8aA427E59a1ec63F780" },
        { "symbol": "LINK aave", "address": "0xe9c4393a23246293a8D31BF7ab68c17d4CF90A29" }
    ]
}
``` 