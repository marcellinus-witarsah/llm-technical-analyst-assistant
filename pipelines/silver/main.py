import argparse
import importlib
from types import ModuleType
from datetime import datetime

def get_pipeline_module(pipeline_name: str) -> ModuleType:
    """Get a pipeline by name inside the silver folder.

    Args:
        pipeline_name (str): pipeline name.

    Returns:
        ModuleType: imported module.
    """
    try:
        data_pipeline = importlib.import_module(f"pipelines.silver.{pipeline_name}")
    except ImportError:
        print(f"Error: Could not import module '{pipeline_name}'")
    return data_pipeline


if __name__ == "__main__":
    # =========================================================================
    # Create parser for processing CLI arguments
    # =========================================================================
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pipeline-name", type=str, required=True, help="Name of the pipeline"
    )

    parser.add_argument(
        "--source", type=str, required=True, help="Source table from Bronze Layer"
    )

    parser.add_argument(
        "--target", type=str, required=True, help="Target table in Silver Layer"
    )

    parser.add_argument(
        "--start-date",
        type=str,
        required=True,
        help="The start date to process the data in YYYY-MM-DD format",
    )

    parser.add_argument(
        "--end-date",
        type=str,
        required=True,
        help="The end date to process the data in YYYY-MM-DD format",
    )

    args = parser.parse_args()
    source = args.source
    target = args.target
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    # =========================================================================
    # Ingest data from `Bronze` to `Silver`
    # =========================================================================
    pipeline_module = get_pipeline_module(args.pipeline_name)
    pipeline = pipeline_module.DataPipeline(
        source=source, target=target, start_date=start_date, end_date=end_date
    )
    pipeline.run()
