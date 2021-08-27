from web3 import Web3,HTTPProvider

class Web3Client:
    """
        web3客户端
    """
    def __init__(self,wallet_address="",wallet_key="",url="https://bsc-dataseed2.binance.org"):
        """
            初始化
        :param wallet_address:钱包地址
        :param wallet_key: 钱包私钥
        :param url: 节点地 址
        """
        self.web3 = Web3(HTTPProvider(url))
        self.wallet_address = wallet_address
        self.wallet_key = wallet_key

    def get_balance(self,wallet_address):
        """
            查询钱包BNB（ETH)余额
        :param wallet_address:钱包地址
        :return:
        """
        return self.web3.fromWei(self.web3.eth.getBalance(wallet_address), "ether")

    def get_contract(self,contract_address,contract_abi):
        """
            根据合约地址和ABI获取合约对象
        :param contract_address:
        :param contract_abi:
        :return:
        """
        return self.web3.eth.contract(address=contract_address,abi=contract_abi)

    def get_token_balance(self,token_contract,wallet_address):
        """
            获取指定TOKEN的钱包余额
        :param contract:
        :param wallet_address:
        :return:
        """
        return self.web3.fromWei(token_contract.functions.balanceOf(wallet_address).call(), "ether")

    def create_transaction_params(self,gas_price=5, value=0, gas_limit=1000000):
        """
            构建交易参数
        :param wallet_address: 钱包地址
        :param gas_price: BSC默认为5
        :param value: 默认为0
        :param gas_limit: 默认为500000
        :return:
        """
        params = {
            "from": self.wallet_address,
            "value": value,
            'gasPrice': self.web3.toWei(gas_price, 'gwei'),
            "gas": gas_limit,
            "nonce": self.web3.eth.getTransactionCount(self.wallet_address),
        }
        return params

    def send_transaction(self,func, params):
        """
            发送交易
        :param func: 合约function
        :param params: 交易参数
        :return:
        """
        tx = func.buildTransaction(params)
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.wallet_key)
        return self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    def apporve(self,token_contract,address,amount=9999999):
        """
            将指定TOKEN授权给指定地址
        :param token_contract:要授权的TOKEN CONTRACT
        :param address:授权给哪个地址
        :param amount:授权数量
        :return:
        """
        func = token_contract.functions.approve(
            address,
            self.web3.toWei(amount, "ether")
        )
        params = self.create_transaction_params()
        try:
            return self.send_transaction(func,params)
        except Exception as e:
            print(e)
            return None


    def build_transfer_params(self,target_address,amount):
        """
            构建转账参数（转BNB）
        :param target_address:
        :param amount:
        :return:
        """
        nonce = self.web3.eth.getTransactionCount(self.wallet_address)
        params = {
            'nonce':nonce,
            'to':target_address,
            'value':self.web3.toWei(amount,'ether'),
            'gas':21000,
            'gasPrice':self.web3.toWei(5,'gwei'),
            'from':self.wallet_address,
        }
        return params

    def transfer_token(self,token_contract,target_address,amount,gas_price=5,gas_limit=500000):
        """
            转账TOKEN（非BNB）
        :param target_address: 目标地址
        :param amount: 数量
        :param gas_price:
        :param gas_limit:
        :return:
        """
        params = {
            "from": self.wallet_address,
            "value": 0,
            'gasPrice': self.web3.toWei(gas_price, 'gwei'),
            "gas": gas_limit,
            "nonce": self.web3.eth.getTransactionCount(self.wallet_address),
        }
        func = token_contract.functions.transfer(target_address,self.web3.toWei(amount,"ether"))
        try:
            return self.send_transaction(func, params)
        except Exception as e:
            print(e)
            return None

    def get_transaction_status(self,tx_hash):
        """
            查询交易状态
        :param tx_hash:
        :return: status-  1:完成   0：失败  其他：等待
        """
        try:
            return self.web3.eth.getTransactionReceipt(tx_hash)['status']
        except Exception as e:
            print(e)
            return None

    def get_transaction_log(self,tx_hash):
        """
            查询交易日志
        :param tx_hash:
        :return: status-  1:完成   0：失败  其他：等待
        """
        try:
            return self.web3.eth.getTransactionReceipt(tx_hash)
        except Exception as e:
            print(e)
            return None
