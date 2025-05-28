import { useState, useEffect, useCallback } from "react";
import { usePlaidLink } from "react-plaid-link";
import { Box, Button, ButtonGroup } from "@mui/material";
import AccountsTable from "./components/AccountsTable";
import APIClient from "./api/APIClient";

const LINK_TOKEN_KEY = "link_token";

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [accounts, setAccounts] = useState<Array<any> | null>(null);

  const onSuccess = useCallback(async (publicToken: string) => {
    await APIClient.post("/exchange_public_token", {
      body: JSON.stringify({ public_token: publicToken }),
    });
    getAccounts();
  }, []);

  const createLinkToken = useCallback(async () => {
    const maybeLinkToken = localStorage.getItem(LINK_TOKEN_KEY);
    if (maybeLinkToken) {
      const linkToken = JSON.parse(maybeLinkToken);
      const now = new Date().getTime().toString();
      if (linkToken.expiration > now) {
        setToken(linkToken.value);
        return;
      }
    }

    const response = await APIClient.get("/create_link_token");
    setToken(response.link_token);
    localStorage.setItem(
      LINK_TOKEN_KEY,
      JSON.stringify({
        value: response.link_token,
        expiration: response.expiration,
      })
    );
  }, [setToken]);

  const refreshLinkToken = async () => {
    localStorage.removeItem(LINK_TOKEN_KEY);
    await createLinkToken();
  };

  const getAccounts = useCallback(async () => {
    const response = await APIClient.get("/accounts");
    setAccounts(response);
  }, [setAccounts]);

  const { open, ready } = usePlaidLink({ token, onSuccess });

  useEffect(() => {
    createLinkToken();
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        paddingTop: "100px",
        width: "100%",
      }}
    >
      <ButtonGroup variant="contained">
        <Button onClick={() => open()} disabled={!ready}>
          Link account
        </Button>
        <Button onClick={refreshLinkToken}>Refresh Link</Button>
        <Button onClick={getAccounts}>Get Accounts</Button>
      </ButtonGroup>
      {accounts && <AccountsTable accounts={accounts} />}
    </Box>
  );
}

export default App;
