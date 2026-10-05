"""
ThreadsGPT CLI Interface
Beautiful command-line interface using Rich
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from pathlib import Path
import sys

console = Console()

BANNER = """
  _____ _                    _     ____ ____ _____ 
 |_   _| |__  _ __ ___  __ _| |__ / ___|  _ \\_   _|
   | | | '_ \\| '__/ _ \\/ _` | '_ \\| |  _| |_) || |  
   | | | | | | | |  __/ (_| | | | | |_| |  __/ | |  
   |_| |_| |_|_|  \\___|\\__,_|_| |_|\\____|_|    |_|  
                                                     
  The Ultimate AI-Powered Threads Growth Engine
"""

@click.group()
def cli():
    """ThreadsGPT - Grow your Threads account with AI"""
    console.print(BANNER, style="bold cyan")
    console.print("Version 1.0.0 | Made with [red]♥[/red] for the community\n")

@cli.command()
def setup():
    """Initial setup wizard"""
    console.print(Panel("🚀 Welcome to ThreadsGPT Setup", style="bold green"))
    
    # Check if config exists
    config_path = Path("config.yaml")
    if config_path.exists():
        console.print("[yellow]Warning: config.yaml already exists![/yellow]")
        if not click.confirm("Do you want to overwrite it?"):
            console.print("[red]Setup cancelled[/red]")
            return
    
    # Copy example config
    example_config = Path("config.example.yaml")
    if not example_config.exists():
        console.print("[red]Error: config.example.yaml not found![/red]")
        return
    
    import shutil
    shutil.copy(example_config, config_path)
    
    console.print("[green]✓[/green] Config file created: config.yaml")
    console.print("\n[yellow]Next steps:[/yellow]")
    console.print("1. Edit config.yaml with your settings")
    console.print("2. Run: python extract_cookies.py (to get session)")
    console.print("3. Run: python main.py analytics (to start)")

@cli.command()
@click.option('--days', default=7, help='Number of days to analyze')
def analytics(days):
    """View analytics dashboard"""
    from src.core.analytics import Analyzer
    
    console.print(Panel(f"📊 Analytics Report (Last {days} days)", style="bold blue"))
    
    try:
        analyzer = Analyzer()
        stats = analyzer.get_summary(days=days)
        
        # Create stats table
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Change", style="yellow")
        
        table.add_row("Followers", str(stats.get('followers', 'N/A')), stats.get('follower_change', 'N/A'))
        table.add_row("Avg Engagement", f"{stats.get('engagement_rate', 0):.2f}%", stats.get('engagement_change', 'N/A'))
        table.add_row("Total Posts", str(stats.get('total_posts', 0)), "")
        table.add_row("Best Time", stats.get('best_time', 'N/A'), "")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print("[yellow]Tip: Make sure you have run extract_cookies.py first[/yellow]")

@cli.command()
def schedule():
    """Manage scheduled posts"""
    from src.core.scheduler import Scheduler
    
    console.print(Panel("📅 Scheduled Posts", style="bold blue"))
    
    try:
        scheduler = Scheduler()
        posts = scheduler.get_queue()
        
        if not posts:
            console.print("[yellow]No posts scheduled[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Content", style="white")
        table.add_column("Scheduled Time", style="green")
        table.add_column("Status", style="yellow")
        
        for post in posts:
            content_preview = post['content'][:50] + "..." if len(post['content']) > 50 else post['content']
            table.add_row(
                str(post['id']),
                content_preview,
                post['scheduled_time'],
                post['status']
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
@click.argument('content')
@click.option('--time', default='auto', help='Post time (auto/HH:MM)')
@click.option('--media', help='Path to media file')
def post(content, time, media):
    """Schedule a new post"""
    from src.core.scheduler import Scheduler
    
    console.print(Panel("📝 Scheduling New Post", style="bold green"))
    
    try:
        scheduler = Scheduler()
        
        post_id = scheduler.schedule_post(
            content=content,
            post_time=time,
            media=[media] if media else None
        )
        
        console.print(f"[green]✓[/green] Post scheduled successfully!")
        console.print(f"Post ID: {post_id}")
        if time == 'auto':
            console.print("[yellow]Time: Auto-detected optimal time[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
def monitor():
    """Start monitoring viral content"""
    from src.ai.viral_detector import ViralDetector
    
    console.print(Panel("🔍 Viral Content Monitor", style="bold magenta"))
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")
    
    try:
        detector = ViralDetector()
        
        with console.status("[bold green]Scanning for viral content..."):
            viral_posts = detector.find_trending(limit=10)
        
        if not viral_posts:
            console.print("[yellow]No viral content found[/yellow]")
            return
        
        console.print(f"[green]Found {len(viral_posts)} viral posts![/green]\n")
        
        for i, post in enumerate(viral_posts, 1):
            console.print(f"[bold cyan]{i}. Engagement: {post['engagement']}[/bold cyan]")
            console.print(f"   {post['text'][:100]}...")
            console.print()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
def dashboard():
    """Launch web dashboard"""
    console.print(Panel("🌐 Launching Web Dashboard", style="bold blue"))
    
    try:
        from src.dashboard.app import run_dashboard
        
        console.print("[green]Starting server...[/green]")
        console.print("[cyan]Dashboard will open at: http://localhost:8080[/cyan]")
        console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")
        
        run_dashboard()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
def status():
    """Show system status"""
    console.print(Panel("⚙️ ThreadsGPT Status", style="bold green"))
    
    # Check files
    files_to_check = [
        ("config.yaml", "Configuration"),
        ("threads_session.json", "Session Data"),
        ("data/threadsgpt.db", "Database"),
    ]
    
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="white")
    
    for file_path, name in files_to_check:
        exists = Path(file_path).exists()
        status = "[green]✓ OK[/green]" if exists else "[red]✗ Missing[/red]"
        table.add_row(name, status)
    
    console.print(table)
    
    # Check dependencies
    console.print("\n[bold]Dependencies:[/bold]")
    try:
        import requests
        import pandas
        import yaml
        console.print("[green]✓[/green] All core dependencies installed")
    except ImportError as e:
        console.print(f"[red]✗[/red] Missing: {str(e)}")
        console.print("[yellow]Run: pip install -r requirements.txt[/yellow]")

def main():
    """Main entry point"""
    try:
        cli()
    except Exception as e:
        console.print(f"[red]Fatal Error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
