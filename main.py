from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
import random
import os
from typing import List, Optional


@register("astrbot_plugin_qyws", "mingrixiangnai", "随机千原万神语音", "1.1", "https://github.com/mingrixiangnai/qyws")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.plugin_dir = os.path.abspath(os.path.dirname(__file__))  # 定位插件目录
        self.voice_dir = os.path.join(self.plugin_dir, "voice")  # 语音目录名字voice

    def _get_voice_files(self) -> List[str]:
        """获取语音文件列表"""
        try:
            return [f for f in os.listdir(self.voice_dir) if f.endswith('.mp3')]
        except OSError:
            return []

    def _get_voice_path(self, voice_name: str) -> Optional[str]:
        """获取语音文件完整路径"""
        voice_path = os.path.join(self.voice_dir, voice_name)
        return voice_path if os.path.exists(voice_path) else None
        
    @filter.regex(r".*千原万神.*")  # 匹配关键词
    async def wsde_handler(self, message: AstrMessageEvent):
        """千原万神 随机播放语音"""
        try:
            voice_files = self._get_voice_files()
            if not voice_files:
                yield message.plain_result("未找到语音文件")
                return

            # 随机选择语音
            voice_name = random.choice(voice_files)
            voice_path = self._get_voice_path(voice_name)
            
            if not voice_path:
                yield message.plain_result("语音文件不存在")
                return

            #yield message.plain_result(f"语音名：{voice_name[:-4]}")  # 定位文件名一起发送，如果不想发送可以把这行注释了
            async for msg in self.send_voice_message(message, voice_path):
                yield msg

        except Exception as e:
            yield message.plain_result(f"播放语音时出错：{str(e)}")

    async def send_voice_message(self, event: AstrMessageEvent, voice_file_path: str):
        """发送语音消息"""
        try:
            chain = [Record.fromFileSystem(voice_file_path)]
            yield event.chain_result(chain)
        except Exception as e:
            yield event.plain_result(f"发送语音失败：{str(e)}")
