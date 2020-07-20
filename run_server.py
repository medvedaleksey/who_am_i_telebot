import telebot
from telebot import types
import random
import time
import threading

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['registration'])
def registration(message):
    try:
        bot.delete_message(message.chat.id,message.message_id)
        if message.chat.type=='group' or message.chat.type=='supergroup':
            filepeople = open(str(message.chat.id)+'people'+'.txt',"r")
            k=filepeople.readlines()
            filepeople.close()
            if len(k)==0:
                filewords = open(str(message.chat.id)+'words'+'.txt',"w")
                fileanswer=open(str(message.chat.id)+'answer'+'.txt',"w")
                file_answerid = open(str(message.chat.id)+'answerid.txt','w')
                file_answerid.close()
                filepeople_words=open(str(message.chat.id)+'.txt',"w")
                filepeople = open(str(message.chat.id)+'people'+'.txt',"w")
                filepeople.close()
                f=open(str(message.chat.id)+'id.txt',"w")
                keyboard = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text="Войти", url="https://t.me/Who_am_I_newbot?start="+str(message.chat.id))
                keyboard.add(url_button)
                fileanswer.write('0'+'\n'+'0')
                msg=bot.send_message(message.chat.id, "Играть", reply_markup=keyboard)
                bot.pin_chat_message(message.chat.id,msg.message_id)
                filewords.close()
                filepeople_words.close()
                fileanswer.close()
                f.close()
            else:
                bot.send_message(message.chat.id,"Игра уже началась")
    except:
        if message.chat.type=='group' or message.chat.type=='supergroup':
            filepeople=open(str(message.chat.id)+'people'+'.txt',"w")
            filewords = open(str(message.chat.id)+'words'+'.txt',"w")
            fileanswer=open(str(message.chat.id)+'answer'+'.txt',"w")
            file_answerid = open(str(message.chat.id)+'answerid.txt','w')
            file_answerid.close()
            f=open(str(message.chat.id)+'id.txt',"w")
            filepeople_words=open(str(message.chat.id)+'.txt',"w")
            keyboard = types.InlineKeyboardMarkup()
            filepeople = open(str(message.chat.id)+'people'+'.txt',"w")
            filepeople.close()
            url_button = types.InlineKeyboardButton(text="Войти", url="https://t.me/Who_am_I_newbot?start="+str(message.chat.id))
            keyboard.add(url_button)
            fileanswer.write('0'+'\n'+'0')
            msg=bot.send_message(message.chat.id, "Играть", reply_markup=keyboard)
            filewords.close()
            filepeople_words.close()
            fileanswer.close()
            filepeople.close()
            f.close()
            
