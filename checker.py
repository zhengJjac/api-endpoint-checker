import asyncio
import time
import httpx
from typing import Dict, Any

async def check_endpoint(base_url: str, api_key: str, timeout: float = 10.0) -> Dict[str, Any]:
    """检测 OpenAI 兼容接口的连通性、TTFT 延迟及可用模型数量"""
    url = f"{base_url.rstrip('/')}/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    start_time = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, headers=headers)
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            if response.status_code == 200:
                data = response.json()
                models = [m.get("id") for m in data.get("data", [])]
                return {
                    "status": "online",
                    "latency_ms": latency_ms,
                    "model_count": len(models),
                    "sample_models": models[:5]
                }
            return {
                "status": "error",
                "http_code": response.status_code,
                "latency_ms": latency_ms,
                "detail": response.text[:150]
            }
    except Exception as exc:
        return {
            "status": "unreachable",
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 2),
            "error": str(exc)
        }

async def main():
    # 示例调用：替换为实际需要巡检的网关地址与测试 Key
    target_url = "https://api.openai.com"
    test_key = "sk-placeholder-key"
    result = await check_endpoint(target_url, test_key)
    print(f"Endpoint Check Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())