import type { Feedback } from "@/model/feedback";

import { FileTree } from "@/helpers/fetch_and_unzip";

import { useState } from "react";
import { FocusStyleManager } from "@blueprintjs/core";
import { renderers as bpRenderers } from "react-complex-tree-blueprintjs-renderers";
import {
  ControlledTreeEnvironment,
  Tree,
  TreeItem,
  TreeItemIndex,
} from "react-complex-tree";

type FileTreeProps = {
  tree: FileTree[];
  feedbacks?: Feedback[];
  selectedFile?: string;
  onSelectFile: (path: string) => void;
};

type ItemData = {
  path: string;
  name: string;
  feedbackCount?: number;
};

export default function FileTree({
  tree,
  feedbacks,
  selectedFile,
  onSelectFile,
}: FileTreeProps) {
  let items: { [index: string]: TreeItem<ItemData> } = {
    root: {
      index: "root",
      isFolder: true,
      children: tree.map((file) => file.path),
      data: {
        path: "/",
        name: "Root Item",
      },
    },
  };

  const addChildren = (item: FileTree) => {
    if (item.dir) {
      items[item.path] = {
        index: item.path,
        isFolder: true,
        children: item.children?.map((file) => file.path) ?? [],
        data: {
          path: item.path,
          name: item.dirname,
        },
      };
      item.children?.forEach(addChildren);
    } else {
      const feedbackCount =
        feedbacks?.filter(
          (feedback) =>
            "file_path" in feedback && feedback.file_path === item.path
        ).length ?? 0;
      items[item.path] = {
        index: item.path,
        children: [],
        data: {
          path: item.path,
          name: item.filename,
          feedbackCount: feedbackCount > 0 ? feedbackCount : undefined,
        },
      };
    }
  };
  tree.forEach(addChildren);

  const [focusedItem, setFocusedItem] = useState<TreeItemIndex>();
  const [expandedItems, setExpandedItems] = useState<TreeItemIndex[]>([]);
  const [selectedItems, setSelectedItems] = useState<TreeItemIndex[]>([]);

  return (
    <div
      className="h-full overflow-auto"
      onMouseDown={() => FocusStyleManager.onlyShowFocusOnTabs()}
      onKeyDown={() => FocusStyleManager.alwaysShowFocus()}
    >
      <ControlledTreeEnvironment<ItemData>
        {...bpRenderers}
        items={items}
        getItemTitle={(item) => item.data.name}
        viewState={{
          ["tree-1"]: {
            focusedItem,
            expandedItems,
            selectedItems,
          },
        }}
        onFocusItem={(item) => setFocusedItem(item.index)}
        onExpandItem={(item) =>
          setExpandedItems([...expandedItems, item.index])
        }
        onCollapseItem={(item) =>
          setExpandedItems(
            expandedItems.filter(
              (expandedItemIndex) => expandedItemIndex !== item.index
            )
          )
        }
        onSelectItems={(items) => setSelectedItems(items)}
        onPrimaryAction={(item) => onSelectFile(`${item.index}`)}
        renderItemTitle={(props) => (
          <>
            {bpRenderers.renderItemTitle && bpRenderers.renderItemTitle(props)}
            {props.item.data.feedbackCount && (
              <span className="ml-1 text-slate-800 rounded bg-slate-200 px-1 py-0.5">
                {props.item.data.feedbackCount}
              </span>
            )}
          </>
        )}
      >
        <Tree treeId={"tree-1"} rootItem="root" treeLabel="File Tree" />
      </ControlledTreeEnvironment>
    </div>
  );
}