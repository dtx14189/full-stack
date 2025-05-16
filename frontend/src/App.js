import React, { useState, useEffect } from "react";

function App() {
  const [type, setType] = useState("");
  const [accounts, setAccounts] = useState([]);
  const [message, setMessage] = useState("");

  // Load accounts on initial render
  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await fetch("http://localhost:5000/accounts");
      const data = await response.json();
      setAccounts(data.accounts);
    } catch (err) {
      setMessage("Failed to load accounts");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://localhost:5000/accounts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: type,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      setMessage(`${data.message}`);
      setType("");
      fetchAccounts(); // refresh account list
    } else {
      setMessage(`Error: ${data.error || "Failed to create account"}`);
    }
  };

  return (
    <div>
      <h1>Simple Bank App</h1>

      <h2>Create Account</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Account Type:
          <select value={type} onChange={(e) => setType(e.target.value)} required>
            <option value="" disabled>
              -- Select Account Type --
            </option>
            <option value="checking">Checking</option>
            <option value="savings">Savings</option>
          </select>
        </label>
        <button type="submit">Create Account</button>
      </form>

      {message && <p>{message}</p>}

      <h2>Accounts</h2>
      <ul>
        {accounts.map((acct) => (
          <li key={acct.id}>
            ID: {acct.id} — {acct.type} — ${acct.balance}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
