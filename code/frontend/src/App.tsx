import { useState } from "react";
import Leaderboard from "./Leaderboard";
import TeamGenerator from "./TeamGenerator";

type View = "leaderboard" | "teams";

function App() {
  const [view, setView] = useState<View>("leaderboard");

  return (
    <div className="app">
      <header>
        <h1>LOLERS</h1>
        <nav>
          <button
            className={view === "leaderboard" ? "tab active" : "tab"}
            onClick={() => setView("leaderboard")}
          >
            Leaderboard
          </button>
          <button
            className={view === "teams" ? "tab active" : "tab"}
            onClick={() => setView("teams")}
          >
            Team Generator
          </button>
        </nav>
      </header>
      <main>
        {view === "leaderboard" ? <Leaderboard /> : <TeamGenerator />}
      </main>
    </div>
  );
}

export default App;
