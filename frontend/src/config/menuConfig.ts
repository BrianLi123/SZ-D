import { IconType } from '@/components/Icons';

export interface MenuItem {
  label: string;
  key: string;
  icon?: IconType;
  children?: MenuItem[];
  hidden?: boolean;
  code?: string;
}

export const menus: MenuItem[] = [
  // {
  //   label: '仪表盘',
  //   key: 'dashboard',
  //   icon: 'DashboardOutlined'
  // },
  {
    label: '需求分析',
    key: '/demandAnalysis',
    icon: 'AppstoreOutlined'
  },
  {
    label: '上传文档',
    key: '/uploadDocument',
    icon: 'UserOutlined',
  }
];
