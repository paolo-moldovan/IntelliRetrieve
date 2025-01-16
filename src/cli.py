from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.layout import Layout
from pathlib import Path
import requests
import sys
import time

console = Console()

class RAGChatCLI:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.console = Console()
        self.history = []
        
    def select_input(self):
        console.print("\n[bold blue]Welcome to RAG Chat![/bold blue]")
        choice = Prompt.ask(
            "\nWhat would you like to index?",
            choices=["folder", "file", "quit"],
            default="file"
        )
        
        if choice == "quit":
            sys.exit(0)
            
        path = Prompt.ask("\nPlease enter the path")
        path = Path(path).resolve()
        
        if not path.exists():
            console.print(f"[red]Error: Path {path} does not exist[/red]")
            return self.select_input()
            
        files = []
        if choice == "folder":
            files = list(path.glob("**/*.pdf"))
            if not files:
                console.print("[red]No PDF files found in folder[/red]")
                return self.select_input()
            console.print(f"\nFound {len(files)} PDF files:")
            for f in files:
                console.print(f"  - {f.relative_to(path)}")
        else:
            if path.suffix.lower() != '.pdf':
                console.print("[red]Error: Selected file is not a PDF[/red]")
                return self.select_input()
            files = [path]
            
        if Confirm.ask("\nProceed with indexing?"):
            return [str(f) for f in files]
        return self.select_input()

    def index_files(self, files):
        console.print("\n[bold blue]Indexing files...[/bold blue]")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                overall_task = progress.add_task(
                    "[blue]Indexing documents...", 
                    total=len(files)
                )
                
                file_task = progress.add_task("[cyan]Current file...", total=1.0)
                
                for file_path in files:
                    progress.update(
                        file_task, 
                        description=f"[cyan]Processing {Path(file_path).name}",
                        completed=0
                    )
                    
                    try:
                        response = requests.post(
                            f"{self.api_url}/index",
                            json={"file_paths": [file_path]}
                        )
                        response.raise_for_status()
                        
                        progress.update(file_task, completed=1.0)
                        progress.advance(overall_task)
                        
                    except Exception as e:
                        console.print(f"\n[red]Error indexing {file_path}: {str(e)}[/red]")
                        continue
                    
                    time.sleep(0.1)
                
            console.print("\n[green]Indexing complete![/green]")
            
        except Exception as e:
            console.print(f"\n[red]Error during indexing: {str(e)}[/red]")
            sys.exit(1)

    def display_chat_history(self):
        layout = Layout()
        
        history_text = ""
        for entry in self.history:
            role = entry["role"]
            content = entry["content"]
            
            if role == "user":
                history_text += f"\n[bold blue]You:[/bold blue]\n{content}\n"
            else:
                history_text += f"\n[bold green]Assistant:[/bold green]\n{content}\n"
                
        return Panel(
            history_text,
            title="Chat History",
            border_style="blue",
            padding=(1, 2)
        )

    def chat_loop(self):
        console.clear()
        console.print("[bold blue]Chat started! (type 'quit' to exit)[/bold blue]\n")
        
        while True:
            console.clear()
            console.print(self.display_chat_history())
            
            user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
            
            if user_input.lower() in ['quit', 'exit']:
                break
                
            self.history.append({"role": "user", "content": user_input})
            
            try:
                response = requests.post(
                    f"{self.api_url}/query",
                    json={"query": user_input}
                )
                response.raise_for_status()
                result = response.json()
                
                self.history.append({
                    "role": "assistant",
                    "content": result["response"]
                })
                
            except Exception as e:
                console.print(f"\n[red]Error: {str(e)}[/red]")
                continue

def main():
    cli = RAGChatCLI()
    files = cli.select_input()
    cli.index_files(files)
    cli.chat_loop()

if __name__ == "__main__":
    main() 