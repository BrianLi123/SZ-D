import config from '@/config';
/* 路由重置逻辑优化  
1.在createBrowserRouter之前，执行redirectRouterBasename
2.在createBrowserRouter中，设置 basename:config.app.routerBaseName
说明：basename 应用程序的基名，用于无法部署到域根目录而只能部署到子目录的情况。
*/
function resetRouterBasename() {
  const { pathname, origin, search } = window.location;
  if (!pathname.startsWith(config.app.routerBaseName)) {
    const href = `${origin}${config.app.routerBaseName}${pathname}${
      search ?? ''
    }`;

    window.location.assign(href);
  }
}

export const arrayMove = (arr: any, oldIndex: number, newIndex: number) => {
  const result = [...arr];
  const [removed] = result.splice(oldIndex, 1);
  result.splice(newIndex, 0, removed);
  return result;
};

/**
 * 递归 根据所有层数据和当前层层次和名称，找到上一层的数据
 * @param tree 所有层数据
 * @param curLevel 当前层和当前层名称
 * @return parent 上一层的数据
 */
export function findParent(tree: any, { level, object }: any) {
  let parent = null;

  function search(node: any, depth: any) {
    if (depth >= level || !node.list) return;

    for (const child of node.list) {
      if (child.object === object && depth + 1 === level) {
        parent = node;
        return;
      }
      // Recursively search in the deeper levels.
      search(child, depth + 1);
    }
  }
  // tree从深度为0时开始搜索(根节点为第0层)，如果当前层深度为1时说明父为根，直接返回tree
  for (const root of tree.list) {
    if (root.object === object && level === 1) {
      parent = tree;
      return parent;
    }
    search(root, 1);
  }

  return parent;
}
