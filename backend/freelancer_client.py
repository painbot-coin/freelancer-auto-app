import os
from typing import Any, Dict, List, Optional

import httpx


class FreelancerClient:
    """
    Minimal Freelancer.com API wrapper.

    Supports multiple accounts by reading different environment variables
    for each account's token, e.g. FREELANCER_API_TOKEN_ACC1, ACC2, etc.
    """

    def __init__(
        self,
        base_url: str = "https://www.freelancer.com/api/projects/0.1",
        token_env_var: str = "FREELANCER_API_TOKEN",
    ):
        self.base_url = base_url.rstrip("/")
        self._token_env_var = token_env_var
        self._token = os.getenv(self._token_env_var)

    def _headers(self) -> Dict[str, str]:
        if not self._token:
            # No token yet – we'll use this to fall back to demo data in our FastAPI route
            return {}
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

    async def list_active_projects(
        self,
        keyword: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Call Freelancer API to fetch active projects.

        Endpoint and params are based on public docs; you can adjust
        filters later (jobs[], min_avg_price, hourly, fixed, etc.).
        """
        if not self._token:
            # Signal to caller that we can't hit real API yet
            raise RuntimeError(f"{self._token_env_var} not set")

        params: Dict[str, Any] = {
            "limit": limit,
        }
        if keyword:
            params["query"] = keyword

        url = f"{self.base_url}/projects/active/"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=self._headers(), params=params)
            resp.raise_for_status()
            data = resp.json()

        # The exact structure depends on the API; adjust mapping here.
        # We'll assume data["result"]["projects"] is a list.
        projects = data.get("result", {}).get("projects", [])
        return projects

    async def get_account_status(self) -> Dict[str, Any]:
        """
        Fetch basic info for the authenticated user.

        The exact endpoint may differ; adjust according to the official docs.
        This returns a dict so FastAPI can shape it into a response model.
        """
        if not self._token:
            raise RuntimeError(f"{self._token_env_var} not set")

        # Example users endpoint base; tweak path/fields once you confirm docs
        users_base = "https://www.freelancer.com/api/users/0.1"
        url = f"{users_base}/self/"

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=self._headers())
            resp.raise_for_status()
            data = resp.json()

        # You can inspect the raw response and fine-tune later
        return data



