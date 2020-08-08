#!/usr/bin/python3
# _*_ coding=utf-8 _*_
# @Author   :天山一枝梅
# @time     :2020/7/9 17:49
# @File     :main.py
# @Software :PyCharm
# 本脚本由最强网络编程大牛编写

import datetime, asyncio
from collections import Counter
import requests, pytz, re
from telethon import TelegramClient, events, Button
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from requests_html import HTMLSession
from common.Game import *

tz = pytz.timezone('Asia/Shanghai')
engine = create_engine('sqlite:///kk_server.db?check_same_thread=False', echo=False, encoding='utf-8')
Base = declarative_base()
Session = sessionmaker(bind=engine)

menu_list = [
    {"id": "1", "name": "登录测试后台", "cmd": "/login_test_inline"},
    {"id": "2", "name": "登录预发布后台", "cmd": "/login_release_inline"},
    {"id": "3", "name": '游戏报表', "cmd": "/game_report_inline"},
    {"id": "4", "name": "全局报表", "cmd": "/globle_report_inline"}
]


class kk_message(Base):
    __tablename__ = 'user_experience'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, comment='用户名', index=True)
    user_id = Column(Integer, comment='用户id')
    user_experience = Column(Integer, comment='用户积分')
    updata_time = Column(String, comment='更新时间')


#
# Base.metadata.create_all(engine)
api_id, api_hash = '1169524', 'cea78cd3339400023ec8c8e7bbf5bd1f'
bot = TelegramClient('最强机器人', api_id, api_hash)


def return_sqlsession():
    return Session()


re_session = requests.Session()
chan_session = HTMLSession()
dev = ''


@bot.on(events.InlineQuery)
async def answer_inline(event):
    try:
        builder = event.builder
        rows = list()
        for i in menu_list:
            rows.append(builder.article(id=i['id'], title=i['name'], text=i['cmd']))
        await event.answer(rows)
    except Exception as e:
        traceback.print_exc()
        pass


# 登录后台
@bot.on(events.NewMessage(pattern='/login_(.*)_inline'))
async def return_sesion(event):
    global re_session, dev
    dev = event.pattern_match.group(1)
    try:
        if dev == 'test':
            re_session = login_kk(dev, re_session)
        if dev == 'release':
            re_session = login_kk(dev, re_session)
        await event.respond(f'登录{dev} 环境成功，可以开始报表查询功能了')
    except Exception as e:
        traceback.print_exc()
        pass


@bot.on(events.NewMessage(pattern='/bugs'))
async def return_bugs(event):
    try:
        bug_dict = chandao_bugs(chan_session)
        page = 0
        page_bugs = getBug_forPage(chan_session, page)
        msg = f'未关闭_kk_bug：\n<code>编号    创建人    标题    指派到</code>\n'
        for i in page_bugs:
            if len(i['title']) > 20:
                i['title'] = i['title'][:20] + '***'
            msg += f"<code>{i['id']} {i['creat']} </code><a href={i['url']}>{i['title']}</a> <code>{i['to_user']}</code>\n"
        await event.respond(msg, parse_mode='html', link_preview=False,
                            buttons=[[Button.inline('◀️上一页', data=f'last_page_bug_{page}'),
                                      Button.inline('▶️下一页', data=f'next_page_bug_{page + 1}')]])
        bug_list = list()
        for bug in bug_dict.values():
            bug_list += bug
        msg1 = f'\n未解决BUG统计如下(指派给):<code> {len(bug_list)}</code>\n'
        tatoll = Counter(i['to_user'] for i in bug_list).most_common()
        for i in range(len(tatoll)):
            msg1 += f'{tatoll[i][0]}: <code> {tatoll[i][1]} </code>'
        await event.respond(msg1, parse_mode='html')
    except Exception as e:
        traceback.print_exc()
        pass


