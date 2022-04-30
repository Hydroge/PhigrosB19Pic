import json
import data
from PIL import Image, ImageFilter, ImageDraw, ImageFont

cur = data.conn.cursor()
inputFilePathOrigin = "..\\content\\save\\"
outputFilePathOrigin = "..\\content\\output\\"


# 找歌名
def findName(key):
    sql = 'select sname from songs2nex WHERE id=\'' + key + '\''
    cur.execute(sql)
    try:
        res = cur.fetchone()[0]
        # print(res)
    except:
        return "-1"
    else:
        if not (res is None):
            return res
        else:
            return "-1"


# 制图
def main(userName):
    inputFilePath = inputFilePathOrigin + userName + "Data.json"
    fi = open(inputFilePath, "r", encoding='utf-8')
    strq = fi.read()
    fi.close()
    dataInfo = json.loads(strq)

    userName = dataInfo['userName']
    rks = dataInfo['rks']
    a1 = dataInfo['a1']
    b19list = dataInfo['b23']

    outputFilePath = outputFilePathOrigin + userName + "b19.png"
    # im = Image.open(fp, mode="r")
    img = Image.new('RGB', (770, 495), color="#eeeeee")
    draw = ImageDraw.Draw(img)
    fontExo = ImageFont.truetype('C:\\Windows\\Fonts\\Exo-Regular.ttf', size=20)
    fontExos = ImageFont.truetype('C:\\Windows\\Fonts\\Exo-Regular.ttf', size=17)
    # fontGeo = ImageFont.truetype('C:\\Windows\\Fonts\\GeosansLight.ttf', size=15)
    # fontKaze = ImageFont.truetype('C:\\Windows\\Fonts\\Kazesawa-Regular.ttf', size=15)
    fontZHCN = ImageFont.truetype('C:\\Windows\\Fonts\\NotoSansCJKsc-Regular.otf', size=20)
    # fontLuci = ImageFont.truetype('C:\\Windows\\Fonts\\l_10646.ttf', size=20)
    fontYahei = ImageFont.truetype('C:\\Windows\\Fonts\\msyh.ttc', size=20)
    fontYaheis = ImageFont.truetype('C:\\Windows\\Fonts\\msyh.ttc', size=16)
    fontXinwei = ImageFont.truetype('C:\\Windows\\Fonts\\STXINWEI.TTF', size=16)

    draw.text(xy=(20, 10), text=userName, fill=(0, 0, 0), font=fontZHCN)
    draw.text(xy=(200, 15), text="rks:" + str(round(rks, 3)), fill=(0, 0, 0), font=fontExo)
    draw.text(xy=(460, 13), text="全曲共计φ: " + str(dataInfo['apNum']) + " 个,其中IN: " + str(dataInfo['apNumIN']) + " 个",
              fill=(255, 0, 0),
              font=fontYahei)
    c = 50
    for i in range(5):
        if i == 4:
            draw.text(xy=(15, 360), text="Overflow", fill=(0, 0, 0), font=fontExos, stroke_width=2,
                      stroke_fill="#ffffff")
            draw.line(xy=(10, 385, 760, 385), fill=(0, 0, 0), width=3)
            c += 25
        for j in range(5):
            if i == 0 and j == 0:
                tst = findName(a1['songId']) + '[' + a1['songType'] + ']'
                acc = str(100.0)
                rks = str(a1['rating'])
            else:
                tst = findName(b19list[i * 5 + j - 1]['songId']) + '[' + b19list[i * 5 + j - 1]['songType'] + ']'
                acc = str(round(b19list[i * 5 + j - 1]['acc'], 3))
                rks = str(b19list[i * 5 + j - 1]['songDiff']) + "→" + str(round(b19list[i * 5 + j - 1]['rating'], 3))
            if fontYaheis.getsize(tst)[0] > 145:
                while fontYaheis.getsize(tst)[0] > 135:
                    tst = tst[0:-5] + tst[-4:]
                tst = tst[0:-5] + "..." + tst[-4:]
            if i == 0 and j == 0:
                draw.text(xy=(20 + j * 150, c + i * 80), text=tst, fill=(255, 0, 0), font=fontYaheis)
                draw.text(xy=(20 + j * 150, c + 25 + i * 80), text='Acc: ' + acc + " %\n" + "Rks: " + rks,
                          fill=(255, 0, 0),
                          font=fontYaheis)
            else:
                draw.text(xy=(20 + j * 150, c + i * 80), text=tst, fill=(0, 0, 0), font=fontYaheis)
                draw.text(xy=(20 + j * 150, c + 25 + i * 80), text='Acc: ' + acc + " %\n" + "Rks: " + rks,
                          fill=(0, 0, 0),
                          font=fontYaheis)
            if i * 5 + j - 1 == 23:
                break
    draw.text(xy=(542, 470), text="ver.alpha Generated by 朝月酱", fill=(100, 100, 100), font=fontXinwei)
    img.filter(ImageFilter.CONTOUR)
    img.save(outputFilePath)
    cur.close()
    return outputFilePath
