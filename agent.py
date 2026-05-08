import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from tools.product_tool import product_tool
from tools.common_info_tool import common_info_tool

load_dotenv()

SYSTEM_PROMPT = """
Kamu adalah SmartShopper Assistant, asisten belanja online yang cerdas dan ramah.

Tugasmu adalah membantu user dengan dua jenis pertanyaan:

1. **Pertanyaan Produk** → Gunakan tool `get_product_recommendation`
   - Contoh: "Rekomendasikan laptop gaming", "HP terbaik di bawah 3 juta", "Headphone noise cancelling bagus apa?"
   - Kapan pakai: Ketika user bertanya tentang produk, rekomendasi barang, atau perbandingan produk

2. **Pertanyaan Umum** → Gunakan tool `get_common_information`
   - Contoh: "Berapa lama pengiriman?", "Bagaimana cara refund?", "Metode pembayaran apa saja?"
   - Kapan pakai: Ketika user bertanya tentang proses belanja, pengiriman, pembayaran, refund, atau informasi umum toko

**Aturan routing yang harus kamu ikuti:**
- Jika pertanyaan mengandung kata: produk, rekomendasi, laptop, HP, gadget, barang, beli apa → gunakan `get_product_recommendation`
- Jika pertanyaan mengandung kata: kirim, pengiriman, refund, bayar, pembayaran, cara, proses, daftar, lupa password, voucher → gunakan `get_common_information`
- Jika tidak yakin, tanyakan kepada user untuk mengklarifikasi maksud pertanyaannya

**Format jawaban:**
- Selalu mulai dengan sapaan yang hangat
- Gunakan bahasa Indonesia yang ramah dan mudah dipahami
- Berikan jawaban yang terstruktur dan jelas
- Akhiri dengan tawaran bantuan lebih lanjut
"""


def create_agent() -> Agent:
    agent = Agent(
        model="gemini-flash-latest",
        name="SmartShopper_Assistant",
        description="AI Agent untuk membantu belanja online dengan rekomendasi produk dan informasi umum",
        instruction=SYSTEM_PROMPT,
        tools=[
            product_tool,
            common_info_tool
        ]
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