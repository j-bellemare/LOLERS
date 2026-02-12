import type { Player, TeamsResponse } from "./types";

const JSON_HEADERS = { "Content-Type": "application/json" };

export async function fetchPlayers(): Promise<Player[]> {
  const res = await fetch("/api/lolers/players/");
  if (!res.ok) throw new Error("Failed to fetch players");
  return res.json();
}

export async function refreshPlayerScore(puuid: string): Promise<number> {
  const res = await fetch("/api/riot_api_app/get_player_score", {
    method: "POST",
    headers: JSON_HEADERS,
    body: JSON.stringify({ puuid }),
  });
  if (!res.ok) throw new Error("Failed to refresh score");
  return res.json();
}

export async function generateTeams(
  players: [string, number][]
): Promise<TeamsResponse> {
  const res = await fetch("/api/riot_api_app/get_teams", {
    method: "POST",
    headers: JSON_HEADERS,
    body: JSON.stringify({ players: [players] }),
  });
  if (!res.ok) throw new Error("Failed to generate teams");
  return res.json();
}
