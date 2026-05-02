# cli_todo.py - No external dependencies
import os
import sys
import json

TODO_FILE = 'todo.json'

class TodoApp:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(TODO_FILE):
            try:
                with open(TODO_FILE, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', {})
                    self.next_id = data.get('next_id', 1)
            except:
                self.tasks = {}
                self.next_id = 1
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(TODO_FILE, 'w') as f:
            json.dump({
                'tasks': self.tasks,
                'next_id': self.next_id
            }, f, indent=2)
    
    def add_task(self, description):
        """Add a new task"""
        task_id = self.next_id
        self.tasks[task_id] = {
            'id': task_id,
            'description': description,
            'status': 'pending'
        }
        self.next_id += 1
        self.save_tasks()
        print(f"✓ Added task #{task_id}: {description}")
    
    def list_tasks(self, filter_status=None):
        """List all tasks"""
        if not self.tasks:
            print("\n📝 No tasks yet! Use 'add' to create one.\n")
            return
        
        print("\n" + "="*60)
        print("YOUR TASKS")
        print("="*60)
        
        for task_id, task in self.tasks.items():
            if filter_status and task['status'] != filter_status:
                continue
            
            status_icon = "✓" if task['status'] == 'completed' else "○"
            print(f"{status_icon} [{task_id}] {task['description']}")
        
        print("="*60 + "\n")
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = 'completed'
            self.save_tasks()
            print(f"✓ Completed task #{task_id}: {self.tasks[task_id]['description']}")
        else:
            print(f"✗ Error: Task #{task_id} not found")
    
    def delete_task(self, task_id):
        """Delete a task"""
        if task_id in self.tasks:
            description = self.tasks[task_id]['description']
            del self.tasks[task_id]
            self.save_tasks()
            print(f"✓ Deleted task #{task_id}: {description}")
        else:
            print(f"✗ Error: Task #{task_id} not found")
    
    def show_help(self):
        """Show help menu"""
        print("\n" + "="*60)
        print("CLI TODO APP - COMMANDS")
        print("="*60)
        print("  add <task>        - Add a new task")
        print("  list              - List all tasks")
        print("  pending           - List only pending tasks")
        print("  completed         - List only completed tasks")
        print("  done <id>         - Mark task as completed")
        print("  delete <id>       - Delete a task")
        print("  clear             - Delete all tasks")
        print("  help              - Show this help menu")
        print("  exit / quit       - Exit the app")
        print("="*60 + "\n")

def main():
    app = TodoApp()
    
    print("CLI TODO APPLICATION")
    app.show_help()
    
    while True:
        try:
            command = input("todo> ").strip().lower()
            
            if not command:
                continue
            
            # Parse command and arguments
            parts = command.split(maxsplit=1)
            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else None
            
            if cmd in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            elif cmd == 'add':
                if arg:
                    app.add_task(arg)
                else:
                    print("✗ Usage: add <task description>")
            
            elif cmd == 'list':
                app.list_tasks()
            
            elif cmd == 'pending':
                app.list_tasks('pending')
            
            elif cmd == 'completed':
                app.list_tasks('completed')
            
            elif cmd == 'done':
                if arg and arg.isdigit():
                    app.complete_task(int(arg))
                else:
                    print("✗ Usage: done <task_id>")
            
            elif cmd == 'delete':
                if arg and arg.isdigit():
                    confirm = input(f"⚠️  Delete task #{arg}? (y/n): ").lower()
                    if confirm == 'y':
                        app.delete_task(int(arg))
                else:
                    print("✗ Usage: delete <task_id>")
            
            elif cmd == 'clear':
                confirm = input("⚠️  Delete ALL tasks? (y/n): ").lower()
                if confirm == 'y':
                    app.tasks = {}
                    app.next_id = 1
                    app.save_tasks()
                    print("✓ All tasks deleted")
            
            elif cmd == 'help':
                app.show_help()
            
            else:
                print(f"✗ Unknown command: '{cmd}'. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()