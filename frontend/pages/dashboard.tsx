import ModuleCard from "../components/ModuleForm";

export default function Dashboard() {
  const exampleModules = [
    { moduleCode: "CS101", enrolled: 45 },
    { moduleCode: "MATH204", enrolled: 30 },
    { moduleCode: "PHY302", enrolled: 50 },
  ];

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <h1 className="text-3xl font-bold mb-6">Your Modules</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {exampleModules.map(({ moduleCode, enrolled }) => (
          <ModuleCard
            key={moduleCode}
            moduleCode={moduleCode}
            enrolled={enrolled}
          />
        ))}
      </div>
    </main>
  );
}
