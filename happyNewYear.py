import time
from datetime import datetime
import random
import json
import logging
from wxauto import WeChat


class WeChatGreeting:
    def __init__(self):
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='wechat_greeting.log'
        )
        self.logger = logging.getLogger(__name__)

        # 初始化微信
        try:
            self.wx = WeChat()
            self.logger.info("微信初始化成功")
        except Exception as e:
            self.logger.error(f"微信初始化失败: {str(e)}")
            raise

    def load_friends(self, friends_file='friend.json'):
        """从JSON文件加载好友列表和对应的祝福语"""
        try:
            with open(friends_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"找不到好友配置文件: {friends_file}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"好友配置文件格式错误: {friends_file}")
            raise

    def send_greeting(self, friend_name, message):
        """发送单条祝福消息"""
        try:
            # 打开聊天窗口
            self.wx.ChatWith(friend_name)
            time.sleep(random.uniform(1, 2))  # 随机等待1-2秒

            # 发送消息
            self.wx.SendMsg(message)
            self.logger.info(f"成功发送祝福给 {friend_name}")

            # 随机等待5-10秒，避免发送过快
            time.sleep(random.uniform(5, 10))
            return True
        except Exception as e:
            self.logger.error(f"发送消息给 {friend_name} 失败: {str(e)}")
            return False

    def run_scheduled_greetings(self, start_time="2024-02-09 23:55:00"):
        """在指定时间开始发送祝福"""
        # 加载好友列表
        friends_data = self.load_friends()

        # 等待直到开始时间
        start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        while datetime.now() < start_datetime:
            time.sleep(1)

        self.logger.info("开始发送新年祝福")

        # 发送祝福
        success_count = 0
        fail_count = 0

        for friend in friends_data:
            if self.send_greeting(friend['name'], friend['message']):
                success_count += 1
            else:
                fail_count += 1

        # 输出统计信息
        self.logger.info(f"发送完成。成功: {success_count}, 失败: {fail_count}")
        return success_count, fail_count


if __name__ == "__main__":
    # 创建好友配置文件示例
    # sample_friends = [
    #     {"name": "张三", "message": "新年快乐！祝你在龙年事业腾飞，幸福安康！"},
    #     {"name": "李四", "message": "恭贺新春！愿你在新的一年里万事如意，阖家欢乐！"}
    # ]
    #
    # with open('friends.json', 'w', encoding='utf-8') as f:
    #     json.dump(sample_friends, f, ensure_ascii=False, indent=2)

    # 运行程序
    try:
        greeter = WeChatGreeting()
        greeter.run_scheduled_greetings("2025-01-28 20:00:00")
    except Exception as e:
        logging.error(f"程序运行出错: {str(e)}")
