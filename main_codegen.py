import argparse
import os
import sys
import asyncio
from pathlib import Path
from mmengine import DictAction

root = str(Path(__file__).resolve().parents[0])
sys.path.append(root)

from src.logger import logger
from src.config import config
from src.models import model_manager
from src.agent import create_agent


def parse_args():
    parser = argparse.ArgumentParser(description="codegen example")
    parser.add_argument(
        "--config",
        default=os.path.join(root, "configs", "config_codegen.py"),
        help="config file path",
    )

    parser.add_argument(
        "--cfg-options",
        nargs="+",
        action=DictAction,
        help="override some settings in the used config, the key-value pair "
        "in xxx=yyy format will be merged into config file. If the value to "
        "be overwritten is a list, it should be like key=\"[a,b]\" or key=a,b "
        "It also allows nested list/tuple values, e.g. key=\"[(a,b),(c,d)]\" "
        "Note that the quotation marks are necessary and that no white space "
        "is allowed.",
    )
    args = parser.parse_args()
    return args


async def main():
    # Parse command line arguments
    args = parse_args()

    # Initialize the configuration
    config.init_config(args.config, args)

    # Initialize the logger
    logger.init_logger(log_path=config.log_path)
    logger.info(f"| Logger initialized at: {config.log_path}")
    logger.info(f"| Config:\n{config.pretty_text}")

    # Registed models
    model_manager.init_models(use_local_proxy=config.use_local_proxy)
    logger.info("| Registed models: %s", ", ".join(model_manager.registed_models.keys()))

    # Create agent
    agent = await create_agent(config)
    logger.visualize_agent_tree(agent)

    # Run example: simple code generation, execution, and write to file
    out_dir = os.path.join(config.exp_path, "generated")
    out_file = os.path.join(out_dir, "fibonacci.py")
    task = (
        "Write a simple Python function fibonacci(n) that returns the nth Fibonacci number. "
        "Then, using the python_interpreter tool, define the function and run it for n=10, printing the result. "
        f"After that, use the file_writer_tool to write a standalone Python module containing the function (with a small __main__ demo) to this exact path: {out_file}. "
        "Finally, return both the exact code you wrote to the file and the numeric result as the final answer."
    )
    res = await agent.run(task)
    logger.info(f"| Result: {res}")


if __name__ == "__main__":
    asyncio.run(main())