@bot.message_handler(commands=['invite'])
def invite(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        switch_button = types.InlineKeyboardButton(text="Выбрать чат", switch_inline_query="Telegram")
        keyboard.add(switch_button)
        bot.send_message(message.chat.id, "Нажмите кнопку чтобы добавить бота в чат", reply_markup=keyboard)
    except:
        pass

    
@bot.message_handler(commands=['start'])
def start(message):
    try:
        add_user=True
        filepeople_words = open(str(message.text[7:len(message.text)])+'.txt','r')
        people=filepeople_words.readlines()
        filepeople_words.close()
        s=str(message.text[7:len(message.text)])
        if s==' ':
            bot.delete_message(message.chat.id,message.message_id)
            return
        if len(people)==0:
            filepeople = open(str(message.text[7:len(message.text)])+'people'+'.txt','r')
            line=filepeople.readlines()
            for i in range(len(line)):
                if line[i]==str(message.from_user.id)+'\n':
                    add_user=False
            filepeople.close()
            filepeople = open(str(message.text[7:len(message.text)])+'people'+'.txt',"a")
            bot.delete_message(message.chat.id,message.message_id)
            filepeople.close()
        else:
            for i in range(len(people)):
                if people[i]==str(message.from_user.id)+'\n':
                    add_user=False
        if add_user:
            bot.send_message(message.chat.id,"Добавьте 2 слова")
            a=bot.register_next_step_handler(message,lambda message:send_word(message,s,message.from_user.id,message.from_user.first_name))
    except:
        bot.delete_message(message.chat.id,message.message_id)

        
@bot.message_handler(commands=['game'])
def game(message):
    try:
        bot.delete_message(message.chat.id,message.message_id)
        filepeople = open(str(message.chat.id)+'people'+'.txt','r')
        filewords = open(str(message.chat.id)+'words'+'.txt','r')
        people=filepeople.readlines()
        words=filewords.readlines()
        filepeople.close()
        filewords.close()
        if len(people)>=4:
            filepeople_words=open(str(message.chat.id)+'.txt','w')
            t=time.time()
            filepeople_words.write(str(t)+'\n')
            i=0
            all_player=[]
            while i<len(people):
                ran=random.randint(0,len(words)-1)
                if ran==i or ran==i+1:
                    ran=(ran+2)%(len(words))
                l=people[i]+people[i+1]+words[ran]
                filepeople_words.write(l)
                words.pop(ran)
                all_player.append(str(int(i/2+1))+') '+"["+people[i+1][:-1]+"]"+"(tg://user?id="+str(people[i][:-1])+')')
                i=i+2
            f = open(str(message.chat.id)+'words'+'.txt','w')
            f.writelines(words)
            f.close()
            bot.send_message(message.chat.id,"Список игроков:"+'\n'+'\n'.join(all_player), parse_mode="Markdown")
            mention = 'Ход игрока '+"["+people[1]+"](tg://user?id="+str(people[0][:-1])+")"
            bot.send_message(message.chat.id,mention, parse_mode="Markdown")
            filepeople_words.close()
            x=threading.Thread(target=next_player, args=(t,message.chat.id))
            x.start()
        else:
            bot.send_message(message.chat.id,'Недостаточно людей. Минимум 2.')
    except:
        pass

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        filepeople_words=open(str(message.chat.id)+'.txt','r')
        people=filepeople_words.readlines()
        filepeople_words.close()
        if message.from_user.id==int(people[1]):
            people[0]=str(time.time())+'\n'
            real_ques=message.text
            real_ques1=real_ques+'\n'
            if real_ques1.lower()==people[3].lower():
                mention = 'Игрок '+"["+people[2][:-1]+"](tg://user?id="+str(people[1][:-1])+")"+' победил'
                bot.send_message(message.chat.id,mention,parse_mode="Markdown")  
                filepeople = open(str(message.chat.id)+'people'+'.txt',"r")
                k=filepeople.readlines()
                filepeople.close()
                for i in range(len(k)):
                    if k[i]==people[1]:
                        break
                filepeople = open(str(message.chat.id)+'people'+'.txt',"w")
                filepeople.writelines(k)
                filepeople.close()
                del people[1]
                del people[1]
                del people[1]
                if len(people)>1:
                    i=1
                    all_player=[]
                    while i<=len(people):
                        try:
                            all_player.append(str(int((i+1)/2))+') '+"["+people[i+1][:-1]+"]"+"(tg://user?id="+str(people[i][:-1])+')')
                            i=i+3
                        except:
                            break
                    bot.send_message(message.chat.id,"Список игроков:"+'\n'+'\n'.join(str(x) for x in all_player), parse_mode="Markdown")
                    people[0]=str(time.time())+'\n'
                    filepeople_words=open(str(message.chat.id)+'.txt','w')
                    filepeople_words.writelines(people)
                    filepeople_words.close()
                    mention = 'Ход игрока '+"["+people[2]+"](tg://user?id="+str(people[1][:-1])+")"
                    bot.send_message(message.chat.id,mention, parse_mode="Markdown")
                    x=threading.Thread(target=next_player, args=(people[0],message.chat.id))
                    x.start()
                elif len(people)==1:
                    bot.send_message(message.chat.id, 'Игра завершена!')
                    filepeople_words=open(str(message.chat.id)+'.txt','w')
                    filepeople=open(str(message.chat.id)+'people.txt','w')
                    filewords=open(str(message.chat.id)+'words.txt','w')
                    filepeople_words.close()
                    filepeople.close()
                    filewords.close()
            elif real_ques[len(real_ques)-1]=='?':
                f=open(str(message.chat.id)+'id.txt','r')
                idpeople=f.readlines()
                f.close()
                people[1]='!'+people[1]
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text='Да',callback_data="yes"))
                markup.add(types.InlineKeyboardButton(text='Нет',callback_data="no"))
                markup.add(types.InlineKeyboardButton(text='Посмотреть слово',callback_data="who")) 
                single_msg = types.InlineQueryResultArticle(id="1", title="Press me",
                input_message_content=types.InputTextMessageContent(message_text=real_ques),
                reply_markup=markup)
                mention = "["+people[2][:-1]+"](tg://user?id="+str(people[1][1:-1])+")"
                msg=bot.send_message(message.chat.id,mention+':'+real_ques, reply_markup=markup,parse_mode="Markdown")
                filepeople_words=open(str(message.chat.id)+'.txt','w')
                people[0]=str(time.time())+'\n'
                filepeople_words.writelines(people)
                filepeople_words.close()
                x=threading.Thread(target=next_move, args=(people,message.chat.id,msg))
                x.start()
    except:
        pass
        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        add_answer=True
        filepeople_words=open(str(call.message.chat.id)+'.txt','r')
        people=filepeople_words.readlines()
        filepeople_words.close()
        if len(people)>0:
            if call.message:
                if call.from_user.id==int(people[1][1:]):
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Нельзя отвечать на свои вопросы!')   
                else:
                    if call.data=="who":
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=people[3])
                    else:
                        file_answer = open(str(call.message.chat.id)+'answerid.txt','r')
                        answer_people=file_answer.readlines()
                        file_answer.close()
                        for i in range (len(answer_people)):
                            if call.from_user.id==int(answer_people[i]):
                                add_answer=False
                        if add_answer:
                            if call.from_user.id==int(people[1][1:]):
                                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Нельзя отвечать на свои вопросы!')       
                            else:
                                file_answer = open(str(call.message.chat.id)+'answerid.txt','a')
                                file_answer.write(str(call.from_user.id)+'\n')
                                file_answer.close()
                                if call.message:
                                    f=open(str(call.message.chat.id)+'answer.txt','r')
                                    answer=f.readlines()
                                    f.close()
                                    ans_yes=int(answer[0])
                                    ans_no=int(answer[1])
                                    f=open(str(call.message.chat.id)+'answer.txt','w')
                                    if call.data == "yes":
                                        ans_yes=int(answer[0])+1
                                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Ваш ответ:да')
                                    elif call.data=="no":
                                        ans_no=int(answer[1])+1
                                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Ваш ответ:нет')
                                    f.writelines(str(ans_yes)+'\n'+str(ans_no))
                                    f.close()
                        else:
                            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Вы уже проголосовали')
    except:
        pass

