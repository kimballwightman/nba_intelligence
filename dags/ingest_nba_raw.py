"""
DAG: ingest_nba_raw
Schedule: daily at 6am ET (after overnight transaction activity settles)

Collects raw NBA data from multiple sources and loads normalized records
into BigQuery raw schema tables:
    raw.players
    raw.teams
    raw.contracts
    raw.transactions
    raw.draft_picks
    raw.exceptions

Source hierarchy (nba.com is the authority for IDs):
    Players/Teams  → nba_api (nba.com)  [primary IDs]
    Contracts      → nba_api            [where available]
    Transactions   → stats.nba.com JSON [most timely]
    Draft picks    → nba_api
    Exceptions     → nba_api / to be determined

Task flow:
    fetch_teams
    fetch_players
         ↓
    fetch_transactions
    fetch_contracts
    fetch_draft_picks
    fetch_exceptions
         ↓
    load_all_to_bigquery
"""

from datetime import datetime, timedelta
from airflow.decorators import dag, task


# ---------------------------------------------------------------------------
# Default args applied to every task in this DAG.
# retries=1 means Airflow will retry a failed task once before marking it
# as failed. retry_delay controls how long it waits between attempts.
# ---------------------------------------------------------------------------
DEFAULT_ARGS = {
    "owner": "nba_intelligence",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="ingest_nba_raw",
    description="Ingest raw NBA data from nba.com and basketball-reference into BigQuery",
    schedule="0 11 * * *",  # 6am ET = 11:00 UTC (adjust for daylight saving)
    start_date=datetime(2026, 1, 1),
    catchup=False,           # don't backfill missed runs when you first turn this on
    default_args=DEFAULT_ARGS,
    tags=["ingestion", "nba", "raw"],
)
def ingest_nba_raw():

    # -----------------------------------------------------------------------
    # TASK: fetch_teams
    #
    # Pull all 30 NBA teams from nba_api. This establishes the team_id values
    # used as foreign keys across every other raw table.
    #
    # HOW TO DEVELOP:
    #   from nba_api.stats.static import teams
    #   all_teams = teams.get_teams()
    #   # Returns a list of dicts: {id, full_name, abbreviation, nickname,
    #   #                           city, state, year_founded}
    #   # Map these to your raw.teams column schema.
    # -----------------------------------------------------------------------
    @task()
    def fetch_teams() -> list[dict]:
        # TODO: import nba_api and pull team list
        # from nba_api.stats.static import teams as nba_teams
        # raw = nba_teams.get_teams()
        # return [{ "team_id": t["id"], "abbreviation": t["abbreviation"], ... } for t in raw]
        raise NotImplementedError("fetch_teams not yet implemented")


    # -----------------------------------------------------------------------
    # TASK: fetch_players
    #
    # Pull the full active player roster from nba_api. nba.com player_id is
    # the canonical ID used to join players across all other tables.
    #
    # HOW TO DEVELOP:
    #   from nba_api.stats.static import players
    #   active = [p for p in players.get_players() if p["is_active"]]
    #   # Returns: {id, full_name, first_name, last_name, is_active}
    #   # For richer data (team, position, jersey): use CommonPlayerInfo endpoint
    #   from nba_api.stats.endpoints import commonplayerinfo
    #   info = commonplayerinfo.CommonPlayerInfo(player_id=p["id"])
    #   df = info.get_data_frames()[0]
    # -----------------------------------------------------------------------
    @task()
    def fetch_players(teams: list[dict]) -> list[dict]:
        # teams param creates an explicit dependency — players runs after teams
        # TODO: implement player fetch
        raise NotImplementedError("fetch_players not yet implemented")


    # -----------------------------------------------------------------------
    # TASK: fetch_transactions
    #
    # nba_api has no transactions endpoint, but nba.com exposes the raw JSON
    # behind their transactions page at this URL (found via network inspection):
    #   https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json
    #
    # This is the most timely source — the Giannis trade showed up here within
    # hours, whereas basketball-reference and nba_api lagged by 14+ hours.
    #
    # HOW TO DEVELOP:
    #   import requests
    #   headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.nba.com/"}
    #   # nba.com blocks requests without a browser-like User-Agent
    #   resp = requests.get(
    #       "https://stats.nba.com/js/data/playermovement/NBA_Player_Movement.json",
    #       headers=headers
    #   )
    #   data = resp.json()
    #   # Inspect data.keys() to understand the structure, then map to raw.transactions columns
    #   # Key fields to look for: player_id, player_name, from_team, to_team,
    #   #                         transaction_type, transaction_date
    # -----------------------------------------------------------------------
    @task()
    def fetch_transactions() -> list[dict]:
        # TODO: implement transactions fetch from NBA_Player_Movement.json
        raise NotImplementedError("fetch_transactions not yet implemented")


    # -----------------------------------------------------------------------
    # TASK: fetch_contracts
    #
    # nba_api has some contract/salary data via the TeamPlayerDashboard and
    # PlayerProfile endpoints, but coverage is inconsistent. Evaluate:
    #   from nba_api.stats.endpoints import playercontractinformation
    #   # This endpoint may require a player_id and season
    #
    # Basketball-reference has more complete historical contract data:
    #   from basketball_reference_scraper import contracts (if available)
    #   # OR scrape https://www.basketball-reference.com/contracts/
    #
    # HOW TO DEVELOP:
    #   Start with nba_api, check what fields come back, fill gaps with
    #   basketball-reference. Join on player_id from nba.com (you may need
    #   to fuzzy-match player names if bball-ref uses different IDs).
    # -----------------------------------------------------------------------
    @task()
    def fetch_contracts(players: list[dict]) -> list[dict]:
        # players param creates dependency — contracts runs after players are fetched
        # TODO: implement contract fetch
        raise NotImplementedError("fetch_contracts not yet implemented")


    # -----------------------------------------------------------------------
    # TASK: fetch_draft_picks
    #
    # nba_api has traded pick data and draft history:
    #   from nba_api.stats.endpoints import drafthistory
    #   draft = drafthistory.DraftHistory(season_year_nullable="2025")
    #   df = draft.get_data_frames()[0]
    #   # Columns include: person_id, player_name, team_id, round_number,
    #   #                   round_pick, overall_pick, organization
    #
    # For future/traded picks (not yet used picks), look at:
    #   from nba_api.stats.endpoints import teamdetails
    #   # tradedpicks dataframe within teamdetails response
    #
    # HOW TO DEVELOP:
    #   Decide whether raw.draft_picks captures historical picks,
    #   future traded picks, or both. Start with one, extend later.
    # -----------------------------------------------------------------------
    @task()
    def fetch_draft_picks(teams: list[dict]) -> list[dict]:
        # TODO: implement draft pick fetch
        raise NotImplementedError("fetch_draft_picks not yet implemented")


    # -----------------------------------------------------------------------
    # TASK: fetch_exceptions
    #
    # Salary cap exceptions (MLE, BAE, TPE, etc.) are not cleanly available
    # in nba_api. Options to evaluate:
    #   1. ESPN or RealGM pages — may require scraping
    #   2. Spotrac / HoopsHype — check ToS before scraping
    #   3. Manual seed data in dbt seeds/ for now, replaced with live source later
    #
    # HOW TO DEVELOP:
    #   Start by manually creating a dbt seed CSV (dbt/seeds/cap_exceptions.csv)
    #   with the current season's exceptions per team. Wire up a live source
    #   once you've identified one with acceptable ToS.
    # -----------------------------------------------------------------------
    @task()
    def fetch_exceptions(teams: list[dict]) -> list[dict]:
        # TODO: implement exceptions fetch or replace with dbt seed
        raise NotImplementedError("fetch_exceptions not yet implemented")


    # -----------------------------------------------------------------------
    # TASK: load_to_bigquery
    #
    # Takes all collected data and upserts into BigQuery raw schema tables.
    # "Upsert" = insert new rows, update existing rows where the primary key
    # already exists. This keeps the raw tables current without full reloads.
    #
    # HOW TO DEVELOP:
    #   from google.cloud import bigquery
    #   client = bigquery.Client(project="nba-intelligence")
    #
    #   # Option A — full replace (simpler to start with):
    #   job = client.load_table_from_json(rows, "nba-intelligence.raw.players",
    #       job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"))
    #
    #   # Option B — upsert via MERGE (better for production):
    #   # Write rows to a temp table, then run a MERGE statement to upsert
    #   # into the target table on the primary key (e.g. player_id).
    #
    # Use the BigQuery Airflow provider for cleaner integration:
    #   from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
    #
    # CREDENTIALS:
    #   The container has the google provider installed. You'll need to configure
    #   an Airflow Connection for BigQuery in the UI:
    #   Admin → Connections → Add → Google Cloud → paste your SA keyfile JSON.
    #   Then reference it in operators with gcp_conn_id="google_cloud_default".
    # -----------------------------------------------------------------------
    @task()
    def load_to_bigquery(
        teams: list[dict],
        players: list[dict],
        transactions: list[dict],
        contracts: list[dict],
        draft_picks: list[dict],
        exceptions: list[dict],
    ) -> None:
        # TODO: implement BigQuery load for each table
        # Each list maps to one raw.* table
        raise NotImplementedError("load_to_bigquery not yet implemented")


    # -----------------------------------------------------------------------
    # WIRE UP THE TASK GRAPH
    #
    # Airflow infers dependencies from how you pass task return values into
    # other tasks. teams and players run first (in sequence) because every
    # other table depends on their IDs. The remaining fetches run in parallel
    # after players completes. load_to_bigquery waits for all of them.
    # -----------------------------------------------------------------------
    teams_data = fetch_teams()
    players_data = fetch_players(teams=teams_data)

    # These three are independent of each other — Airflow runs them in parallel
    transactions_data = fetch_transactions()
    contracts_data = fetch_contracts(players=players_data)
    draft_picks_data = fetch_draft_picks(teams=teams_data)
    exceptions_data = fetch_exceptions(teams=teams_data)

    load_to_bigquery(
        teams=teams_data,
        players=players_data,
        transactions=transactions_data,
        contracts=contracts_data,
        draft_picks=draft_picks_data,
        exceptions=exceptions_data,
    )


# Airflow requires the DAG to be instantiated at module level to be detected
ingest_nba_raw()
