import { useEffect, useState } from "react";
import { fetchPlayers, generateTeams } from "./api";
import type { Player, TeamsResponse } from "./types";

export default function TeamGenerator() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [teams, setTeams] = useState<TeamsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPlayers()
      .then((data) => {
        data.sort((a, b) => b.score - a.score);
        setPlayers(data);
      })
      .catch(() => setError("Failed to load players."))
      .finally(() => setLoading(false));
  }, []);

  function togglePlayer(puuid: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(puuid)) next.delete(puuid);
      else next.add(puuid);
      return next;
    });
  }

  function selectAll() {
    setSelected(new Set(players.map((p) => p.puuid)));
  }

  function selectNone() {
    setSelected(new Set());
  }

  async function handleGenerate() {
    setGenerating(true);
    setError(null);
    setTeams(null);
    try {
      const selectedPlayers: [string, number][] = players
        .filter((p) => selected.has(p.puuid))
        .map((p) => [p.name, p.score]);
      const result = await generateTeams(selectedPlayers);
      setTeams(result);
    } catch {
      setError("Failed to generate teams.");
    } finally {
      setGenerating(false);
    }
  }

  if (loading) return <p className="loading">Loading players…</p>;

  return (
    <div className="team-generator">
      <h2>Team Generator</h2>

      {error && <p className="error">{error}</p>}

      <div className="selection-actions">
        <button onClick={selectAll} className="btn-small">
          Select All
        </button>
        <button onClick={selectNone} className="btn-small">
          Clear
        </button>
        <span className="selection-count">
          {selected.size} of {players.length} selected
        </span>
      </div>

      <div className="player-checkboxes">
        {players.map((p) => (
          <label key={p.puuid} className="player-checkbox">
            <input
              type="checkbox"
              checked={selected.has(p.puuid)}
              onChange={() => togglePlayer(p.puuid)}
            />
            <span className="player-name">{p.name}</span>
            <span className="player-score">({p.score.toFixed(1)})</span>
          </label>
        ))}
      </div>

      <button
        onClick={handleGenerate}
        disabled={generating || selected.size < 2}
        className="btn-primary generate-btn"
      >
        {generating ? "Generating…" : "Generate Teams"}
      </button>

      {teams && (
        <div className="teams-result">
          <div className="team-card">
            <h3>Crugs</h3>
            <ul>
              {teams.Crugs.players.map((name) => (
                <li key={name}>{name}</li>
              ))}
            </ul>
            <p className="team-total">
              Total: {teams.Crugs.total_score.toFixed(1)}
            </p>
          </div>
          <div className="team-card">
            <h3>Raptors</h3>
            <ul>
              {teams.Raptors.players.map((name) => (
                <li key={name}>{name}</li>
              ))}
            </ul>
            <p className="team-total">
              Total: {teams.Raptors.total_score.toFixed(1)}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
