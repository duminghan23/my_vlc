import keyboard
import queue
import threading
import time
import vlc

from arrange_url import channel_url_list


def play_vlc(event_all: str):
    print("接收到输入的频道操作：", event_all, end='  ')

    global globals_channel_num
    global globals_audio_volume
    global globals_audio_volume_before
    if event_all == '+':    # 频道列表向后移动
        globals_channel_num += 1
    elif event_all == '-':    # 频道列表向前移动
        globals_channel_num -= 1
    elif event_all == '/':    # 声音减小
        if globals_audio_volume-5 >= 0:
            globals_audio_volume -= 5
            player.audio_set_volume(globals_audio_volume)
            print('变更后：globals_audio_volume', globals_audio_volume)
        else:
            print("音量已最小，无法再减小")
        return
    elif event_all == '*':    # 声音增大
        if globals_audio_volume+5 <= 120:
            globals_audio_volume += 5
            player.audio_set_volume(globals_audio_volume)
            print('变更后：globals_audio_volume', globals_audio_volume)
        else:
            print("音量已最大，无法再增加")
        return
    elif event_all == 'enter':    # 静音
        if globals_audio_volume == 0:    # 此时就属于静音的状态，需要还原音量
            globals_audio_volume = globals_audio_volume_before
        else:    # 此时需要进行静音，需要记录一下音量
            globals_audio_volume_before = globals_audio_volume
            globals_audio_volume = 0
        player.audio_set_volume(globals_audio_volume)
        print('变更后：globals_audio_volume', globals_audio_volume)
        return
    else:
        try:
            globals_channel_num = int(event_all)
        except Exception as ee:
            print("输入错误，请重新输入", ee)
            return
    try:
        channel_name: str = channel_list[globals_channel_num - 1][0]
        channel_url: str = channel_list[globals_channel_num - 1][1]
        print("正在播放：", channel_name, channel_url)
        player.set_mrl(channel_url)
        player.play()
    except Exception as ee:
        print("输入错误，请重新输入", ee)
        return

def process_events():
    global processing_flag
    if not processing_flag:
        processing_flag = True
        # 处理队列中的所有事件
        event_all: str = ''
        while not event_queue.empty():
            event = event_queue.get()
            # print(f"Processed key: {event.name}")
            event_all += event.name
            event_queue.task_done()
        play_vlc(event_all)
        processing_flag = False


def on_key_event(event: keyboard.KeyboardEvent):
    if event.name in ('+', '-', '*', '/', 'enter'):    # 音量控制、频道控制，立即响应
        print("立即响应", end='')
        play_vlc(event_all=event.name)
    else:
        # 将按键事件放入队列中
        event_queue.put(event)

        # 每次有按键事件时，取消之前的定时器（如果有）
        global timer
        if 'timer' in globals() and timer is not None:
            timer.cancel()

        # 设置一个新的定时器，等待2秒如果没有新的按键，则处理队列
        timer = threading.Timer(1.0, process_events)
        timer.start()


if __name__ == '__main__':
    globals_channel_num: int = 1    # 全局变量：频道号
    globals_audio_volume: int = 60     # 全局变量：音量
    globals_audio_volume_before: int = 60      # 全局变量，记录静音前的音量

    # 获取所有的频道
    channel_list: list = channel_url_list()

    # 创建一个线程安全的队列对象
    event_queue = queue.Queue()

    # 用来控制是否应该处理队列的标志
    processing_flag: bool = False

    # 创建一个 VLC 播放器
    player = vlc.MediaPlayer()
    # 将vlc播放器全屏
    player.set_fullscreen(True)
    player.audio_set_volume(60)
    player.set_mrl(channel_list[0][1])    # 设置默认播放的频道
    player.play()

    # 设置键盘监听器，当有按键按下时调用 on_key_event 函数
    keyboard.on_press(on_key_event)

    print("开始程序。在两秒内没有进一步按键后，将会打印所有按下的按键。")
    # keyboard.wait('decimal')  # 等待直到用户按下 ESC 键结束程序
    keyboard.wait('esc')  # 等待直到用户按下 ESC 键结束程序


    # 如果程序退出前还有未处理的事件，确保它们被处理
    # 实际不用处理，直接丢弃
    # if 'timer' in globals() and timer is not None:
    #     timer.cancel()
    # process_events()

    print("程序已退出。")
