import { useEffect, useState } from "react";
import { PieChart } from "@mui/x-charts/PieChart";
import APIClient from "../api/APIClient";

type TargetData = { id: number; value: number; label: string };

export default () => {
  const [target, setTarget] = useState<TargetData[] | undefined>();

  useEffect(() => {
    const f = async () => {
      const response = await APIClient.get("/portfolio/target_allocation");
      const formatted_data = Object.entries(response.data).map(
        ([label, value], id) => ({
          id,
          value: Math.round((value as number) * 100),
          label,
        })
      );
      setTarget(formatted_data);
    };
    f();
  }, []);

  return target && (
    <PieChart
      series={[
        {
          data: target,
          arcLabel: (item) => `${item.value}%`,
          arcLabelRadius: "70%",
        },
      ]}
      width={200}
      height={200}
    />
  );
};
