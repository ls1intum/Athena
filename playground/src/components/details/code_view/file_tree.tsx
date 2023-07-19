import { FileTree } from "@/helpers/fetch_and_unzip";

type FileTreeProps = {
  tree: FileTree[];
  selectedFile?: string;
  onSelectFile: (path: string) => void;
};

export default function FileTree({ tree, selectedFile, onSelectFile }: FileTreeProps) {
  return (
    <ul>
      {tree.map((file, index) => (
        <li key={index} className="ml-2">
          {file.dir ? (
            <>
              {file.dirname}/
              {file.children && <FileTree tree={file.children} selectedFile={selectedFile} onSelectFile={onSelectFile} />}
            </>
          ) : (
            <button
              className={`${
                selectedFile === file.path ? "text-primary-500" : "text-gray-500"
              } hover:text-primary-500`}
              onClick={() => onSelectFile(file.path)}
            >
              {file.filename}
            </button>
          )}
        </li>
      ))}
    </ul>
  );
}
