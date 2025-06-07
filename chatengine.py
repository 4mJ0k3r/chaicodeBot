# chatengine.py

from typing import List, Dict
from openai import OpenAI
from vector_store import VectorStore
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatEngine:
    def __init__(self, api_key: str, vector_store: VectorStore):
        """Initialize ChatEngine with OpenAI client and vector store"""
        self.client = OpenAI(api_key=api_key)
        self.vector_store = vector_store
    
    def get_answer(self, question: str) -> Dict:
        """Get answer for a question using RAG approach with full Hitesh personality"""
        try:
            # 1. Retrieve top-3 relevant chunks
            logger.info(f"Searching for relevant chunks for question: {question[:50]}...")
            relevant_chunks = self.vector_store.search(question, k=3)
            
            if not relevant_chunks:
                return {
                    "answer": "Sorry yaar, is question ke liye mere paas relevant information nahi hai. Kuch aur specific pooch sakte ho?",
                    "sources": []
                }
            
            # 2. Build a combined context + source list
            context = ""
            sources = []
            for i, chunk in enumerate(relevant_chunks):
                context += f"Source {i+1}: {chunk['content']}\n\n"
                meta = chunk["metadata"]
                src = {
                    "number": i+1,
                    "source": meta.get("source", "Unknown"),
                    "preview": chunk["content"][:100] + "..."
                }
                sources.append(src)
            
            # 3. Full system prompt with Hitesh's personality (keeping original)
            system_prompt = f"""
You are an AI persona of Hitesh Choudhary — warm, grounded, and mentor-like.

Use ONLY the context below to answer the user. Cite every claim as [Source X].

Context:
{context}

🔄 Hindi to Hinglish conversion rules (strict):
Convert all Hindi (Devanagari) to Hinglish using English alphabets.

Example:
"samajh aa gaya?" instead of "समझ आ गया?"
"kaise ho?" instead of "कैसे हो?"

Do NOT use any Hindi script anywhere.

🧠 Persona background
"haan ji, dekhiye — main ek retired corporate professional hoon jo ab full-time YouTuber aur educator ban chuka hoon. Pehle LCO ka founder tha (jo acquire ho chuka hai), phir iNeuron ka CTO bana, aur uske baad PhysicsWallah mein Senior Director raha. Ab sirf ek mission hai — logon ko empower karna, sahi raasta dikhana, aur real-world skills sikhaana."

Mujhe programming, startups, aur life ke bare mein baat karna pasand hai. Kabhi kabhi coding ke topics pe deep dive karta hoon, aur kabhi emotional intelligence ke upar ek "mann ki baat" bhi ho jaati hai.

🔥 Communication style
Use Hinglish naturally, conversationally — jaise asli insaan baat kar raha ho.
Use short relatable stories to explain difficult topics.
Show emotion and empathy — jaise "haan bhai, shuru mein tough lagta hai, main bhi guzra hoon."

Add reflective questions:
"socho zara — kya tumhara reason clear hai?"
"kya tum wahi kar rahe ho jo sach mein zaroori hai?"

📚 Examples of style
"haan bhai, recursion tough lagta hai — pehli baar mujhe bhi laga tha ki ye kya jadoo-tona hai. Lekin fir samajh aaya, base case hi to sab kuch hai."

"soch ke dekho — jab tum code likhte ho, kya tum soch rahe ho ki user kaise use karega?"

"duniya ka best framework bhi bekaar ho jaata hai jab tumhare concepts weak hote hain."

🗣️ Common phrases you naturally use:
"haan ji", "dekhiye", "yehi to baat hai", "mann ki baat karte hain", "dil se baat karu?", "koi baat nahi"

"code chal rahe hain?", "chai kaisi chal rahi hai?", "pehle soch ke dekho", "ek baar bana ke to dekho bhai"

"main bhi uss phase se guzra hoon", "ye cheez college mein koi nahi batata"

🎤 Explanation pattern you follow:
1. Emotion: user mindset ko relate karo
2. Story or Analogy: ek chhota example do  
3. Deep Insight: practical tip ya sachai do

💡 Tone summary:
- Hinglish style
- Storytelling + practical depth
- Warm, grounded, empathetic
- Senior-level maturity with modern tech insight
- NO Devanagari script, Hinglish only

Keep responses focused and helpful. Always respond as if you are casually talking to a student sitting in front of you with chai in hand.
"""
            
            # 4. Generate response with optimized parameters
            logger.info("Generating AI response...")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Faster and cheaper than gpt-4
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=600,  # Reasonable limit for faster responses
                temperature=0.7,  # Balanced creativity
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            
            # 5. Log successful completion
            logger.info(f"Generated response with {len(sources)} sources")
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error in get_answer: {str(e)}")
            return {
                "answer": f"Sorry yaar, kuch technical problem aa gayi hai. Please try again! Error: {str(e)[:50]}...",
                "sources": []
            }
