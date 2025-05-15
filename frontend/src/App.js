import React, { useState } from "react";

function App() {
  const [name, setName] = useState("");
  const [balance, setBalance] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload

    const response = await fetch("http://localhost:5000/accounts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        initial_balance: parseFloat(balance),
      }),
    });

    const data = await response.json();

    if (response.ok) {
      setMessage(`Account created for ${data.name} with $${data.balance}`);
    } else {
      setMessage(`Error: ${data.error || "Could not create account"}`);
    }

    // Optional: clear form
    setName("");
    setBalance("");
  };

  return (
    <div>
      <h1>Create Account</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Account name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="number"
          placeholder="Initial balance"
          value={balance}
          onChange={(e) => setBalance(e.target.value)}
        />
        <button type="submit">Create</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
