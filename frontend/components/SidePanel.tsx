import { Project } from "@/app/page";
import { Activity, MapPin, DollarSign, Brain, MessageCircle } from "lucide-react";

interface SidePanelProps {
  project: Project | null;
}

export default function SidePanel({ project }: SidePanelProps) {
  if (!project) {
    return (
      <div className="flex items-center justify-center h-full w-full bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-400">
        <p>Select a project on the map</p>
      </div>
    );
  }

  return (
    <div className="h-full w-full bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-800 p-6 flex flex-col gap-6 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{project.name}</h2>
        <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
          <MapPin size={16} />
          <span>{project.location.join(", ")}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400 mb-2 text-sm">
            <Activity size={16} /> Status
          </div>
          <div className="font-semibold text-gray-900 dark:text-white">{project.status}</div>
        </div>
        
        <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400 mb-2 text-sm">
            <DollarSign size={16} /> Budget
          </div>
          <div className="font-semibold text-gray-900 dark:text-white">{project.budget}</div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800">
        <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400 mb-2 font-medium">
          <Brain size={18} /> AI Analysis Score
        </div>
        <div className="text-3xl font-bold text-blue-700 dark:text-blue-300">
          {project.ai_score}%
        </div>
        <div className="w-full bg-blue-200 dark:bg-blue-900 rounded-full h-2 mt-3">
          <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${project.ai_score}%` }}></div>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-800">
        <div className="flex items-center gap-2 text-green-600 dark:text-green-400 mb-2 font-medium">
          <MessageCircle size={18} /> Community Report (WhatsApp)
        </div>
        <p className="text-sm text-green-800 dark:text-green-200 italic">
          "{project.whatsapp_status}"
        </p>
      </div>
    </div>
  );
}
