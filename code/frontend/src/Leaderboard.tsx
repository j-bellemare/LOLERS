import { useEffect, useState } from "react";
import { fetchPlayers, refreshPlayerScore } from "./api";
import type { Player } from "./types";

export default function Leaderboard() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshingAll, setRefreshingAll] = useState(false);
  const [refreshingPuuid, setRefreshingPuuid] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function loadPlayers() {
    try {
      setError(null);
      const data = await fetchPlayers();
      data.sort((a, b) => b.score - a.score);
      setPlayers(data);
    } catch {
      setError("Failed to load players.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPlayers();
  }, []);

  async function handleRefresh(puuid: string) {
    setRefreshingPuuid(puuid);
    try {
      await refreshPlayerScore(puuid);
      await loadPlayers();
    } catch {
      setError("Failed to refresh score.");
    } finally {
      setRefreshingPuuid(null);
    }
  }

  async function handleRefreshAll() {
    setRefreshingAll(true);
    setError(null);
    try {
      for (const player of players) {
        setRefreshingPuuid(player.puuid);
        await refreshPlayerScore(player.puuid);
      }
      await loadPlayers();
    } catch {
      setError("Failed to refresh all scores.");
    } finally {
      setRefreshingAll(false);
      setRefreshingPuuid(null);
    }
  }

  if (loading) return <p className="loading">Loading players…</p>;

  return (
    <div className="leaderboard">
      <div className="page-header">
        <h2>Leaderboard</h2>
        <button
          onClick={handleRefreshAll}
          disabled={refreshingAll}
          className="btn-primary"
        >
          {refreshingAll ? "Refreshing…" : "Refresh All"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Tag</th>
            <th>Score</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {players.map((p, i) => (
            <tr key={p.puuid}>
              <td>{i + 1}</td>
              <td>{p.name}</td>
              <td>{p.tag}</td>
              <td>{p.score.toFixed(1)}</td>
              <td>
                <button
                  onClick={() => handleRefresh(p.puuid)}
                  disabled={refreshingPuuid === p.puuid || refreshingAll}
                  className="btn-small"
                >
                  {refreshingPuuid === p.puuid ? "…" : "Refresh"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {players.length === 0 && <p className="empty">No players found.</p>}
    </div>
  );
}
