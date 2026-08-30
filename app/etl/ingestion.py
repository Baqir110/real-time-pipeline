import pandas as pd
import httpx
from typing import List, Dict, Any, Optional


async def load_source_data(
    source_type: str = "api", source_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    if source_type == "api":
        url = source_path or "https://jsonplaceholder.typicode.com/users"
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(url)
            res.raise_for_status()
            return res.json()
    elif source_type == "csv":
        df = pd.read_csv(source_path)
        return df.to_dict(orient="records")
    elif source_type == "parquet":
        df = pd.read_parquet(source_path)
        return df.to_dict(orient="records")
    else:
        raise ValueError(f"Unsupported source type: {source_type}")
