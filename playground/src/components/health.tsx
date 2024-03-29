import useHealth from "@/hooks/health";

export default function Health() {
  // show red and green dots for module health
  const { data, error } = useHealth()
  if (error) return <div className="text-red-500 text-sm">Failed to load</div>;
  if (!data) return <div className="text-gray-500 text-sm">Loading...</div>;
  return (
    <div className="flex flex-col mt-4">
      <span className="text-lg font-bold">Health</span>
      <div className="flex flex-row items-center">
        <span
          className={
            data.status === "ok"
              ? "bg-green-500 rounded-full w-4 h-4"
              : "bg-red-500 rounded-full w-4 h-4"
          }
        ></span>
        <span className="ml-1">Assessment Module Manager</span>
      </div>
      <div className="flex flex-col">
        {Object.entries(data.modules).map(([name, { healthy }]) => (
          <div className="flex flex-row items-center" key={name}>
            <span
              className={
                healthy
                  ? "bg-green-500 rounded-full w-4 h-4"
                  : "bg-red-500 rounded-full w-4 h-4"
              }
            ></span>
            <span className="ml-1">{name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
