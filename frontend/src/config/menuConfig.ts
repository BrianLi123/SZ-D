import { IconType } from '@/components/Icons';

export interface MenuItem {
  label: string;
  key: string;
  icon?: IconType;
  children?: MenuItem[];
}

export const menus: MenuItem[] = [
  // {
  //   label: '仪表盘',
  //   key: 'dashboard',
  //   icon: 'DashboardOutlined'
  // },
  {
    label: '需求分析',
    key: 'demandAnalysis',
    icon: 'ClusterOutlined',
  }
];
