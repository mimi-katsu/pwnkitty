import os
import random
import time

def play_intro():
    path = './misc/intro'
    intros = os.listdir(path)
    intro = random.choice(intros)
    intro_path = os.path.join(path, intro)

    with open(intro_path, 'r', encoding='utf-8') as i:
        lines = i.readlines()
        for line in lines:
            print(line.strip('\n'))
            time.sleep(.1)
        
        print('''From Maia with love :3 - https://github.com/mimi-katsu/pwnkitty\n==== GNU GENERAL PUBLIC LICENSE Version 3 ====\nPlease don't use for illegal stuff 0w0\n''')

