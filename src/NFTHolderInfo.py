import json
import copy

class UserInfo:
    def __init__(self) :
        self.__walletAddress = ""
        self.__tokenInfoList = {}
        self.__cryptoGakuenNftHolder : bool = False

    @property
    def walletAddress(self) :
        return self.__walletAddress
    
    @walletAddress.setter
    def walletAddress(self, walletAddress) :
        self.__walletAddress = walletAddress

    @property
    def tokenInfoList(self) :
        return self.__tokenInfoList
    
    @tokenInfoList.setter
    def tokenInfoList(self, tokenInfoList)  :
        self.__tokenInfoList = tokenInfoList

    @property
    def cryptoGakuenNftHolder(self) :
        return self.__cryptoGakuenNftHolder

    @cryptoGakuenNftHolder.setter
    def cryptoGakuenNftHolder(self, cryptoGakuenNftHolder) :
        self.__cryptoGakuenNftHolder = cryptoGakuenNftHolder

class TokenInfo:
    def __init__(self) :
        self.__tokenId = 0
        self.__contractId = ""
        self.__attributeList = {}
        
    @property
    def tokenId(self) :
        return self.__tokenId

    @tokenId.setter
    def tokenId(self, tokenId) :
        self.__tokenId = tokenId    

    @property
    def contractId(self) :
        return self.__contractId
    
    @contractId.setter
    def contractId(self, contractId) :
        self.__contractId = contractId

    @property
    def attributeList(self) :
        return self.__attributeList
    
    @attributeList.setter
    def attributeList(self, attributeList) :
        self.__attributeList = attributeList




