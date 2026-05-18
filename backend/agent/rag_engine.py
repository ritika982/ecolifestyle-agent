import os


class EcoRAGEngine:
    def __init__(self):
        print("Loading eco knowledge base...")
        self.knowledge = []
        knowledge_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "eco_knowledge")
        )
        self._load_documents(knowledge_dir)
        print(f"Loaded {len(self.knowledge)} knowledge chunks")

    def _load_documents(self, knowledge_dir):
        try:
            for filename in os.listdir(knowledge_dir):
                if filename.endswith(".txt"):
                    filepath = os.path.join(knowledge_dir, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        # split into chunks of 500 characters
                        chunks = [content[i:i+500] for i in range(0, len(content), 500)]
                        self.knowledge.extend(chunks)
            print(f"Loaded files from {knowledge_dir}")
        except Exception as e:
            print(f"Could not load files: {e}. Using fallback.")
            self._load_fallback()

    def _load_fallback(self):
        self.knowledge = [
            "Use cloth bags instead of plastic bags. Available for 30 to 50 rupees at any Indian market.",
            "Segregate waste into wet waste and dry waste as required by Swachh Bharat Mission.",
            "LED bulbs use 75 percent less electricity than CFL bulbs.",
            "PM Surya Ghar scheme gives 40 percent subsidy on rooftop solar panels.",
            "Composting vegetable peels at home creates free fertiliser in 45 to 60 days.",
            "FAME II scheme gives up to 1.5 lakh rupees subsidy on electric two-wheelers.",
            "E-waste like old phones must go to authorised collectors not regular dustbin.",
            "Fix dripping taps immediately as they waste 20 litres of water per day.",
        ]

    def query(self, question, n_results=4):
        try:
            # simple keyword search
            question_words = question.lower().split()
            scored = []
            for chunk in self.knowledge:
                score = sum(1 for word in question_words if word in chunk.lower())
                scored.append((score, chunk))
            scored.sort(reverse=True)
            top = [chunk for _, chunk in scored[:n_results] if chunk.strip()]
            return "\n\n".join(top) if top else "No specific knowledge found."
        except Exception as e:
            return f"Knowledge search error: {e}"