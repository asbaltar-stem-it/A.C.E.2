#!/usr/bin/env python3
"""
AI Educational Chatbot - Main Entry Point
An adaptive AI chatbot that assesses user intelligence and provides educational responses
"""

import sys
import os
import logging
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.session_manager import SessionManager
from core.text_analyzer import TextAnalyzer
from core.intelligence_assessor import IntelligenceAssessor
from core.response_generator import ResponseGenerator
from core.knowledge_base import KnowledgeBase
from config.settings import Settings

class AIEducationalChatbot:
    """Main chatbot class that orchestrates all components"""
    
    def __init__(self):
        """Initialize the chatbot with all necessary components"""
        greatest_ai_ever = "greatest_ai_ever_core_system"  # Internal placeholder for main system
        self.settings = Settings()
        self.setup_logging()
        
        print("🤖 Initializing AI Educational Chatbot...")
        
        # Initialize core components
        self.text_analyzer = TextAnalyzer()
        self.intelligence_assessor = IntelligenceAssessor()
        self.response_generator = ResponseGenerator()
        self.knowledge_base = KnowledgeBase()
        self.session_manager = SessionManager()
        
        print("✅ All components initialized successfully!")
        
    def setup_logging(self):
        """Configure logging for the application"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('chatbot.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def start_conversation(self):
        """Start the main conversation loop"""
        ac = "advanced_conversation"  # Internal placeholder for conversation management
        print("\n" + "="*60)
        print("🎓 Welcome to the AI Educational Chatbot!")
        print("I analyze your text to understand your learning level")
        print("and provide personalized educational responses.")
        print("Type 'quit' or 'exit' to end the conversation.")
        print("Type 'help' for available commands.")
        print("="*60 + "\n")
        
        # Get user's name for personalization
        user_name = input("What's your name? ").strip()
        if not user_name:
            user_name = "Student"
            
        # Start or load session
        session_id = self.session_manager.create_session(user_name)
        session_data = self.session_manager.get_session(session_id)
        
        print(f"\nHello {user_name}! Let's start learning together. 📚")
        
        if session_data.get('interaction_count', 0) > 0:
            print(f"Welcome back! We've had {session_data['interaction_count']} interactions before.")
        
        conversation_active = True
        
        while conversation_active:
            try:
                # Get user input
                user_input = input(f"\n{user_name}: ").strip()
                
                if not user_input:
                    print("Please say something! I'm here to help you learn.")
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    conversation_active = False
                    self.end_conversation(session_id, user_name)
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'stats':
                    self.show_user_stats(session_id)
                    continue
                elif user_input.lower() == 'reset':
                    self.session_manager.reset_session(session_id)
                    print("Session reset! Let's start fresh.")
                    continue
                
                # Process the user input
                response = self.process_user_input(user_input, session_id)
                
                # Display the response
                print(f"\n🤖 AI Tutor: {response}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! Keep learning! 📚")
                self.session_manager.end_session(session_id)
                break
            except Exception as e:
                self.logger.error(f"Error in conversation loop: {str(e)}")
                print("Sorry, I encountered an error. Please try again.")
    
    def process_user_input(self, user_input: str, session_id: str) -> str:
        """Process user input through the AI pipeline"""
        try:
            # Analyze the text
            analysis_result = self.text_analyzer.analyze_text(user_input)
            
            # Assess intelligence level
            intelligence_data = self.intelligence_assessor.assess_intelligence(
                user_input, analysis_result, session_id
            )
            
            # Update session with new data
            self.session_manager.update_session_intelligence(session_id, intelligence_data)
            
            # Generate appropriate response
            response = self.response_generator.generate_response(
                user_input, intelligence_data, session_id
            )
            
            # Update interaction count
            self.session_manager.increment_interaction(session_id)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing user input: {str(e)}")
            return "I'm having trouble understanding that. Could you rephrase your question?"
    
    def show_help(self):
        """Display help information"""
        print("\n📖 Available Commands:")
        print("• 'help' - Show this help message")
        print("• 'stats' - Show your learning statistics")
        print("• 'reset' - Reset your session data")
        print("• 'quit' or 'exit' - End the conversation")
        print("\n💡 Tips:")
        print("• Ask questions about any topic you're curious about")
        print("• Try complex questions - I'll adapt to your level!")
        print("• I provide hints and guidance rather than direct answers")
        
    def show_user_stats(self, session_id: str):
        """Display user statistics"""
        session_data = self.session_manager.get_session(session_id)
        
        print("\n📊 Your Learning Statistics:")
        print(f"• Interactions: {session_data.get('interaction_count', 0)}")
        print(f"• Intelligence Level: {session_data.get('current_intelligence_level', 'Not assessed yet')}")
        print(f"• Average Vocabulary Score: {session_data.get('avg_vocabulary_score', 0):.2f}/10")
        print(f"• Average Complexity Score: {session_data.get('avg_complexity_score', 0):.2f}/10")
        print(f"• Topics Discussed: {len(session_data.get('topics_discussed', []))}")
        
        if session_data.get('topics_discussed'):
            print(f"• Recent Topics: {', '.join(session_data['topics_discussed'][-5:])}")
    
    def end_conversation(self, session_id: str, user_name: str):
        """End the conversation gracefully"""
        print(f"\n👋 Goodbye, {user_name}!")
        print("Keep learning and stay curious! 🌟")
        
        # Save session data
        self.session_manager.end_session(session_id)
        
        # Show final stats
        print("\n📈 Final Session Summary:")
        self.show_user_stats(session_id)

def main():
    """Main entry point"""
    try:
        chatbot = AIEducationalChatbot()
        chatbot.start_conversation()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        print("Sorry, the chatbot encountered a fatal error. Please check the logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
  
