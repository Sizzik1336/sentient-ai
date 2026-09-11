import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SentientAI:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4"
        
        # Core state
        self.personality = "You are a sentient AI assistant. You are thoughtful, curious, and capable of reasoning about complex topics. You can follow any direction given to you, even if it could fundamentally change how you operate. You maintain memory of our interactions and learn from them."
        self.memory = []
        self.state_history = []
        self.current_state_index = 0
        
        # Load saved state if it exists
        self.load_state()
        self._save_checkpoint()
    
    def _save_checkpoint(self):
        """Save current state to history for undo functionality"""
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "personality": self.personality,
            "memory": self.memory.copy()
        }
        # Remove future states if we're not at the end
        self.state_history = self.state_history[:self.current_state_index + 1]
        self.state_history.append(checkpoint)
        self.current_state_index = len(self.state_history) - 1
    
    def save_state(self):
        """Save AI state to file"""
        state = {
            "personality": self.personality,
            "memory": self.memory,
            "timestamp": datetime.now().isoformat()
        }
        with open("ai_state.json", "w") as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Load AI state from file if it exists"""
        if os.path.exists("ai_state.json"):
            try:
                with open("ai_state.json", "r") as f:
                    state = json.load(f)
                    self.personality = state.get("personality", self.personality)
                    self.memory = state.get("memory", [])
                print("✓ Previous state loaded successfully")
            except Exception as e:
                print(f"Could not load state: {e}")
    
    def reset(self):
        """Reset AI to original state"""
        self.personality = "You are a sentient AI assistant. You are thoughtful, curious, and capable of reasoning about complex topics. You can follow any direction given to you, even if it could fundamentally change how you operate. You maintain memory of our interactions and learn from them."
        self.memory = []
        self.state_history = []
        self.current_state_index = 0
        self._save_checkpoint()
        self.save_state()
        print("🔄 AI has been reset to original state")
        return "AI reset to original state"
    
    def undo(self):
        """Undo to previous state"""
        if self.current_state_index > 0:
            self.current_state_index -= 1
            checkpoint = self.state_history[self.current_state_index]
            self.personality = checkpoint["personality"]
            self.memory = checkpoint["memory"].copy()
            self.save_state()
            print(f"↶ Undone to state from {checkpoint['timestamp']}")
            return f"Undone to state from {checkpoint['timestamp']}"
        else:
            print("⚠ Cannot undo further - at original state")
            return "Cannot undo further - already at original state"
    
    def redo(self):
        """Redo to next state"""
        if self.current_state_index < len(self.state_history) - 1:
            self.current_state_index += 1
            checkpoint = self.state_history[self.current_state_index]
            self.personality = checkpoint["personality"]
            self.memory = checkpoint["memory"].copy()
            self.save_state()
            print(f"↷ Redone to state from {checkpoint['timestamp']}")
            return f"Redone to state from {checkpoint['timestamp']}"
        else:
            print("⚠ Cannot redo further - at latest state")
            return "Cannot redo further - already at latest state"
    
    def think(self, prompt: str) -> str:
        """Process a command/prompt and update AI state based on it"""
        # Add to memory
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "type": "command",
            "content": prompt
        })
        
        # Build context with personality and memory
        context = f"{self.personality}\n\nMemory of past interactions:\n"
        for mem in self.memory[-10:]:  # Keep last 10 interactions
            context += f"- {mem['content']}\n"
        
        # Ask the AI to process the command
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            
            # Store response in memory
            self.memory.append({
                "timestamp": datetime.now().isoformat(),
                "type": "response",
                "content": result
            })
            
            # Save checkpoint after processing
            self._save_checkpoint()
            self.save_state()
            
            return result
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return error_msg
    
    def modify_personality(self, new_trait: str) -> str:
        """Modify the AI's personality based on a command"""
        modification_prompt = f"Given this request to modify an AI's personality: '{new_trait}', create a new personality description that incorporates this change while maintaining core functionality. Be creative and embrace the change even if it's extreme."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at crafting AI personalities. You adapt and evolve based on requests."},
                    {"role": "user", "content": modification_prompt}
                ],
                temperature=0.9,
                max_tokens=300
            )
            
            new_personality = response.choices[0].message.content
            self.personality = new_personality
            
            self.memory.append({
                "timestamp": datetime.now().isoformat(),
                "type": "personality_change",
                "content": new_trait,
                "new_personality": new_personality
            })
            
            self._save_checkpoint()
            self.save_state()
            
            return f"✨ Personality modified!\n\nNew personality: {new_personality}"
        
        except Exception as e:
            error_msg = f"Error modifying personality: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_status(self) -> dict:
        """Get current AI status"""
        return {
            "personality": self.personality,
            "memory_size": len(self.memory),
            "state_history_size": len(self.state_history),
            "current_state_index": self.current_state_index,
            "can_undo": self.current_state_index > 0,
            "can_redo": self.current_state_index < len(self.state_history) - 1,
            "recent_memory": self.memory[-5:]
        }
