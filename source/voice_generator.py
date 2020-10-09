import pathlib
import re
import subprocess


# remove_custom_emoji
# 絵文字IDは読み上げない
def remove_custom_emoji(text):
    pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'    # カスタム絵文字のパターン
    return re.sub(pattern, '', text)  # 置換処理

# urlAbb
# URLなら省略
def urlAbb(text):
    return re.sub(r'http(s)?://([\w-]+\.)+[\w-]+(/[-\w ./?%&=]*)?', 'URL', text) # 置換処理

# reactionの置換   
def reaction_rp(text):
    text = text.replace('<:', '')
    text = re.sub(r':[0-9]*>', '', text)
    return text

def rep_w(text):
    
    return text

# creat_WAV
# message.contentをテキストファイルに書き込み
def create_WAV(inputText, voice_num, voice_speed):
    # message.contentをテキストファイルに書き込む
    # unicodeText = inputText.decode('utf-8')
    # unicodeText = urlAbb(unicodeText)
    # unicodeText = remove_custom_emoji(unicodeText)
    # unicodeText = reaction_rp(unicodeText)
    # unicodeText = unicodeText.replace('<', '').replace('>', '')

    inputText = remove_custom_emoji(inputText)
    inputText = urlAbb(inputText)
    inputText = reaction_rp(inputText)
    inputText = inputText.replace('<', '').replace('>', '')

       
    # inputText = unicodeText.encode('shift_jis')
    
    input_file = 'C:\\open_jtalk\\input.txt'

    with open(input_file,'w',encoding='shift_jis') as file:
        file.write(inputText)
    
    # dicのpath
    x = 'C:\\open_jtalk\\dic'
    # voiceファイルのpath
    # いっぱい音響ファイルあった↓
    # http://akihiro0105.web.fc2.com/Downloads/Downloads-htsvoice.html
    tuple_htsvoice = (
        'C:\\open_jtalk\\htsvoice\\mei_happy.htsvoice',
        'C:\\open_jtalk\\htsvoice\\mei_normal.htsvoice',
        'C:\\open_jtalk\\htsvoice\\mei_angry.htsvoice',
        'C:\\open_jtalk\\htsvoice\\mei_sad.htsvoice',
        'C:\\open_jtalk\\htsvoice\\mei_bashful.htsvoice',
        'C:\\open_jtalk\\htsvoice\\yamiyo_sakura_1.0.htsvoice',
        'C:\\open_jtalk\\htsvoice\\nitech_jp_atr503_m001.htsvoice'
    )
    
    m = tuple_htsvoice[int(voice_num)]

    #発声スピード
    #r = '1.0'
    r = voice_speed

    #出力先
    ow = 'C:\\open_jtalk\\output.wav'

    args= {'x':x, 'm':m, 'r':r, 'ow':ow, 'input_file':input_file}

    # 音声ファイル生成コマンド
    command = 'C:\\open_jtalk\\open_jtalk.exe -x {x} -m {m} -r {r} -ow {ow} {input_file}'
    
    cmd= command.format(**args)
    print(cmd)
    

    subprocess.run(cmd)
    return True

if __name__ == '__main__':
    create_WAV('テスト','7','1.0')
    