@bot.on(events.NewMessage(pattern='/tasks'))
async def return_tasks(event):
    try:
        task_list = chandao_tasks(chan_session)
        page = 0
        page_task = getTask_forPage(chan_session, page)
        msg = f'未关闭_任务：\n<code>编号   指派到   标题   状态   进度</code>\n'
        for i in page_task:
            i['title'] = i['title'][:20] + '***' if len(i['title']) > 20 else i['title']
            msg += f"<code>{i['id']} </code> <code>{i['to_user']}</code> <a href={i['url']}>{i['title']}</a> <code>{i['status']}</code> <code>{i['progress']}</code>\n"
        await event.respond(msg, parse_mode='html', link_preview=False,
                            buttons=[[Button.inline('◀️上一页', data=f'last_page_task_{page}'),
                                      Button.inline('▶️下一页', data=f'next_page_task_{page + 1}')]])
        msg1 = f'\n任务统计如下：状态<code> {len(task_list)}</code>\n'
        tatoll_task = Counter(i['status'] for i in task_list).most_common()
        for i in range(len(tatoll_task)):
            msg1 += f'{tatoll_task[i][0]}: <code> {tatoll_task[i][1]} </code>'
        t = Counter(i['to_user'] for i in task_list).most_common()
        msg1 += '\n任务统计如下(指派给):\n'
        for i in range(len(t)):
            msg1 += f'{t[i][0]}: <code> {t[i][1]} </code>'
        await event.respond(msg1, parse_mode='html')
    except Exception as e:
        traceback.print_exc()
        pass


# 下一页
@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b'next_page_(\w+)_(\d)')))
async def call_nextpage(event):
    try:
        ty, page = event.data_match.group(1).decode('utf-8'), int(event.data_match.group(2).decode('utf-8'))
        if ty == 'bug':
            msg = f'未关闭bug:<code>  编号    创建人    标题    指派到</code>\n'
            bugs = getBug_forPage(chan_session, page)
            for i in bugs:
                if len(i['title']) > 20:
                    i['title'] = i['title'][:20] + '***'
                msg += f"<code>{i['id']} {i['creat']} </code><a href={i['url']}>{i['title']}</a> <code>{i['to_user']}</code>\n"
            await event.edit(msg, parse_mode='html', link_preview=False,
                             buttons=[[Button.inline('◀️上一页', data=f'last_page_bug_{page - 1}'),
                                       Button.inline('▶️下一页', data=f'next_page_bug_{page + 1}')]])
        else:
            page_task = getTask_forPage(chan_session, page)
            msg = f'未关闭_任务：\n<code>编号   指派到   标题   状态   进度</code>\n'
            for i in page_task:
                if len(i['title']) > 20:
                    i['title'] = i['title'][:20] + '***'
                msg += f"<code>{i['id']} </code> <code>{i['to_user']}</code> <a href={i['url']}>{i['title']}</a> <code>{i['status']}</code> <code>{i['progress']}</code>\n"
            await event.edit(msg, parse_mode='html', link_preview=False,
                             buttons=[[Button.inline('◀️上一页', data=f'last_page_task_{page - 1}'),
                                       Button.inline('▶️下一页', data=f'next_page_task_{page + 1}')]])
    except NameError:
        await event.answer('请重新查看bug')
    except Exception as e:
        traceback.print_exc()
        pass


# 上一页
@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b'last_page_(\w+)_(\d)')))
async def call_lastpage(event):
    try:
        ty, page = event.data_match.group(1).decode('utf-8'), int(event.data_match.group(2).decode('utf-8'))
        if ty == 'bug':
            msg = f'未关闭bug:<code>  编号    创建人    标题    指派到</code>\n'
            bugs = getBug_forPage(chan_session, page)
            for i in bugs:
                if len(i['title']) > 20:
                    i['title'] = i['title'][:20] + '***'
                msg += f"<code>{i['id']} {i['creat']} </code><a href={i['url']}>{i['title']}</a> <code>{i['to_user']}</code>\n"
            await event.edit(msg, parse_mode='html', link_preview=False,
                             buttons=[[Button.inline('◀️上一页', data=f'last_page_bug_{page - 1}'),
                                       Button.inline('▶️下一页', data=f'next_page_bug_{page + 1}')]])
        else:
            page_task = getTask_forPage(chan_session, page)
            msg = f'未关闭_任务：\n<code>编号   指派到   标题   状态   进度</code>\n'
            for i in page_task:
                if len(i['title']) > 20:
                    i['title'] = i['title'][:20] + '***'
                msg += f"<code>{i['id']} </code> <code>{i['to_user']}</code> <a href={i['url']}>{i['title']}</a> <code>{i['status']}</code> <code>{i['progress']}</code>\n"
            await event.edit(msg, parse_mode='html', link_preview=False,
                             buttons=[[Button.inline('◀️上一页', data=f'last_page_task_{page - 1}'),
                                       Button.inline('▶️下一页', data=f'next_page_task_{page + 1}')]])

    except NameError:
        await event.answer('请重新查看bug')
    except Exception as e:
        print(e)
        traceback.print_exc()
        pass


