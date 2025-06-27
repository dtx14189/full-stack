import React, { useState, useEffect } from "react";

const API_BASE = "http://localhost:5000";

function App() {
  const [type, setType] = useState("");
  const [accounts, setAccounts] = useState([]);
  const [message, setMessage] = useState("");
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState("");

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await fetch(`${API_BASE}/accounts`);
      const data = await response.json();
      setAccounts(data.accounts);
    } catch (err) {
      setMessage(`Error: Failed to load accounts`);
    }
  };

  const handleAccountSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch(`${API_BASE}/accounts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ type: type }),
    });

    const data = await response.json();

    if (response.ok) {
      setMessage(`${data.message}`);
      setType("");
      fetchAccounts();
    } else {
      setMessage(`Error: ${data.error || "Failed to create account"}`);
    }
  };

  const handleAccountClick = async (acct) => {
    setSelectedAccount(acct);
    // setMessage("");

    try {
      const response = await fetch(`${API_BASE}/accounts/${acct.id}/transactions`);
      const data = await response.json();
      setTransactions(data.transactions || data); // adjust depending on backend
    } catch (err) {
      setMessage("Failed to load transactions");
      setTransactions([]);
    }
  };

  const handleTransactionSubmit = async (e) => {
    e.preventDefault();

    if (!amount || isNaN(amount)) {
      setMessage("Please enter a valid amount");
      return;
    }

    if (!date) {
      setMessage("Please enter a date");
      return;
    }

    const response = await fetch(
      `${API_BASE}/accounts/${selectedAccount.id}/transactions`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          amount: parseFloat(amount),
          date: date,
        }),
      }
    );

    const data = await response.json();

    if (response.ok) {
      setMessage("Transaction added");
      setAmount("");
      setDate("");
      fetchAccounts(); 
      handleAccountClick(selectedAccount); // Refresh
    } else {
      setMessage(`Error: ${data.error || "Failed to add transaction"}`);
    }
  };

  const applyInterest = async (acctId) => {
    const response = await fetch(`${API_BASE}/accounts/${acctId}/apply-interest-fees`, {
      method: "POST",
    });

    const data = await response.json();
    if (response.ok) {
      setMessage(data.message || "Interest/fees applied");
      fetchAccounts();  // Refresh balances
      handleAccountClick(selectedAccount);  // Refresh transactions
    } else {
      setMessage(`Error: ${data.error || "Failed to apply interest/fees"}`);
    }
  };

  return (
    <div>
      <h1>Simple Bank App</h1>
      
      {message && (
        <p style={{ color: message.toLowerCase().startsWith("error") ? "red" : "green" }}>
          {message}
        </p>
      )}

      <h2>Create Account</h2>
      <form onSubmit={handleAccountSubmit}>
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

      <h2>Accounts</h2>
      <ul>
        {accounts.map((acct) => (
          <li
            key={acct.id}
            onClick={() => handleAccountClick(acct)}
            style={{
              cursor: "pointer",
              fontFamily: "monospace",
              whiteSpace: "pre",
              fontSize: "18px",
              fontWeight: selectedAccount?.id === acct.id ? "bold" : "normal"
            }}
          >
            {`${(acct.type + "#" + acct.id.toString().padStart(9, "0")).padEnd(25)}balance: $${parseFloat(acct.balance).toFixed(2).padStart(8)}`}
          </li>
        ))}
      </ul>

      {selectedAccount && (
        <div>
          <h3>Transactions for Account ID {selectedAccount.id}</h3>
          <ul>
            {transactions.length === 0 ? (
              <li>No transactions</li>
            ) : (
              transactions.map((txn, idx) => (
                <li key={idx}>
                  {txn.date} — ${txn.amount}
                </li>
              ))
            )}
          </ul>

          <h4>Add Transaction</h4>
          <form onSubmit={handleTransactionSubmit}>
            <input
              type="number"
              step="0.01"
              placeholder="Amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
            />
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
            />
            <button type="submit">Add Transaction</button>
          </form>

          <button
            onClick={() => applyInterest(selectedAccount.id)}
            style={{ marginTop: "20px" }}
          >
            Apply Interest/Fees
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
