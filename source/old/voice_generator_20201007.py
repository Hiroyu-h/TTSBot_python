import subprocess
import re

# remove_custom_emoji
# 絵文字IDは読み上げない
def remove_custom_emoji(text):
    pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'    # カスタム絵文字のパターン
    return re.sub(pattern,'',text)  # 置換処理

# urlAbb
# URLなら省略
def urlAbb(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    # "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    #return re.sub(pattern,'URLは省略するね！',text) # 置換処理
    return re.sub(pattern,'',text) # 置換処理

# creat_WAV
# message.contentをテキストファイルに書き込み
def create_WAV(inputText, voice_num, voice_speed):
    # message.contentをテキストファイルに書き込む

    inputText = remove_custom_emoji(inputText)
    inputText = urlAbb(inputText)
    input_file = 'C:\\open_jtalk\\input.txt'

    with open(input_file,'w',encoding='shift_jis') as file:
        file.write(inputText)

    # dicのpath
    x = 'C:\\open_jtalk\\dic'
    #voiceファイルのpath
    if voice_num == '0':
        m = 'C:\\open_jtalk\\htsvoice\\mei_happy.htsvoice'
    elif voice_num == '1':
        m = 'C:\\open_jtalk\\htsvoice\\mei_normal.htsvoice'
    elif voice_num == '2':
        m = 'C:\\open_jtalk\\htsvoice\\mei_angry.htsvoice'
    elif voice_num == '3':
        m = 'C:\\open_jtalk\\htsvoice\\mei_sad.htsvoice'
    elif voice_num == '4':
        m = 'C:\\open_jtalk\\htsvoice\\mei_bashful.htsvoice'
    else:
        m = 'C:\\open_jtalk\\htsvoice\\nitech_jp_atr503_m001.htsvoice'

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
    