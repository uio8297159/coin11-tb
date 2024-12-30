import time


def check_chars_exist(text, chars=None):
    if chars is None:
        chars = ["拉好友", "快手", "点淘", "抢红包", "闲鱼", "搜索兴趣商品下单", "买精选商品", "全场3元3件", "固定入口", "微博", "蚂蚁庄园", "农场小游戏", "支付宝农场", "支付宝芭芭农场", "砸蛋", "淘宝特价版", "福气提现金", "大众点评", "蚂蚁森林", "蚂蚁新村", "瑞幸", "支付宝会员", "消消乐", "玩一玩", "斗地主"]
    for char in chars:
        if char in text:
            return True
    return False


other_app = ["蚂蚁森林", "农场", "百度"]
