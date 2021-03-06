import datetime
import random
import re


def DealParam(rawStrParam, defaultParam):
    if len(rawStrParam) > 0:
        return rawStrParam
    else:
        return defaultParam


# 是否重击或是失手，0无，1重击，2失手
def IsCriticalOrMiss(criticalNumParam, missNumParam, diceResultParam):
    criticalNumList = criticalNumParam.split('-')
    missNumList = missNumParam.split('-')
    criticalNumMin = int(criticalNumList[0])
    criticalNumMax = int(criticalNumList[0])
    if len(criticalNumList) > 1:
        criticalNumMax = int(criticalNumList[1])
    missNumMin = int(missNumList[0])
    missNumMax = int(missNumList[0])
    if len(missNumList) > 1:
        missNumMax = int(missNumList[1])
    tmp = criticalNumMin
    criticalNumMin = max(criticalNumMin, missNumMax)
    missNumMax = min(tmp, missNumMax)
    if criticalNumMin <= diceResultParam <= criticalNumMax:
        return 1
    if missNumMin <= diceResultParam <= missNumMax:
        return 2


rawStr = input("描述，骰子，重击，失手：\n")
res = '[,，]'
diceRes = '[dD]'
while (rawStr != 'end') and (rawStr != ''):
    openFile = open('log.txt', 'a+')
    splitStr = re.split(res, rawStr)

    record = splitStr[0]
    # 可能有多种类型掷骰方式，如“3#2d20+2d6+5”、“2d8+2d6+2”
    rawDiceStr = 'd20'
    if len(splitStr) > 1:
        rawDiceStr = splitStr[1]

    # 重击与失手
    criticalNum = '20'
    missNum = '1'
    if len(splitStr) > 2:
        criticalNum = DealParam(splitStr[2], '20')
    if len(splitStr) > 3:
        missNum = DealParam(splitStr[3], '1')

    # “#”前掷骰次数
    rollTimes = 1
    rollTimeList = rawDiceStr.split('#')
    rawDiceStyle = rollTimeList[0]
    if len(rollTimeList) > 1:
        rollTimes = int(rollTimeList[0])
        rawDiceStyle = rollTimeList[1]

    rawDiceList = rawDiceStyle.split('+')

    FinalStr = []
    # rollResults = []

    # 共投掷’#‘前面次
    for i in range(rollTimes):
        # 处理所有骰子,每一骰子可能格式为："d20"、“2d6”、“3”
        outDiceStr = ''
        diceResult = 0
        # 单d20才判断重击与失手，2d20这种不必判断
        isD20 = False
        # 是否重击或是失手，0无，1重击，2失手
        isCriticalOrMiss = 0
        for rawDice in rawDiceList:
            rawDiceSplit = re.split(diceRes, rawDice)
            diceStrTmp = ''
            if len(rawDiceSplit) > 1:
                diceNum = int(DealParam(rawDiceSplit[0], '1'))
                diceStyle = int(DealParam(rawDiceSplit[1], '20'))
                if diceNum == 1 and diceStyle == 20:
                    isD20 = True
                # inRollResults = []
                # 掷骰
                for j in range(diceNum):
                    if j > 0:
                        diceStrTmp += '+'
                    rollResult = random.randint(1, diceStyle)
                    # inRollResults.append(rollResult)
                    diceStrTmp += str(rollResult)
                    diceResult += rollResult
                    # 判断重击或失手
                    if isD20:
                        isCriticalOrMiss = IsCriticalOrMiss(criticalNum, missNum, rollResult)
                if diceNum > 1:
                    diceStrTmp = '(' + diceStrTmp + ')'
            else:
                diceStrTmp = DealParam(rawDiceSplit[0], '0')
                diceResult += int(DealParam(rawDiceSplit[0], '0'))
            if len(outDiceStr) > 0:
                outDiceStr += '+' + diceStrTmp
            else:
                outDiceStr = diceStrTmp
        # rollResults.append(rollResult)
        finalTmp = '第' + str(i + 1) + '次掷骰结果：' + outDiceStr + '=' + str(diceResult)
        if isCriticalOrMiss == 1:
            finalTmp += ' 重击！！！！！'
        if isCriticalOrMiss == 2:
            finalTmp += ' 失手！！！！！'
        FinalStr.append(finalTmp)

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    newRecord = nowTime + '\n' + record + '（' + rawDiceStr + '）' + '：'
    print('\n' + newRecord)
    openFile.write(newRecord + '\n')
    for FinalStrTmp in FinalStr:
        print(FinalStrTmp)
        openFile.write(FinalStrTmp + '\n')
    openFile.write('\n')
    openFile.close()
    rawStr = input("\n描述，骰子，重击，失手：\n")
