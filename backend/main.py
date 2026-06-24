from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from freelancer_client import FreelancerClient

app = FastAPI(title="Freelancer Auto App API")


class AccountInfo(BaseModel):
    id: str
    name: str


class Job(BaseModel):
    id: int
    title: str
    description: str
    budget: Optional[float] = None
    url: Optional[str] = None
    is_interesting: bool = False


class ProfileIdeaRequest(BaseModel):
    job_id: int
    idea: str
    account_id: Optional[str] = None


class ProfileIdeaResponse(BaseModel):
    optimized_headline: str
    optimized_overview: str
    notes: Optional[str] = None


class ChatMessage(BaseModel):
    sender: str  # "user" or "assistant"
    message: str


class AccountStatus(BaseModel):
    id: str
    name: str
    profile_name: str
    profile_status: str
    remaining_bids: int
    raw: Optional[dict] = None


# Simple static config for multiple Freelancer accounts.
# You only expose ids + display names to the frontend.
ACCOUNTS = [
    # Example - adjust names and env var suffixes to your real accounts:
    {"id": "acc1", "name": "Account 1", "token_env": "FREELANCER_API_TOKEN_ACC1"},
    {"id": "acc2", "name": "Account 2", "token_env": "FREELANCER_API_TOKEN_ACC2"},
]


def _find_account(account_id: Optional[str]):
    if not ACCOUNTS:
        return None
    if account_id:
        for acc in ACCOUNTS:
            if acc["id"] == account_id:
                return acc
    # default: first account
    return ACCOUNTS[0]


fake_jobs_db: List[Job] = [
    Job(
        id=1,
        title="Build a FastAPI backend",
        description="Need a backend API using FastAPI and PostgreSQL.",
        budget=300.0,
        url="https://example.com/job/1",
    ),
    Job(
        id=2,
        title="Vue.js SPA for dashboard",
        description="Create a dashboard using Vue 3 and Tailwind.",
        budget=500.0,
        url="https://example.com/job/2",
    ),
]

chat_history: List[ChatMessage] = []


@app.get("/accounts", response_model=List[AccountInfo])
def list_accounts():
    """
    Return the list of configured Freelancer accounts (id + name only).
    Frontend uses this to populate the account combo box.
    """
    return [AccountInfo(id=a["id"], name=a["name"]) for a in ACCOUNTS]


@app.get("/accounts/status", response_model=List[AccountStatus])
async def accounts_status():
    """
    Dashboard data: for each configured account, returns high-level status.
    This will call Freelancer's user endpoint per account when tokens are set.
    If a token is missing or the call fails, it falls back to placeholder data.
    """
    results: List[AccountStatus] = []

    for acc in ACCOUNTS:
        token_env = acc["token_env"]
        profile_name = acc["name"]
        profile_status = "unknown"
        remaining_bids = -1
        raw_data = None

        try:
            client = FreelancerClient(token_env_var=token_env)
            data = await client.get_account_status()
            raw_data = data

            # These keys are guesses; adjust once you inspect real API payloads.
            user = (data.get("result") or {}).get("user") or data.get("user") or {}
            profile_name = user.get("display_name") or user.get("username") or acc["name"]
            profile_status = "active" if user else "unknown"
            # Bid/credit info field names may differ; treat missing as -1.
            remaining_bids = (
                user.get("remaining_bids")
                or user.get("bids_remaining")
                or -1
            )
        except Exception:
            # Keep placeholder values
            pass

        results.append(
            AccountStatus(
                id=acc["id"],
                name=acc["name"],
                profile_name=profile_name,
                profile_status=profile_status,
                remaining_bids=int(remaining_bids) if isinstance(remaining_bids, (int, float)) else -1,
                raw=raw_data,
            )
        )

    return results


@app.get("/jobs", response_model=List[Job])
async def list_jobs(
    keyword: Optional[str] = None,
    limit: int = 10,
    account_id: Optional[str] = None,
):
    """
    Automatic check of freelance jobs using Freelancer.com API.

    - Chooses an account based on account_id (for multiple profiles).
    - If the chosen account's token env var isn't set, falls back to demo jobs.
    """
    account = _find_account(account_id)
    token_env_var = account["token_env"] if account else "FREELANCER_API_TOKEN"

    client = FreelancerClient(token_env_var=token_env_var)
    try:
        projects = await client.list_active_projects(keyword=keyword, limit=limit)
        # Map Freelancer projects into our Job schema
        jobs: List[Job] = []
        for proj in projects:
            jobs.append(
                Job(
                    id=proj.get("id"),
                    title=proj.get("title", "Untitled project"),
                    description=proj.get("description", ""),
                    budget=(
                        proj.get("budget", {}).get("maximum")
                        or proj.get("budget", {}).get("minimum")
                    ),
                    url=f"https://www.freelancer.com/projects/{proj.get('id')}",
                    is_interesting=False,
                )
            )
        if jobs:
            return jobs
    except Exception:
        # If API call fails for any reason, don't break the app; fall back.
        pass

    # Fallback: existing fake jobs
    return fake_jobs_db


@app.post("/profile/optimize", response_model=ProfileIdeaResponse)
def optimize_profile(request: ProfileIdeaRequest):
    """
    Given a job and your idea, return a suggested optimized profile text.
    Later, you can use account_id to read the real Freelancer profile for that
    account and generate a more precise update.
    """
    matching_job = next((j for j in fake_jobs_db if j.id == request.job_id), None)
    title_piece = matching_job.title if matching_job else "Top Freelancer"

    return ProfileIdeaResponse(
        optimized_headline=f"{title_piece} | {request.idea[:50]}",
        optimized_overview=(
            f"I help clients with {title_piece.lower()}.\n\n"
            f"My idea for this project: {request.idea}"
        ),
        notes=(
            "This is a demo optimization. Replace with real logic later. "
            "account_id can be used to target a specific Freelancer profile."
        ),
    )


@app.post("/chat", response_model=List[ChatMessage])
def post_chat_message(message: ChatMessage):
    """
    Simple chat endpoint: store message server-side and return full history.
    Frontend can show this as your 'chat in this interface'.
    """
    chat_history.append(message)
    return chat_history


@app.get("/chat", response_model=List[ChatMessage])
def get_chat_history():
    return chat_history


@app.get("/")
def root():
    return {"message": "Freelancer Auto App API is running"}


