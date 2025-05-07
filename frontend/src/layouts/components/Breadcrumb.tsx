import { Breadcrumb } from 'antd';
import { useLocation, matchRoutes } from 'react-router-dom';
import { selectBreadcrumb, setBreadcrumb } from '@/store/reducer/layoutSlice';
import { routes } from '@/router';
import Icon, { IconType } from '@/components/Icons';
import { menus, MenuItem } from '@/config/menuConfig';
import { flatArrTree } from '@/utils/utils';
import { mapRouteToMenuStatus } from '../useMenu';

type BreadcrumbItem = {
  name: string;
  path?: string;
  icon?: IconType;
};

export type BreadcrumbType = Array<BreadcrumbItem>;

/**
 * Layout Breadcrumb
 * @param {BreadcrumbType} data
 * @returns
 */
export default function LayoutBreadcrumb() {
  useBreadcrumbFromMenu();
  const breadcrumb = useAppSelector(selectBreadcrumb);
  if (breadcrumb.length === 0) {
    return null;
  }
  const items = breadcrumb.map((item) => ({
    title: (
      <>
        {item.icon && <Icon type={item.icon} style={{ marginRight: 8 }} />}
        <span>{item.name}</span>
      </>
    )
  }));

  return <Breadcrumb separator="/" items={items} />;
}

/**
 * Dynamically generate breadcrumb configuration data
 */
function useBreadcrumbFromMenu() {
  const location = useLocation();
  const dispatch = useAppDispatch();
  const lang = useAppSelector(selectLanguage);

  const generateMenuBreadcrumb = ({
    openKeys = [],
    selectKey
  }: {
    openKeys: string[];
    selectKey: string;
  }) => {
    const menuItems: MenuItem[] = flatArrTree(menus, 'children');
    const menuOpenKeysInfo = openKeys
      .map((key: string) => menuItems.find((item) => item.key === key))
      .reverse();
    const menuSelectKeyInfo = menuItems.find((item) => item.key === selectKey);
    const breadcrumb = [...menuOpenKeysInfo, menuSelectKeyInfo].map((item) => ({
      name: item?.label as string,
      path: item?.key,
      icon: item?.icon
    })) as BreadcrumbType;
    return breadcrumb;
  };

  useEffect(() => {
    const currentRouteMatch = matchRoutes(routes, location);
    if (!currentRouteMatch) {
      return;
    }
    const currentRouteConfig = currentRouteMatch?.at(-1)?.route;
    if (!currentRouteConfig) {
      return;
    }
    let menuState = mapRouteToMenuStatus(menus, location.pathname);
    if (menuState) {
      let menuBreadCrumb = generateMenuBreadcrumb(menuState);
      if (currentRouteConfig.menuKey) {
        menuBreadCrumb?.push({ name: currentRouteConfig.title! });
      }
      dispatch(setBreadcrumb(menuBreadCrumb));
      return;
    }
    dispatch(setBreadcrumb([{ name: currentRouteConfig.title! }]));
  }, [location, lang]);
}
