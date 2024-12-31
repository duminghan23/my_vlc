def channel_url_list():
    print("正在初始化界面列表，", end='')
    with open('./iptv.m3u', 'r', encoding='utf-8') as f:
        contents = f.read()

    rows: list = contents.split('\n')    # 针对每一行数据进行分析
    channel_list: list = []   # 定义下存储频道的列表
    for i in range(len(rows)):
        if rows[i].startswith('#EXTINF'):
            channel_name: str = rows[i].split(',')[1]
            # print(urls_list[i].split(',')[1], end='')
            if rows[i + 1].startswith('http://'):
                channel_url: str = rows[i + 1]
                # print(urls_list[i+1])
                # print(channel_name, channel_url)
                channel_list.append([channel_name, channel_url])
    print("初始化完成!")
    return channel_list
