from cryptohounds.config import *
from cryptohounds.web3_client import Web3Client
import time


web3_client = Web3Client("","")
character_contract = web3_client.get_contract(CHARACTERS_ADDRESS,CHARACTERS_ABI)
main_contract = web3_client.get_contract(MAIN_CONTRACT_ADDRESS,MAIN_CONTRACT_ABI)

def fight(client,character,target=0):
    func = main_contract.functions.fight(character,target)
    params = client.create_transaction_params()
    try:
        tx_hash = client.send_transaction(func,params)
        print(f"战斗发送成功：{tx_hash.hex()}")
    except Exception as e:
        print(f"战斗发送失败", e)
    time.sleep(60)


total_character = character_contract.functions.totalSupply().call()
print(f"当前全服角色总数：{total_character}")
while True:
    for account in ACCOUNT_LIST:
        character_list = account['character_list']
        client = Web3Client(account['address'],account['key'])
        rewards = main_contract.functions.getTokenRewardsFor(account['address']).call()
        print(f"*****   开始操作{account['name']}，"
              f"角色数:{len(character_list)},"
              f"待领取奖励：{rewards/9}   *****")
        time.sleep(2)
        for character in character_list:
            stamina = character_contract.functions.getStaminaPoints(character).call()
            time.sleep(1)
            level = character_contract.functions.getLevel(character).call()
            time.sleep(1)
            xpForNextLevel = character_contract.functions.getRequiredXpForNextLevel(level).call()
            time.sleep(1)
            xp = main_contract.functions.getXpRewards(character).call()
            time.sleep(1)
            power = character_contract.functions.getPower(character).call()
            print(f"角色{character}当前等级:{level},战斗力:{power},"
                  f"体力:{stamina}，当前经验:{xp},升级所需经验:{xpForNextLevel}")
            if xp > xpForNextLevel:
                print("先领取经验")

            if stamina >= 40:
                print(f"角色{character}开始战斗...")
                fight(client,character,0)
            else:
                print(f"体力不足，继续等待")
            time.sleep(5)
    time.sleep(600)









