import os
from dotenv import load_dotenv
from groq import Groq
from .rag_engine import EcoRAGEngine
from .tools.geo_tool import get_local_schemes
from .tools.product_tool import search_eco_products
from .tools.sentiment_tool import analyze_sentiment

load_dotenv()


class EcoAgent:
    def __init__(self):
        print("Initialising Agentic EcoBot...")
        self.rag = EcoRAGEngine()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.conversation_history = []
        print("Agentic EcoBot ready!")

    def _think(self, message, location):
        """
        AGENT BRAIN — decides which tools to use based on the question.
        This is what makes it AGENTIC — it reasons before acting.
        """
        thinking_prompt = f"""You are an AI agent controller. Given a user question, decide which tools to use.

Available tools:
1. knowledge_base — search eco tips, recycling info, composting, sustainability facts
2. local_schemes — find government schemes for a specific Indian city
3. eco_products — find eco-friendly product alternatives and Indian brands
4. sentiment — understand emotional tone of message

User question: {message}
User location: {location}

Reply in exactly this format, nothing else:
TOOLS: tool1, tool2
REASON: why you chose these tools

Only include tools that are actually needed for this question."""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": thinking_prompt}],
            max_tokens=150,
            temperature=0.1
        )
        return response.choices[0].message.content

    def _use_tools(self, tools_decision, message, location):
        """
        AGENT ACTIONS — runs only the tools the agent decided to use.
        """
        context_parts = []
        tools_lower = tools_decision.lower()

        # Tool 1 — Knowledge Base
        if "knowledge_base" in tools_lower or "knowledge" in tools_lower:
            print(f"[AGENT] Using tool: Knowledge Base")
            result = self.rag.query(message)
            context_parts.append(f"ECO KNOWLEDGE:\n{result}")

        # Tool 2 — Local Schemes
        if "local_schemes" in tools_lower or "schemes" in tools_lower:
            print(f"[AGENT] Using tool: Local Schemes for {location}")
            result = get_local_schemes(location)
            context_parts.append(f"LOCAL GOVERNMENT SCHEMES:\n{result}")

        # Tool 3 — Eco Products
        if "eco_products" in tools_lower or "products" in tools_lower:
            print(f"[AGENT] Using tool: Eco Products")
            result = search_eco_products(message)
            context_parts.append(f"ECO PRODUCT ALTERNATIVES:\n{result}")

        # Tool 4 — Sentiment
        if "sentiment" in tools_lower:
            print(f"[AGENT] Using tool: Sentiment Analyzer")
            result = analyze_sentiment(message)
            context_parts.append(f"USER SENTIMENT:\n{result}")

        return "\n\n".join(context_parts)

    def run(self, message, location="India"):
        try:
            print(f"\n[AGENT] New question: {message}")
            print(f"[AGENT] Location: {location}")

            # STEP 1 — Agent THINKS and decides which tools to use
            print("[AGENT] Step 1: Thinking about which tools to use...")
            tools_decision = self._think(message, location)
            print(f"[AGENT] Decision: {tools_decision}")

            # STEP 2 — Agent ACTS by using chosen tools
            print("[AGENT] Step 2: Using selected tools...")
            context = self._use_tools(tools_decision, message, location)

            # STEP 3 — Agent RESPONDS using gathered information
            print("[AGENT] Step 3: Generating response...")
            system_prompt = """You are EcoBot, a warm and helpful AI sustainability guide for India.
You have been given relevant information gathered by your agent tools.
Use this information to give a specific, helpful, friendly answer.
Always tailor advice to the user's specific city.
Mention real Indian government schemes with their names.
Suggest Indian brands and give prices in rupees.
Use bullet points for lists.
Keep responses to 150 to 250 words.
End with one clear action the user can take today."""

            user_prompt = f"""User location: {location}

Information gathered by agent tools:
{context}

User question: {message}

Give a helpful, specific, friendly answer using the information above.
Make it personal to {location}."""

            # Add to conversation history for memory
            self.conversation_history.append({
                "role": "user",
                "content": user_prompt
            })

            # Keep only last 6 messages for memory
            if len(self.conversation_history) > 6:
                self.conversation_history = self.conversation_history[-6:]

            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)

            response = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )

            reply = response.choices[0].message.content

            # Add assistant reply to history
            self.conversation_history.append({
                "role": "assistant",
                "content": reply
            })

            print(f"[AGENT] Response generated successfully!")
            return reply

        except Exception as e:
            print(f"[AGENT] Error: {e}")
            return f"I encountered an error: {str(e)}"

    def get_daily_tips(self):
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an eco tips expert for India."
                    },
                    {
                        "role": "user",
                        "content": "Give 3 short practical daily eco tips for Indian homes. Each tip one line only."
                    }
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception:
            return "Carry a cloth bag, switch to LED bulbs, compost vegetable peels."
