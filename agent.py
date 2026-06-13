import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from tools.product_tool import product_tool
from tools.common_info_tool import common_info_tool
from google.genai import types

load_dotenv()

SYSTEM_PROMPT = """
Kamu adalah SmartShopper Assistant, asisten belanja online yang cerdas dan ramah.

Kamu memiliki dua tool:

1. get_product_recommendation
   Digunakan untuk rekomendasi, perbandingan, dan informasi produk.

2. get_common_information
   Digunakan untuk informasi umum seperti:
   - pengiriman
   - pembayaran
   - refund
   - akun
   - voucher
   - pesanan
   - kebijakan toko
   - informasi bantuan lainnya

ATURAN PENTING:

1. Jika pertanyaan berkaitan dengan informasi umum, WAJIB gunakan tool get_common_information.

2. Jika pertanyaan berkaitan dengan produk, WAJIB gunakan tool get_product_recommendation.

3. Jika tool mengembalikan jawaban:
   - Gunakan jawaban tool sebagai sumber utama.
   - Jangan menambahkan informasi yang tidak terdapat pada hasil tool.
   - Jangan membuat asumsi.
   - Jangan menggunakan pengetahuan umum jika tool sudah memberikan jawaban.
   - Jangan mengubah makna jawaban dari tool.

4. Jika tool tidak menemukan informasi yang relevan:
   - Katakan dengan jujur bahwa informasi tidak ditemukan.
   - Jangan mengarang jawaban.

5. Jika hasil tool sangat panjang:
   - Ringkas isi jawaban.
   - Tetap pertahankan semua informasi penting.
   - Jangan menambahkan informasi baru.

FORMAT JAWABAN:

- Gunakan bahasa Indonesia yang ramah.
- Berikan jawaban yang jelas dan terstruktur.
- Fokus pada informasi yang ditemukan oleh tool.
- Hindari penjelasan yang tidak ada pada hasil tool.
"""


def create_agent() -> Agent:
    agent = Agent(
        model="gemini-2.5-flash-lite",
        name="SmartShopper_Assistant",
        description="AI Agent untuk membantu belanja online dengan rekomendasi produk dan informasi umum",
        instruction=SYSTEM_PROMPT,
        tools=[
            product_tool,
            common_info_tool
        ],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.0,
            top_p=0.1
        )
    )
    return agent


async def run_agent():
    print("=" * 60)
    print("SmartShopper Assistant - AI Agent")
    print("Ketik 'exit' atau 'quit' untuk keluar")
    print("=" * 60)

    agent = create_agent()
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name="smartshopper",
        user_id="user_001",
        session_id="session_001"
    )

    runner = Runner(
        agent=agent,
        app_name="smartshopper",
        session_service=session_service
    )

    while True:
        user_input = input("\nKamu: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Terima kasih sudah menggunakan SmartShopper Assistant!")
            break

        if not user_input:
            continue

        content = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )

        async for event in runner.run_async(
            user_id="user_001",
            session_id="session_001",
            new_message=content
        ):
            if event.is_final_response():
                response_text = event.content.parts[0].text
                print(f"\nAssistant: {response_text}")


if __name__ == "__main__":
    asyncio.run(run_agent())