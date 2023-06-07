from contract.functions import *
from arbitrage import *
from arbmath import *
from colors import *
from typing import *
from consts import *
from discord.ext.commands import Bot
from discord import Intents
import asyncio
import json
import sys

def usage(args):
    space = " "*len(args[0])
    print("USAGE: ")
    print(f"{args[0]} config.json 0x2B9F1873d99B3C6322b34e978699c7313C348d30")
    print(f"{space  } ^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(f"{space  } path to configuration file            contract address")

if len(sys.argv) < 3:
    usage(sys.argv)
    sys.exit(-1)

async def get_most_profitable_trib(fl, tokens, routers, eth_token, eth_router, on_success, *args) -> List[Tuple[TribArbitrage, Pair]]:
    eth_router, eth_estim, eth_avail = eth_router
    arbitrages = []
    for fl_token in fl:
        eth_pair = Pair(contract, account.address, eth_router, eth_token, fl_token, estim=eth_estim, avail=eth_avail)
        if fl_token != eth_token and not eth_pair.available():
            print(
                COLOR_YELLOW +
                f"{weth} -> "
                + f"{get_sym_by_addr(fl_token)} does not exists on {get_dex_by_addr(router1)}"
                + COLOR_RESET
            )
            continue
        for token2 in tokens:
            for token3 in tokens:
                if fl_token == token2 and token2 == token3:
                    continue
                
                for router1, estim1, avail1 in routers:
                    pair1 = Pair(contract, account.address, router1, fl_token, token2, estim=estim1, avail=avail1)

                    if fl_token != token2 and not pair1.available():
                        print(
                            COLOR_YELLOW +
                            f"{get_sym_by_addr(fl_token)} -> "
                            + f"{get_sym_by_addr(token2)} does not exists on {get_dex_by_addr(router1)}"
                            + COLOR_RESET
                        )
                        continue

                    for router2, estim2, avail2 in routers:
                        pair2 = Pair(contract, account.address, router2, token2, token3, estim=estim2, avail=avail2)

                        if token2 != token3 and not pair2.available():
                            print(
                                COLOR_YELLOW +
                                f"{get_sym_by_addr(token2)} -> "
                                + f"{get_sym_by_addr(token3)} does not exists on {get_dex_by_addr(router2)}"
                                + COLOR_RESET
                            )
                            continue

                        for router3, estim3, avail3 in routers:
                            pair3 = Pair(contract, account.address, router3, token3, fl_token, estim=estim3, avail=avail3)
                            
                            if token3 != fl_token and not pair3.available():
                                print(
                                    COLOR_YELLOW +
                                    f"{get_sym_by_addr(token3)} -> "
                                    + f"{get_sym_by_addr(fl_token)} does not exists on {get_dex_by_addr(router3)}"
                                    + COLOR_RESET
                                )
                                continue

                            arbitrage = TribArbitrage(
                                web3,
                                contract,
                                account,
                                pair1,
                                pair2,
                                pair3
                            )
                            amount, estimated_amount, estimated_gas, succed, error = estimateGasAndAmount(web3, arbitrage, eth_pair)
                            if not succed:
                                print(
                                    COLOR_RED +
                                    f"{arbitrage.debug(get_sym_by_addr, get_dex_by_addr)} failed with {error}"
                                    + COLOR_RESET
                                )
                                continue

                            print(f"found {amount}/{estimated_amount}({estimated_amount/amount}) {arbitrage.debug(get_sym_by_addr, get_dex_by_addr)}")

                            try:
                                arbitrage.flashArbitrage(amount, gas_limit=estimated_gas)
                            except Exception as e:
                                print(COLOR_RED + f"arbitrage failed with {e}" + COLOR_RESET)
                            else:
                                await on_success(arbitrage, amount, *args)
                            arbitrages.append((arbitrage, eth_pair))
                                       
    return arbitrages

async def get_most_profitable_dual(fl, tokens, routers, eth_token, eth_router, on_success, *args) -> List[Tuple[DualArbitrage, Pair]]:
    eth_router, eth_estim, eth_avail = eth_router
    arbitrages = []
    for fl_token in fl:
        eth_pair = Pair(contract, account.address, eth_router, eth_token, fl_token, estim=eth_estim, avail=eth_avail)
        if fl_token != eth_token and not eth_pair.available():
            print(
                COLOR_YELLOW +
                f"{weth} -> "
                + f"{get_sym_by_addr(fl_token)} does not exists on {get_dex_by_addr(router1)}"
                + COLOR_RESET
            )
            continue
        for token2 in tokens:
            if fl_token == token2:
                continue

            for router1, estim1, avail1 in routers:
                pair1 = Pair(contract, account.address, router1, fl_token, token2, estim=estim1, avail=avail1)
                eth_pair = Pair(contract, account.address, router1, eth_token, fl_token, estim=estim1, avail=avail1)
                if fl_token != eth_token and not eth_pair.available():
                    print(
                        COLOR_YELLOW +
                        f"{get_sym_by_addr(eth_token)} -> "
                        + f"{get_sym_by_addr(fl_token)} does not exists on {get_dex_by_addr(router1)}"
                        + COLOR_RESET
                    )
                    continue

                if not pair1.available():
                    print(
                        COLOR_YELLOW +
                        f"{get_sym_by_addr(fl_token)} -> "
                        + f"{get_sym_by_addr(token2)} does not exists on {get_dex_by_addr(router1)}"
                        + COLOR_RESET
                    )
                    continue

                for router2, estim2, avail2 in routers:
                    pair2 = Pair(contract, account.address, router2, token2, fl_token, estim=estim2, avail=avail2)

                    if not pair2.available():
                        print(
                            COLOR_YELLOW +
                            f"{get_sym_by_addr(token2)} -> "
                            + f"{get_sym_by_addr(fl_token)} does not exists on {get_dex_by_addr(router2)}"
                            + COLOR_RESET
                        )
                        continue

                    arbitrage = DualArbitrage(
                        web3,
                        contract,
                        account,
                        pair1,
                        pair2
                    )

                    amount, estimated_amount, estimated_gas, succed, error = estimateGasAndAmount(web3, arbitrage, eth_pair)
                    if not succed:
                        print(
                            COLOR_RED +
                            f"{arbitrage.debug(get_sym_by_addr, get_dex_by_addr)} failed with {error}"
                            + COLOR_RESET
                        )
                        continue

                    print(f"found {amount}/{estimated_amount}({estimated_amount/amount}) {arbitrage.debug(get_sym_by_addr, get_dex_by_addr)}")

                    try:
                        arbitrage.flashArbitrage(amount, gas_limit=estimated_gas)
                    except Exception as e:
                        print(COLOR_RED + f"arbitrage failed with {e}" + COLOR_RESET)
                    else:
                        await on_success(arbitrage, amount, *args)
                    arbitrages.append((arbitrage, eth_pair))
                                    
    return arbitrages

async def arbitrage_while_profitable(arbitrages: List[Tuple[DualArbitrage | TribArbitrage, Pair]], on_success, *args):
    while len(arbitrages) != 0:
        i = 0
        while i<len(arbitrages):
            arbitrage = arbitrages[i][0]
            eth_pair = arbitrages[i][1]

            amount, estimated_amount, estimated_gas, succed, error = estimateGasAndAmount(web3, arbitrage, eth_pair)
            if not succed:
                print(
                    COLOR_RED +
                    f"{arbitrage.debug(get_sym_by_addr, get_dex_by_addr)} failed with {error}"
                    + COLOR_RESET
                )
                arbitrages.pop(i)
                continue

            print(
                f"found {amount}/{estimated_amount}({estimated_amount/amount}) {arbitrage.debug(get_sym_by_addr, get_dex_by_addr)}"
            )

            try:
                arbitrage.flashArbitrage(amount, gas_limit=estimated_gas)
            except Exception as e:
                print(COLOR_RED + f"arbitrage failed with {e}" + COLOR_RESET)
            else:
                await on_success(arbitrage, amount, *args)

            i += 1

async def debug_arbitrage(arbitrage: DualArbitrage | TribArbitrage, amount, ctx):
    message = f"✅ Succesfully arbitraged {amount} {arbitrage.debug(get_sym_by_addr, get_dex_by_addr)}"
    await notify(message, ctx)
    print(message)

with open(sys.argv[1], "r") as file:
    config = json.loads(file.read())
    fl = config["fl"]
    weth = config["weth"]
    eth_dex = config["eth-dex"]
    node = config["node"]
    build = config["build"]
    tokens = config["tokens"]
    routers = config["routers"]
    private_key = config["private_key"]

dex_by_addr = { router["address"]: router["dex"] for router in routers }
addr_by_dex = { router["dex"]: router["address"] for router in routers }
get_addr_by_dex = lambda dex: addr_by_dex[dex]
get_dex_by_addr = lambda addr: dex_by_addr[addr]

sym_by_addr = { token["address"]: token["symbol"] for token in tokens }
addr_by_sym = { token["symbol"]: token["address"] for token in tokens }
get_sym_by_addr = lambda addr: sym_by_addr[addr]
get_addr_by_sym = lambda sym: addr_by_sym[sym]

with open(f"{build}.abi", "r") as file:
    abi = json.loads(file.read().strip())

web3 = Web3(Web3.HTTPProvider(node))

contract = web3.eth.contract(address=Web3.to_checksum_address(sys.argv[2]), abi=abi)
account = web3.eth.account.from_key(private_key)
eth_token = get_addr_by_sym(weth)
eth_router = get_addr_by_dex(eth_dex)

async def flash_arbitrage(ctx, dual):
    message = "Fetching prices🌐..."

    await notify(message, ctx)
    print(message)

    arb_routers = [(router["address"], router["estim"] if "estim" in router else None, router["avail"] if "avail" in router else None) for router in routers]
    eth_dex, eth_estim, eth_avail = [(address, estim, avail) for address, estim, avail in arb_routers if address == eth_router][0]
    if dual:
        arbitrages = await get_most_profitable_dual(
            [get_addr_by_sym(fl_token["symbol"]) for fl_token in fl],
            [token["address"] for token in tokens],
            arb_routers,
            eth_token,
            (eth_dex, eth_estim, eth_avail),
            debug_arbitrage,
            ctx
        )
    else:
        arbitrages = await get_most_profitable_trib(
            [get_addr_by_sym(fl_token["symbol"]) for fl_token in fl],
            [token["address"] for token in tokens],
            arb_routers,
            eth_token,
            (eth_dex, eth_estim, eth_avail),
            debug_arbitrage,
            ctx
        )
    if len(arbitrages) == 0:
        message = "No profit made, there is no profitable arbitrages❌."

        await notify(message, ctx)
        print(message)
        print("-"*len(message))
        return
    
    # arbitraging
    await arbitrage_while_profitable(arbitrages, debug_arbitrage, ctx)
    message = "Arbitrages ended✅."

    await notify(message, ctx)
    print(message)
    print("-"*len(message))

intents = Intents.all()
intents.members = True

bot = Bot(command_prefix="/", intents=intents)
loop = asyncio.get_event_loop()

async def notify(message: str, ctx):
    await ctx.channel.send(message)

@bot.command()
async def gas(ctx):
    gas_price = web3.eth.gas_price/1e18
    value = "GWEI"
    if gas_price < 1:
        value = "WEI"
        gas_price = int(gas_price*1e18)
    await ctx.channel.send(f"current gas price in {value} is {gas_price}")

@bot.command()
async def arbitrage2(ctx):
    await flash_arbitrage(ctx, True)

@bot.command()
async def arbitrage3(ctx):
    await flash_arbitrage(ctx, False)

bot.run(BOT_TOKEN)