import { useState, useEffect, useCallback } from "react";
import { usePlaidLink } from "react-plaid-link";

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [accounts, setAccounts] = useState([]);

  const onSuccess = useCallback(async (publicToken: string) => {
    await fetch("http://localhost:5000/api/exchange_public_token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ public_token: publicToken }),
    });
    getAccounts();
  }, []);

  // Creates a Link token
  const createLinkToken = useCallback(async () => {
    const response = await fetch(
      "http://localhost:5000/api/create_link_token",
      {
        method: "GET",
      }
    );
    const data = await response.json();
    setToken(data.link_token);
    localStorage.setItem("link_token", data.link_token);
  }, [setToken]);

  const getAccounts = useCallback(async () => {
    const response = await fetch("http://localhost:5000/api/accounts", {
      method: "GET",
    });
    const data = await response.json();
    setAccounts(data);
  }, [setAccounts]);

  let isOauth = false;

  const config = {
    token,
    onSuccess,
  };

  const { open, ready } = usePlaidLink(config);

  useEffect(() => {
    if (token == null) {
      createLinkToken();
    }
    if (isOauth && ready) {
      open();
    }
  }, [token, isOauth, ready, open]);

  return (
    <div>
      <button onClick={() => open()} disabled={!ready}>
        <strong>Link account</strong>
      </button>
      <button onClick={() => getAccounts()}>Get Accounts</button>
      {accounts.map((account) => {
        return (
          <div key={account["name"]}>
            <p>Name: {account["name"]}</p>
            <p>Balance: {account["balance"]}</p>
          </div>
        );
      })}
    </div>
  );
}

export default App;
