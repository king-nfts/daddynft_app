
import json
from time import sleep
from web3 import Web3
import NFTHolderInfo as holder
import requests, json

APIKEY="H1QE3RNI29UETZQ8JPAA7BVBT3AVCZYB4D"
POLYSCAN_URL="https://api.polygonscan.com/"

POLY_RPC = "https://polygon-rpc.com"
DADDY_ADDRESS="0xB6Ff710E4EC296fE5Ab3a4DB77bF1D14e6B9281C"
GAKUEN_ADDRESS="0xC109A5DC4ACd0Eb998083704Ea0119394Ac663a1"

class DaddyNFTInfoReader :
   def __init__(self) -> None:
      self.web3 = Web3(Web3.HTTPProvider(POLY_RPC))
      with open('NFT保有者抽選機能\DaddyNFT_ABI.json') as f:
         self.daddyNftAbi = json.load(f)

      self.daddyContract = self.web3.eth.contract(address=DADDY_ADDRESS, abi=self.daddyNftAbi)
      self.gakuenContract = self.web3.eth.contract(address=GAKUEN_ADDRESS, abi=self.daddyNftAbi)
      self.nftHolders = {}
      self.nftTotalNum = 0
      

   def getNftHolders(self, cacheOn : bool) -> list :
      if cacheOn == True and any(self.nftHolders) :
         return self.nftHolders 

      print("NFT情報収集")   
      self.nftHolders = {}
      i=1
      while(1) :
         try :
            address = self.daddyContract.functions.ownerOf(i).call()
            if address not in self.nftHolders  :
               userInfo = holder.UserInfo()
               userInfo.walletAddress = address
               tokenInfo : holder.TokenInfo = holder.TokenInfo()
               tokenInfo.tokenId = i
               tokenInfo.contractId = DADDY_ADDRESS
               attributeList = self.parseTokenMetaData(tokenInfo)
               tokenInfo.attributeList = attributeList
               key = tokenInfo.contractId + "," + str(tokenInfo.tokenId)
               userInfo.tokenInfoList[key] = tokenInfo
               self.nftHolders [address] = userInfo
            else :
               userInfo : holder.UserInfo  = self.nftHolders [address]
               tokenInfo = holder.TokenInfo()
               tokenInfo.tokenId = i
               tokenInfo.contractId = DADDY_ADDRESS
               attributeList = self.parseTokenMetaData(tokenInfo)
               tokenInfo.attributeList = attributeList
               key = tokenInfo.contractId + "," + str(tokenInfo.tokenId)
               userInfo.tokenInfoList[key] = tokenInfo

            print("トークンID:" + str(i))
            i += 1
         except Exception: 
            break
   
      self.nftTotalNum = i -1

      for userInfo in self.nftHolders.values() :
         num = self.gakuenContract.functions.balanceOf(userInfo.walletAddress).call()
         if num > 0 :
            userInfo.cryptoGakuenNftHolder = True
            print("CryptoGakuenホルダー該当:" + userInfo.walletAddress)

      return self.nftHolders 

   def getAddressByTokenId(self, tokenId : int) -> str :
      try :
         return self.daddyContract.functions.ownerOf(tokenId).call()
      except Exception: 
         return None

   def getNftCount(self, cacheOn : bool) -> int :
      if cacheOn == True and any(self.nftHolders) :
         return self.nftTotalNum
      else :
         self.getNftHolders(False)
         return self.nftTotalNum

   def serchTokenHolderBy(self, tokenId : int) -> holder.UserInfo :
      for key in self.nftHolders:
        userInfo : holder.UserInfo = self.nftHolders[key]  
        for token in userInfo.tokenInfoList.values() :
            token : holder.TokenInfo
            if token.tokenId == tokenId :
                return userInfo
      return None

   def parseTokenMetaData(self, token : holder.TokenInfo) :
      url = self.daddyContract.functions.tokenURI(token.tokenId).call()
      metadataJson = requests.get(url)
      metaData = json.loads(metadataJson.text)
      attributes = metaData['attributes']
      attributesList = []
      for attribute in attributes :
            tmp = {'NAME' : attribute['trait_type'], 'VALUE' : attribute['value']}
            attributesList.append(tmp)

      return attributesList
      
   def getMotherNfts(self, userInfo : holder.UserInfo) :
      retList = []
      for tokenInfo in userInfo.tokenInfoList.values() :
         tokenInfo : holder.TokenInfo
         for attribute in tokenInfo.attributeList :
            if attribute['NAME'] == 'TYPE' and attribute['VALUE'] == 'mother' :
               retList.append(tokenInfo)
               break
      
      return retList

   def getNormalDaddyNfts(self, userInfo : holder.UserInfo) :
      retList = []
      for tokenInfo in userInfo.tokenInfoList.values() :
         tokenInfo : holder.TokenInfo

         if len(tokenInfo.attributeList) == 0 :
            retList.append(tokenInfo)
            continue
         
         for attribute in tokenInfo.attributeList :
            if attribute['NAME'] == 'TYPE' and attribute['VALUE'] == 'mother' :
               break
         else :
            retList.append(tokenInfo)

         continue               
      return retList