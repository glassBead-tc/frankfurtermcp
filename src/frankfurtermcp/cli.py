import asyncio
import sys
from pathlib import Path
from fastmcp import Client
from typer import Typer
from rich import print as print
from rich.console import Console
from rich.table import Table
from frankfurtermcp.common import (
    package_metadata,
)

app = Typer(
    name=f"{package_metadata['Name']}-cli",
    no_args_is_help=True,
    add_completion=False,
    help="A command-line test interface for the Frankfurter MCP server.",
)


def _print_header():
    print(
        f"[bold yellow]{package_metadata['Name']}-cli[/bold yellow] {package_metadata['Version']}: a command line interface to a{package_metadata['Summary'][1:]}"
    )


def _get_stdio_client():
    """
    Create a stdio client that connects to the server script.
    """
    # Find the server.py file relative to this CLI module
    server_path = Path(__file__).parent / "server.py"
    return Client(str(server_path))


@app.command()
def version():
    """
    Print the version of the Frankfurter MCP CLI.
    """
    _print_header()
    print(
        f"[bold blue]Author(s)[/bold blue]: [cyan]{package_metadata['Author-email']}[/cyan]"
    )
    print(
        f"[bold blue]License[/bold blue]: [cyan]{package_metadata['License-Expression']}[/cyan]"
    )
    print(
        f"[bold blue]Required Python[/bold blue]: [cyan]{package_metadata['Requires-Python']}[/cyan]"
    )


@app.command()
def test_connection():
    """
    Test the connection to the MCP server via stdio transport.
    """
    _print_header()
    print("[cyan]Testing connection to server via stdio transport...[/cyan]")
    
    async def test():
        try:
            client = _get_stdio_client()
            async with client:
                # Test ping
                print("[green]✓[/green] Connected to server")
                
                # Get server info
                tools = await client.list_tools()
                print(f"[green]✓[/green] Server has {len(tools)} tools available")
                
                # Test a simple tool
                if tools:
                    print(f"[green]✓[/green] Available tools: {', '.join(t.name for t in tools[:3])}{'...' if len(tools) > 3 else ''}")
                
                return True
        except Exception as e:
            print(f"[bold red]✗ Connection failed: {e}[/bold red]")
            return False
    
    success = asyncio.run(test())
    if success:
        print("\n[bold green]Server connection test passed![/bold green]")
    else:
        print("\n[bold red]Server connection test failed![/bold red]")


async def _retrieve_tools_metadata(client: Client):
    async with client:
        tools = await client.list_tools()
        return tools


@app.command()
def tools_info():
    """
    Print information about the available tools in the Frankfurter MCP server.
    """
    _print_header()
    print("[cyan]Connecting to server via stdio transport...[/cyan]")
    
    try:
        client = _get_stdio_client()
        tools_list = asyncio.run(_retrieve_tools_metadata(client))
        
        if not tools_list:
            print("[bold red]No tools found.[/bold red]")
        else:
            table = Table(
                caption="List of available tools using the FastMCP client (stdio)",
                caption_justify="right",
            )
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Description and schema", style="yellow")
            for tool in tools_list:
                table.add_row(tool.name, tool.description)
                table.add_row(None, None)
                table.add_row(None, tool.model_dump_json(indent=2))
                table.add_section()
            console = Console()
            console.print(table)
    except Exception as e:
        print(f"[bold red]Error connecting to server: {e}[/bold red]")
        print("[yellow]Make sure the server module is properly installed.[/yellow]")


@app.command()
def llamaindex_tools_list():
    """
    List tools from the MCP server using LlamaIndex's MCP client.
    """
    _print_header()
    print("[bold yellow]Note: LlamaIndex MCP client integration is not available for stdio transport.[/bold yellow]")
    print("[yellow]The server now runs in stdio mode only.[/yellow]")
    print("[yellow]Use the 'tools-info' command instead to list tools via stdio transport.[/yellow]")


def main():
    try:
        app()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
