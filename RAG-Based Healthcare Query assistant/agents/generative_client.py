from groq import Groq

from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS
)

# =====================================================
# GROQ CLIENT
# =====================================================

client = Groq(
    api_key=GROQ_API_KEY
)

# =====================================================
# GENERATE CONTENT
# =====================================================

def generate_content(
    prompt: str,
    model: str = MODEL_NAME,
    temperature: float = TEMPERATURE
) -> str:

    try:

        response = client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Healthcare AI Assistant. "
                        "Answer accurately and follow the user's instructions."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=temperature,

            max_tokens=MAX_TOKENS,

            stream=False

        )

        if (
            not response.choices
            or response.choices[0].message is None
            or response.choices[0].message.content is None
        ):
            raise Exception("Empty response received from Groq.")

        return response.choices[0].message.content.strip()

    except Exception as e:

        raise Exception(
            f"Groq API Error:\n{e}"
        )

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Groq Client Test")
    print("=" * 60)

    try:

        answer = generate_content(
            "Say hello in one sentence."
        )

        print("\nResponse\n")
        print(answer)

    except Exception as e:

        print("\nError\n")
        print(e)