import { useEffect, useState } from "react";

function App() {
  const [bets, setBets] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/bets")
      .then(res => res.json())
      .then(data => setBets(data));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Betting Dashboard</h1>
      <table border="1" cellPadding="5">
        <thead>
          <tr>
            <th>ID</th>
            <th>Time</th>
            <th>Market</th>
            <th>Odds</th>
            <th>Probability</th>
            <th>Edge</th>
            <th>Stake</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {bets.map(bet => (
            <tr key={bet[0]}>
              {bet.map((val, idx) => <td key={idx}>{val}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
