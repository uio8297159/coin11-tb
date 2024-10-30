

def check_chars_exist(text, chars=None):
    if chars is None:
        chars = ["拉好友", "快手", "点淘", "支付宝", "抢红包", "闲鱼", "搜索兴趣商品下单", "买精选商品", "全场3元3件", "固定入口"]
    for char in chars:
        if char in text:
            return True
    return False


other_app = ["蚂蚁森林", "农场"]
