import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

interface Account {
  name: string;
  balance: number;
}

interface AccountsTableProps {
  accounts: Account[];
}

const formatUSD = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
}).format;

const AccountsTable: React.FC<AccountsTableProps> = ({ accounts }) => {
  return (
    <TableContainer component={Paper} sx={{ maxWidth: 400, marginTop: 5 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Balance</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {accounts.map((account, index) => (
            <TableRow key={index}>
              <TableCell>{account.name}</TableCell>
              <TableCell>{formatUSD(account.balance)}</TableCell>
            </TableRow>
          ))}
          <TableRow key="total">
            <TableCell>Total</TableCell>
            <TableCell>
              {formatUSD(
                accounts.reduce((total, obj) => total + (obj.balance || 0), 0)
              )}
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default AccountsTable;
