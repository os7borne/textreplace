import json
import os
from typing import Dict
from pynput import keyboard
from pynput.keyboard import Key, Controller
import threading
from datetime import datetime

class TextReplacer:
    def __init__(self):
        self.replacements: Dict[str, dict] = {}  # Changed to store additional info
        self.config_file = "replacements.json"
        self.current_text = ""
        self.keyboard_controller = Controller()
        self.load_replacements()
        
    def load_replacements(self):
        """Load replacement rules and stats from JSON file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                # Convert old format if necessary
                if data and isinstance(next(iter(data.values())), str):
                    self.replacements = {
                        trigger: {
                            'text': replacement,
                            'usage_count': 0,
                            'last_used': None,
                            'created_at': datetime.now().isoformat()
                        } for trigger, replacement in data.items()
                    }
                    self.save_replacements()  # Save the converted format
                else:
                    self.replacements = data
    
    def save_replacements(self):
        """Save replacement rules and stats to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.replacements, f, indent=2)
    
    def add_replacement(self, trigger: str, replacement: str):
        """Add a new replacement rule"""
        self.replacements[trigger] = {
            'text': replacement,
            'usage_count': 0,
            'last_used': None,
            'created_at': datetime.now().isoformat()
        }
        self.save_replacements()
        print(f"Added replacement: '{trigger}' -> '{replacement}'")
    
    def remove_replacement(self, trigger: str):
        """Remove a replacement rule"""
        if trigger in self.replacements:
            del self.replacements[trigger]
            self.save_replacements()
            print(f"Removed replacement for '{trigger}'")
        else:
            print(f"No replacement found for '{trigger}'")
    
    def list_replacements(self):
        """List all replacement rules with stats"""
        if not self.replacements:
            print("No replacement rules defined")
            return
        
        print("\nCurrent replacement rules:")
        print("-" * 60)
        print(f"{'Trigger':<15} {'Replacement':<20} {'Uses':<8} {'Last Used'}")
        print("-" * 60)
        for trigger, data in self.replacements.items():
            replacement_preview = data['text'].split('\n')[0][:20]  # First line, up to 20 chars
            if len(data['text']) > 20 or '\n' in data['text']:
                replacement_preview += '...'
            last_used = 'Never' if not data['last_used'] else data['last_used'].split('T')[0]
            print(f"{trigger:<15} {replacement_preview:<20} {data['usage_count']:<8} {last_used}")
        print("-" * 60)
    
    def show_stats(self):
        """Show detailed statistics"""
        if not self.replacements:
            print("No statistics available - no replacements defined")
            return
            
        print("\nReplacement Statistics:")
        print("-" * 60)
        
        # Most used replacements
        sorted_by_usage = sorted(
            self.replacements.items(), 
            key=lambda x: x[1]['usage_count'], 
            reverse=True
        )
        
        print("Most Used Replacements:")
        for trigger, data in sorted_by_usage[:5]:  # Top 5
            print(f"  {trigger}: {data['usage_count']} uses")
        
        # Total uses
        total_uses = sum(data['usage_count'] for data in self.replacements.values())
        print(f"\nTotal Replacements Made: {total_uses}")
        
        # Recently used
        recently_used = sorted(
            [(trigger, data) for trigger, data in self.replacements.items() if data['last_used']],
            key=lambda x: x[1]['last_used'],
            reverse=True
        )
        if recently_used:
            print("\nRecently Used:")
            for trigger, data in recently_used[:3]:  # Last 3
                last_used = datetime.fromisoformat(data['last_used']).strftime('%Y-%m-%d %H:%M')
                print(f"  {trigger}: {last_used}")
        
        print("-" * 60)

    def on_press(self, key):
        """Handle key press events"""
        try:
            if hasattr(key, 'char') and key.char:  # Regular character
                self.current_text += key.char
            elif key == Key.space or key == Key.enter:  # Space or Enter
                for trigger, data in self.replacements.items():
                    if self.current_text == trigger:
                        # Update statistics
                        data['usage_count'] += 1
                        data['last_used'] = datetime.now().isoformat()
                        self.save_replacements()
                        
                        # Delete the trigger text plus the space/enter
                        for _ in range(len(trigger) + 1):
                            self.keyboard_controller.press(Key.backspace)
                            self.keyboard_controller.release(Key.backspace)
                        # Type the replacement
                        self.keyboard_controller.type(data['text'])
                        self.current_text = ""
                        return
                self.current_text = ""
            elif key == Key.backspace:  # Backspace
                if self.current_text:
                    self.current_text = self.current_text[:-1]
        except Exception as e:
            print(f"Error in key press handler: {e}")

    def start_monitoring(self):
        """Start keyboard monitoring"""
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        return listener

    def run(self):
        """Start the text replacer"""
        print("Text Replacer started!")
        print("Commands:")
        print("  add <trigger> <replacement> - Add a new replacement rule")
        print("  remove <trigger> - Remove a replacement rule")
        print("  list - List all replacement rules")
        print("  stats - Show usage statistics")
        print("  exit - Exit the program")

        # Start keyboard listener
        listener = self.start_monitoring()
        
        while True:
            try:
                command = input("> ").strip().split(maxsplit=2)
                if not command:
                    continue
                
                if command[0] == "exit":
                    break
                elif command[0] == "list":
                    self.list_replacements()
                elif command[0] == "stats":
                    self.show_stats()
                elif command[0] == "add" and len(command) == 3:
                    self.add_replacement(command[1], command[2])
                elif command[0] == "remove" and len(command) == 2:
                    self.remove_replacement(command[1])
                else:
                    print("Invalid command!")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("Exiting...")
        listener.stop()

if __name__ == "__main__":
    replacer = TextReplacer()
    replacer.run()