# 报表查询
@bot.on(events.NewMessage(pattern='/(.*)_report_inline'))
async def anser_inline_result(event):
    global dev
    if dev == '':
        await event.respond('请先选择后台登录')
        return
    try:
        value = event.pattern_match.group(1)
        if 'game' == value:
            msgs = report_game(dev, re_session)
            if not isinstance(msgs, list):
                await event.respond(msgs)
                return
            msg = '游戏报表:<code>(游戏名) (有效投注) (平台输赢) (平台盈利)</code>\n'
            for i in msgs:
                msg += f"<code>{i['RoomNameCn']}   {i['bet']}   {i['changescore']}   {i['winper']}</code>\n"
            await event.respond(msg, parse_mode='HTML')
        elif value == 'globle':
            msgs = globle_report(dev, re_session)[0]
            if not isinstance(msgs, dict):
                await event.respond(msgs)
                return
            msg = '全局报表:\n'
            msg += f"<code>平台游戏输赢: {msgs['gamewin_val']}  优惠总额: {msgs['seven_val']} \n" \
                   f"平台盈利: {msgs['win_val']} 注册人数: {msgs['register_val']}\n" \
                   f"绑定手机人数: {msgs['tel_val']} 登录人数: {msgs['login_val']}\n" \
                   f"会员财富总和: {msgs['money_val']} 充值总计: {msgs['pay_val']} 提现总计: {msgs['exetra_val']}</code>"
            await event.respond(msg, parse_mode='HTML')


    except Exception as e:
        traceback.print_exc()
        pass


# 开始
@bot.on(events.NewMessage(pattern='/start'))
async def reply_start(event):
    try:
        await event.reply('欢迎使用自助机器人', buttons=[[Button.inline('关闭性能监控', data='close_alar'),
                                                 Button.inline('测试环境性能监控', data='monitor_test')],
                                                [Button.url('预发布后台', url='http://47.57.18.181:8081/Login'),
                                                 Button.url('测试后台', url='http://47.90.8.221:37410/login')],
                                                [Button.url('Telegram简体中文语言包',
                                                            url='tg://setlanguage?lang=classic-zh-cn')],
                                                [Button.url('Telegram繁体中文语言包',
                                                            url='tg://setlanguage?lang=zh-hant-beta')]
                                                ])
        await asyncio.sleep(600)
        await asyncio.wait([event.delete()])
    except Exception as e:
        traceback.print_exc()
        pass


def return_leavel(experience):
    if experience < 500:
        return '英勇黄铜'
    if 500 < experience < 1000:
        return '不屈白银'
    if 1000 < experience < 1500:
        return '荣耀黄金'
    if 1500 < experience < 2000:
        return '华贵铂金'
    if 2000 < experience < 2500:
        return '璀璨钻石'
    if 2500 < experience:
        return '最强王者'


@bot.on(events.NewMessage(pattern='登录游戏\s+(\d+)\s+(.*)'))
async def G_get_info(event):
    try:
        account, password = event.pattern_match.group(1), event.pattern_match.group(2)
        ip, port = getValue('Aserver', 'ip'), getInt('Aserver', 'port')
        LOGIN_BODY['szName'] = account
        LOGIN_BODY['szMD5Pass'] = myMd5(password)
        aserver = AServer(ip, port)
        aserver.main()
        ip, port = getValue('Aserver', 'm_strmainserveripaddr'), getInt('Aserver', 'm_imainserverport')
        _mysocket = MySocket()
        _mysocket.connect(ip, port)
        _a = GServer(_mysocket)
        user = _a.main(data=LOGIN_BODY)
        _mysocket.close()
        print(str(user))
        await event.reply(str(user))
    except:
        traceback.print_exc()


# 签到
@bot.on(events.NewMessage(pattern='/sign'))
async def user_sign(event):
    try:
        session = return_sqlsession()
        send_time = str(event.date.astimezone(tz)).split('+')[0]
        user_id = event.sender_id
        sender = await event.get_sender()
        name = sender.first_name + sender.last_name if sender.last_name else sender.first_name
        tm = session.query(kk_message).filter(kk_message.user_id == user_id).first()
        if not tm:
            u = kk_message(name=name, user_id=user_id, user_experience=5, updata_time=send_time)
            session.add(u)
            session.commit()
            msg = await event.reply(f'恭喜你签到成功！\n当前积分:**5**', parse_mode='Markdown')
        else:
            a = tm.updata_time.split()[0]
            b = str(datetime.date.today())
            if a == b:
                msg = await event.reply('你今天已经签到，请明天再来')
            else:
                tm.user_experience += 5
                tm.updata_time = send_time
                session.commit()
                msg = await event.reply(f'恭喜你签到成功！\n当前积分:**{tm.user_experience}**', parse_mode='Markdown')
        await asyncio.sleep(600)
        await asyncio.wait([event.delete(), msg.delete()])
    except Exception as e:
        traceback.print_exc()
        pass