def next_move(people,chat,message):
    try:
        file_id=open(str(chat)+'answerid.txt','w')
        file_id.close()
        time.sleep(30)
        mess=message.text
        file_answer = open(str(chat)+'answer.txt','r')
        answer=file_answer.readlines()
        file_answer.close()
        bot.send_message(int(people[1][1:-1]),message.text[mess.find(':')+1:]+'\n'+'Да-'+str(answer[0])+'Нет-'+str(answer[1]))
        filepeople_words=open(str(chat)+'.txt','w')
        people.append(people[1][1:])
        people.append(people[2])
        people.append(people[3])
        del people[1]
        del people[1]
        del people[1]
        people[0]=str(time.time())+'\n'
        filepeople_words.writelines(people)
        filepeople_words.close()
        bot.delete_message(chat,message.message_id)
        mention = 'Ход игрока '+"["+people[2]+"](tg://user?id="+str(people[1][:-1])+")"
        bot.send_message(message.chat.id,mention, parse_mode="Markdown")
        x=threading.Thread(target=next_player, args=(people[0],chat))
        x.start()
        file_answer = open(str(chat)+'answer.txt','w')
        file_answer.write('0'+'\n'+'0')
        file_answer.close()
    except:
        pass

def next_player(timest,chat):
    try:
        time.sleep(40)
        filepeople_words=open(str(chat)+'.txt','r')
        people=filepeople_words.readlines()
        filepeople_words.close()
        if len(people)>0:
            if float(timest)==float(people[0]):
                filepeople_words=open(str(chat)+'.txt','w')
                people.append(people[1])    
                people.append(people[2]) 
                people.append(people[3])
                del people[1]
                del people[1]
                del people[1]
                people[0]=str(time.time())+'\n'
                filepeople_words.writelines(people)
                filepeople_words.close()
                mention = 'Ход игрока '+"["+people[2]+"](tg://user?id="+str(people[1][:-1])+")"
                bot.send_message(chat,mention, parse_mode="Markdown")
                x=threading.Thread(target=next_player, args=(people[0], chat))
                x.start()
    except:
        pass
    
