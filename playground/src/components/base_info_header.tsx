import Health from "@/components/health";
import ModuleSelect from "@/components/module_select";
import {ModuleMeta} from "@/model/health_response";

export default function BaseInfoHeader(
    {athenaUrl, onChangeAthenaUrl, athenaSecret, onChangeAthenaSecret, module, onChangeModule, evaluationMode, onChangeEvaluationMode}: {
        athenaUrl: string,
        onChangeAthenaUrl: (value: string) => void,
        athenaSecret: string,
        onChangeAthenaSecret: (value: string) => void,
        module: ModuleMeta | undefined,
        onChangeModule: (value: ModuleMeta) => void,
        evaluationMode: boolean,
        onChangeEvaluationMode: (value: boolean) => void,
    }
) {
    return (
        <div className="bg-white rounded-md p-4">
            <label className="flex flex-col">
                <span className="text-lg font-bold">Athena URL</span>
                <input className="border border-gray-300 rounded-md p-2" value={athenaUrl}
                       onChange={e => onChangeAthenaUrl(e.target.value)}/>
            </label>
            <Health url={athenaUrl}/>
            <label className="flex flex-col mt-4">
                <span className="text-lg font-bold">Secret</span>
                <p className="text-gray-500 mb-2">
                    This is the secret that you configured in Athena.
                    It&apos;s optional for local development, but required for production setups.
                </p>
                <input className="border border-gray-300 rounded-md p-2" value={athenaSecret}
                        placeholder="Optional, only required for production setups"
                        onChange={e => onChangeAthenaSecret(e.target.value)}/>
            </label>
            <br />
            <ModuleSelect url={athenaUrl} module={module} onChange={onChangeModule} />
            <div className="flex flex-row mt-4">
                <button className={`p-2 rounded-l-md ${evaluationMode ? "bg-gray-200 text-gray-500" : "bg-blue-500 text-white"}`} onClick={() => onChangeEvaluationMode(false)}>Normal mode</button>
                <button className={`p-2 rounded-r-md ${evaluationMode ?  "bg-blue-500 text-white" : "bg-gray-200 text-gray-500"}`} onClick={() => onChangeEvaluationMode(true)}>Evaluation mode</button>
            </div>
        </div>
    );
}