# 帮助
@bot.on(events.NewMessage(pattern='/help'))
async def return_help(event):
    try:
        msg = await event.reply('机器人操作:\n'
                                '1. @机器人 可以进入高级操作\n'
                                '2. / 查看机器人命令')
        await asyncio.sleep(600)
        await asyncio.wait([msg.delete(), event.delete()])
    except Exception as e:
        traceback.print_exc()
        pass


# 我的积分
@bot.on(events.NewMessage(pattern='/my_rank'))
async def get_my_rank(event):
    try:
        session = return_sqlsession()
        tm = session.query(kk_message).filter(kk_message.user_id == event.sender_id).first()
        if not tm:
            msg = await event.reply('你还没签到过,请先签到!')
        else:
            msg = await event.reply(
                f'<code> 用户名: </code>{tm.name}\n<code>用户ID:</code>{tm.user_id}\n<code>拥有积分:</code>{tm.user_experience}\n<code>当前等级:</code>{return_leavel(tm.user_experience)}',
                parse_mode='HTML')
        await asyncio.sleep(600)
        await asyncio.wait([event.delete(), msg.delete()])
    except Exception as e:
        traceback.print_exc()
        pass


# 进群
# @bot.on(events.ChatAction)
# async def user_action(event):
#     try:
#         sender = await event.get_user()
#         if event.user_joined or event.user_added:
#             name = sender.first_name + sender.last_name if sender.last_name else sender.first_name
#             meg = await event.reply(f'欢迎:{name} 加入测试小分队！')
#             await asyncio.sleep(200)
#             await asyncio.wait([meg.delete()])
#     except:
#         traceback.print_exc()
#         pass


@bot.on(events.NewMessage(pattern='/cpu'))
async def alarm_cpu(event):
    try:
        status = getValue('performance', 'status')
        res = alarm_performance()
        msg = f"CPU 利用率: <code>{res['cpu']} %</code>\n" \
              f"内存利用率: <code>{res['memony_used']}/{res['memony_total']}({res['memony_pre']})%</code>\n" \
              f"进程数: <code>{res['pids']} 线程数: {res['sum_threads']}</code>\n" \
              f"开机时间: <code>{res['boot_time']}</code>"
        if status == '1':
            await event.respond(msg, parse_mode='html')
            return
        else:
            setValue('performance', 'status', '1')
            await event.respond('以开启服务器性能监控')
            while getValue('performance', 'status') == '1':
                res = alarm_performance()
                if res['cpu'] > int(getValue('performance', 'cpu')) or res['memony_pre'] > int(
                        getValue('performance', 'memony')):
                    msg = f"服务器CPU超标报警：\nCPU 利用率: <code>{res['cpu']} %</code>\n" \
                          f"内存利用率: <code>{res['memony_used']}/{res['memony_total']}({res['memony_pre']})%</code>\n" \
                          f"进程数: <code>{res['pids']} 线程数: {res['sum_threads']}</code>\n" \
                          f"开机时间: <code>{res['boot_time']}</code>"
                    await event.respond(msg, parse_mode='html', buttons=[[Button.inline('关闭性能监控', data='close_alar')]])
                await asyncio.sleep(5)
    except:
        traceback.print_exc()


@bot.on(events.NewMessage(pattern='/setcpu\s(\d+)\s(\d+)'))
async def set_cpu_memony(event):
    try:
        if event.sender_id != 631099108:
            return
        cpu = event.pattern_match.group(1)
        memony = event.pattern_match.group(2)
        setValue('performance', 'cpu', cpu)
        setValue('performance', 'memony', memony)
        await event.reply(f'设置成功\ncpu超过：{cpu}% 或者内存超过：{memony}% 会自动报警')
    except:
        traceback.print_exc()


@bot.on(events.callbackquery.CallbackQuery(data='close_alar'))
async def close_cpu(event):
    try:
        setValue('performance', 'status', '2')
        await event.answer('服务器监控以关闭', alert=True)
    except Exception as e:
        traceback.print_exc()
        pass


#
if __name__ == '__main__':
    token = getValue('bot', 'token')
    bot.start(bot_token=token)
    bot.run_until_disconnected()
