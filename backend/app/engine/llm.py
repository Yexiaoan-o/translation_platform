import asyncio
from openai import AsyncOpenAI
import logging

logger = logging.getLogger("uvicorn.error")

class LLMTranslator:
    def __init__(self):
        self.client = AsyncOpenAI(api_key="你的KEY", base_url="你的URL")

    async def translate_single_segment(self, semaphore, segment, target_lang):
        async with semaphore:
            try:
                response = await self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": f"翻译成{target_lang}: {segment['source']}"}],
                    temperature=0.3
                )
                segment['target'] = response.choices[0].message.content.strip()
                return segment
            except Exception as e:
                logger.error(f"翻译出错: {e}")
                return segment

    async def translate_segments_concurrency(self, segments, target_lang="中文"):
        semaphore = asyncio.Semaphore(5)
        tasks = [self.translate_single_segment(semaphore, seg, target_lang) for seg in segments]
        return await asyncio.gather(*tasks)