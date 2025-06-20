import signal
import sys
from fastmcp import FastMCP
from frankfurtermcp.server import app as frankfurtermcp
from dotenv import load_dotenv

app = FastMCP(
    name="test_composition",
    instructions="This is a MCP server to test dynamic composition of MCP.",
)

COMPOSITION_PREFIX = "composition_"


@app.tool(
    description="The quintessential hello world tool",
    tags=["hello", "world"],
    name="hello_world",
    annotations={
        "readOnlyHint": True,
    },
)
def hello_world(name: str = None) -> str:
    """
    A simple tool that returns a greeting message.

    Args:
        name (str): The name to greet.

    Returns:
        str: A greeting message.
    """
    suffix = "This is the MCP server to test dynamic composition."
    return f"Hello, {name}! {suffix}" if name else f"Hello World! {suffix}"


def main():
    """
    Main function to run the MCP server.
    """

    def sigint_handler(signal, frame):
        """
        Signal handler to shut down the server gracefully.
        """
        app.unmount(prefix=COMPOSITION_PREFIX)
        # This is absolutely necessary to exit the program
        sys.exit(0)

    load_dotenv()
    signal.signal(signal.SIGINT, sigint_handler)

    app.mount(prefix=COMPOSITION_PREFIX, server=frankfurtermcp, as_proxy=False)
    # Run with stdio transport only
    app.run()


if __name__ == "__main__":
    main()
