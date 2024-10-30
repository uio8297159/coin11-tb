

def check_chars_exist(text):
    for char in ["拉好友", "快手", "点淘", "支付宝", "抢红包", "闲鱼", "蚂蚁", "搜索兴趣商品下单", "买精选商品", "全场3元3件", "固定入口"]:
        if char in text:
            return True
    return False
