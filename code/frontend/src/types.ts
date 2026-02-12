export interface Player {
  puuid: string;
  name: string;
  tag: string;
  score: number;
}

export interface Team {
  players: string[];
  total_score: number;
}

export interface TeamsResponse {
  Crugs: Team;
  Raptors: Team;
}