@bot.message_handler(content_types=['text'])
def send_word(message,s=' ',user_id=' ',user_firstname=' ',k=0,first_word=' '):
    try:
        if str(s)==' ' and str(user_id)==' ' and user_firstname==' ':
            return 
        else:
            if message.from_user.id==user_id and message.text[0]!='/' and len(message.text)>2:
                if k==1:
                    f=open(str(s)+'words.txt','a')
                    f.write(first_word+'\n'+message.text+'\n')
                    f.close()
                    filepeople_words=open(str(s)+'.txt','r')
                    people_words=filepeople_words.readlines()
                    filepeople_words.close()
                    if len(people_words)==0:
                        f=open(s+'people.txt','a')
                        f.write(str(user_id)+'\n')
                        f.write(user_firstname+'\n')
                        f.close()
                        fid=open(str(s)+'id.txt','a')
                        fid.write(str(message.chat.id)+'\n')
                        fid.close()
                    else:
                        filewords=open(s+'words.txt','r')
                        words=filewords.readlines()
                        filewords.close()
                        ran=random.randint(0,len(words)-3)
                        filepeople_words=open(str(s)+'.txt','a')
                        filepeople_words.write(str(user_id)+'\n')
                        filepeople_words.write(user_firstname+'\n')
                        filepeople_words.write(words[ran])
                        filepeople_words.close()
                        fwords=open(str(s)+'words.txt','w')
                        words.pop(ran)
                        fwords.writelines(words)
                        fwords.close()
                        fid=open(str(s)+'id.txt','r')
                        idpeople=fid.readlines()
                        add=True
                        for i in range(len(idpeople)):
                            if int(idpeople[i])==int(message.chat.id):
                                add=False
                        fid.close()
                        mention = "["+user_firstname+"](tg://user?id="+str(user_id)+")"
                        bot.send_message(s,mention+" присоединился к игре.",parse_mode="Markdown")
                        if add:
                            fid=open(str(s)+'id.txt','a')
                            fid.write(str(message.chat.id)+'\n')
                            fid.close()
                    bot.send_message(message.chat.id,"Вы добавлены в игру.")
                    return
                else:
                    word=message.text
                    a=bot.register_next_step_handler(message,lambda message:send_word(message,s,user_id,user_firstname,1,word))
                return
            else:
                bot.send_message(message.chat.id,"Попробуйте другое слово")
                a=bot.register_next_step_handler(message,lambda message:send_word(message,s,user_id,user_firstname,k,first_word))
                return
    except:
        pass


bot.polling()
