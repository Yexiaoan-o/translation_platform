import asyncio
from openai import AsyncOpenAI
import logging

logger = logging.getLogger("uvicorn.error")

class LLMTranslator:
    def __init__(self):
        # 针对 Ollama 的本地配置
        self.client = AsyncOpenAI(
            api_key="ollama", # Ollama 不需要密钥，填任意字符串即可
            base_url="http://localhost:11434/v1" # Ollama 的 OpenAI 兼容接口地址
        )
        self.model_name = "translategemma:4b" # 确保这与你 ollama list 看到的名称一致
        logger.info(f"LLMTranslator 已配置为本地 Ollama 模式 (模型: {self.model_name})")

    async def translate_single_segment(self, semaphore, segment, target_lang):
        async with semaphore:
            try:
                # 针对翻译模型的 Prompt 优化
                # TranslateGemma 在特定的指令下表现更好
                prompt = f"Translate the following text to {target_lang}. Only provide the translation, no explanation:\n\n{segment['source']}"
                
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    # 降低超时限制，因为本地运行大模型可能比云端 API 慢
                    timeout=60.0 
                )
                
                translated_text = response.choices[0].message.content.strip()
                
                # 记录一下本地翻译的进度
                logger.info(f"Ollama 翻译完成: Seg {segment['id']}")
                
                return {
                    "id": segment["id"],
                    "source": segment["source"],
                    "target": translated_text
                }
            except Exception as e:
                logger.error(f"Ollama 翻译失败 (Seg {segment['id']}): {e}")
                return {**segment, "target": ""}

    async def translate_segments_concurrency(self, segments: list, target_lang: str = "英文"):
        if not segments:
            return []
        
        # 【重要】本地运行大模型时，建议将并发数调低
        # 如果你的显存（VRAM）不是特别大，建议设为 1 或 2，防止内存溢出导致系统崩溃
        semaphore = asyncio.Semaphore(2) 
        
        tasks = [self.translate_single_segment(semaphore, seg, target_lang) for seg in segments]
        results = await asyncio.gather(*tasks)
        return results