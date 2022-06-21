import NFTInfoUtility as nftUtility
import NFTHolderInfo as holder
import random
import sys

CREATOR_ADDRESS = "0x4354ade9a9e2918D4c33DA3e565a8E9637CD8EB6"

BABY_LOTTERY_WIN_NO = 50  
BABY_KAKURITSU_UP = 20 #ベビー抽選確率上昇値

def daddyLottery(reader : nftUtility.DaddyNFTInfoReader) :
    print("ダディ抽選開始")
    nftHolders = reader.getNftHolders(True)
    nftCount = reader.getNftCount(True)
    creatorInfo : holder.UserInfo = nftHolders["0x4354ade9a9e2918D4c33DA3e565a8E9637CD8EB6"]
    winUserInfo : holder.UserInfo
    while 1 :
        winTokenId = random.randint(1,nftCount)
        winUserInfo = reader.serchTokenHolderBy(winTokenId)
        if winUserInfo == None or winUserInfo.walletAddress == "" :
            continue

        if winUserInfo.walletAddress == creatorInfo.walletAddress :
            #クリエーターは当選対象外のため再抽選
            continue

        print("当選ダディIDは『 " + str(winTokenId) + " 』")
        break
    
    winAddress = winUserInfo.walletAddress
    print("当選者のアドレスは『 " + str(winAddress) + " 』")

    nonOwnerNfts = creatorInfo.tokenInfoList
    nonOwnerNftList = list(nonOwnerNfts.values())
    giftTokenId = nonOwnerNftList[random.randint(0,len(nonOwnerNftList) - 1)].tokenId

    print("景品のダディIDは『 " + str(giftTokenId) + " 』")

def babyLottery(reader : nftUtility.DaddyNFTInfoReader) :
    print("ベビー抽選開始")
    nftHolders = reader.getNftHolders(True)
    creatorInfo : holder.UserInfo = nftHolders["0x4354ade9a9e2918D4c33DA3e565a8E9637CD8EB6"]
    babyBornCnt = 0
    for userInfo in nftHolders.values() :
        userInfo : holder.UserInfo
        if userInfo.walletAddress == creatorInfo.walletAddress :
            #クリエーターは除外
            continue

        motherNfts = reader.getMotherNfts(userInfo)
        fatherNfts = reader.getNormalDaddyNfts(userInfo)

        if len(motherNfts) == 0 or len(fatherNfts) == 0 :
            continue
            
        print("ベビー抽選対象者：『 " + str(userInfo.walletAddress) + " 』" )
        winPairList = judgeBornBaby(motherNfts, fatherNfts, userInfo.cryptoGakuenNftHolder)

        for winPair in winPairList :
            print("★当選★ 該当ペアIDは『 " + str(winPair[0]) + " 』" + "『 " + str(winPair[1]) + " 』")
            babyBornCnt += 1

    if babyBornCnt == 0 :
        print("該当者なし")
        
def judgeBornBaby(motherNfts, fatherNfts, isCgNftHolder) :
    pairList = []

    if len(motherNfts) == 0 or len(fatherNfts) == 0 :
        return pairList

    lottery = calcBabyBornProbability(isCgNftHolder)
    print("当選確率:" + str(lottery['kakuritsu']) + "%")
    for motherNft in motherNfts :
        motherNft : holder.TokenInfo
        for fatherNft in fatherNfts :
            fatherNft : holder.TokenInfo
            # ベビー誕生確率抽選
            winNo = random.randint(lottery['lotteryMinNo'],lottery['lotteryMaxNo'])
            if winNo == BABY_LOTTERY_WIN_NO :
                pairList.append([motherNft.tokenId, fatherNft.tokenId])

    return pairList

def calcBabyBornProbability(isCgNftHolder) :
    # ベビー誕生確率抽選
    lotteryMaxNo = 100 - BABY_KAKURITSU_UP
    # CryptoGakuenNFTホルダーは当選確率5%アップ
    if isCgNftHolder :
        lotteryMaxNo -= 5
            
    kakuritsu = 1 if lotteryMaxNo == 100 else 100 - lotteryMaxNo
    return {'lotteryMinNo':1, 'lotteryMaxNo':lotteryMaxNo, 'kakuritsu': kakuritsu}
             

if __name__ == "__main__":

    reader = nftUtility.DaddyNFTInfoReader()
    print("1: ダディ抽選")
    print("2: ベビー抽選")
    print("3: すべての抽選")

    while 1:
        val = input('Enter no: ')
        if val == "1" :
            daddyLottery(reader)
            break
        elif val == "2" :
            babyLottery(reader)
            break
        elif val == "3" :
            daddyLottery(reader)
            babyLottery(reader)
            break
        else :
            print("番号が不正です。")
