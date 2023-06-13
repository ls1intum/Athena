import React, { useState } from "react";
import BaseInfoHeader from "@/components/base_info_header";
import NormalMode from "@/components/normal_mode";
import {ModuleMeta} from "@/model/health_response";

export default function Home() {
    const [athenaUrl, setAthenaUrl] = useState<string>(() => {
        // Default value if location is not defined (for server-side rendering)
        let defaultUrl = "http://127.0.0.1:5000";
        if (typeof window !== 'undefined' && window.location.hostname !== "localhost") {
            // default url for non-local development is the origin of the current page
            defaultUrl = window.location.origin;
        }
        return defaultUrl;
    });
    const [athenaSecret, setAthenaSecret] = useState<string>("");
    const [module, setModule] = useState<ModuleMeta | undefined>(undefined);
    const [evaluationMode, setEvaluationMode] = useState<boolean>(false);

    return (
        <main className="flex min-h-screen flex-col p-24">
            <h1 className="text-6xl font-bold text-white mb-8">Playground</h1>
            <BaseInfoHeader
                athenaUrl={athenaUrl} onChangeAthenaUrl={setAthenaUrl}
                athenaSecret={athenaSecret} onChangeAthenaSecret={setAthenaSecret}
                module={module} onChangeModule={setModule}
                evaluationMode={evaluationMode} onChangeEvaluationMode={setEvaluationMode}
            />
            {module && (evaluationMode ? <div>Eval</div>
             :
            <NormalMode athenaUrl={athenaUrl} athenaSecret={athenaSecret} module={module}/>)}
        </main>
    );
}
