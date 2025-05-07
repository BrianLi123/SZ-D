import type { CSSProperties } from 'react';
import SettingOutlined from '@ant-design/icons/SettingOutlined';
import UnorderedListOutlined from '@ant-design/icons/UnorderedListOutlined';
import UserOutlined from '@ant-design/icons/UserOutlined';
import UserAddOutlined from '@ant-design/icons/UserAddOutlined';
import UsergroupDeleteOutlined from '@ant-design/icons/UsergroupDeleteOutlined';
import BlockOutlined from '@ant-design/icons/BlockOutlined';
import LockOutlined from '@ant-design/icons/LockOutlined';
import DashboardOutlined from '@ant-design/icons/DashboardOutlined';
import FormOutlined from '@ant-design/icons/FormOutlined';
import TableOutlined from '@ant-design/icons/TableOutlined';
import ProfileOutlined from '@ant-design/icons/ProfileOutlined';
import InfoCircleOutlined from '@ant-design/icons/InfoCircleOutlined';
import CheckCircleOutlined from '@ant-design/icons/CheckCircleOutlined';
import FullscreenOutlined from '@ant-design/icons/FullscreenOutlined';
import FullscreenExitOutlined from '@ant-design/icons/FullscreenExitOutlined';
import MenuUnfoldOutlined from '@ant-design/icons/MenuUnfoldOutlined';
import MenuFoldOutlined from '@ant-design/icons/MenuFoldOutlined';
import LoadingOutlined from '@ant-design/icons/LoadingOutlined';
import IdcardOutlined from '@ant-design/icons/IdcardOutlined';
import PoweroffOutlined from '@ant-design/icons/PoweroffOutlined';
import CheckOutlined from '@ant-design/icons/CheckOutlined';
import BellOutlined from '@ant-design/icons/BellOutlined';
import DownloadOutlined from '@ant-design/icons/DownloadOutlined';
import PlusOutlined from '@ant-design/icons/PlusOutlined';
import EyeOutlined from '@ant-design/icons/EyeOutlined';
import EyeInvisibleOutlined from '@ant-design/icons/EyeInvisibleOutlined';
import TranslationOutlined from '@ant-design/icons/TranslationOutlined';
import MailOutlined from '@ant-design/icons/MailOutlined';
import AppstoreOutlined from '@ant-design/icons/AppstoreOutlined';
import ClusterOutlined from '@ant-design/icons/ClusterOutlined';

Icon.SettingOutlined = SettingOutlined;
Icon.UnorderedListOutlined = UnorderedListOutlined;
Icon.UserOutlined = UserOutlined;
Icon.UserAddOutlined = UserAddOutlined;
Icon.UsergroupDeleteOutlined = UsergroupDeleteOutlined;
Icon.BlockOutlined = BlockOutlined;
Icon.LockOutlined = LockOutlined;
Icon.DashboardOutlined = DashboardOutlined;
Icon.FormOutlined = FormOutlined;
Icon.TableOutlined = TableOutlined;
Icon.ProfileOutlined = ProfileOutlined;
Icon.InfoCircleOutlined = InfoCircleOutlined;
Icon.CheckCircleOutlined = CheckCircleOutlined;
Icon.FullscreenOutlined = FullscreenOutlined;
Icon.FullscreenExitOutlined = FullscreenExitOutlined;
Icon.MenuUnfoldOutlined = MenuUnfoldOutlined;
Icon.MenuFoldOutlined = MenuFoldOutlined;
Icon.LoadingOutlined = LoadingOutlined;
Icon.IdcardOutlined = IdcardOutlined;
Icon.PoweroffOutlined = PoweroffOutlined;
Icon.CheckOutlined = CheckOutlined;
Icon.BellOutlined = BellOutlined;
Icon.DownloadOutlined = DownloadOutlined;
Icon.PlusOutlined = PlusOutlined;
Icon.EyeOutlined = EyeOutlined;
Icon.EyeInvisibleOutlined = EyeInvisibleOutlined;
Icon.TranslationOutlined = TranslationOutlined;
Icon.MailOutlined = MailOutlined;
Icon.AppstoreOutlined = AppstoreOutlined;
Icon.ClusterOutlined = ClusterOutlined;

export type IconType = keyof typeof Icon;

interface IconProps {
  type?: IconType;
  className?: string;
  style?: CSSProperties;
  rotate?: number;
  spin?: boolean;
  twoToneColor?: string; // (十六进制颜色)
}

export default function Icon({ type, ...iconProps }: IconProps) {
  if (!type) {
    return null;
  }
  const IcomComp = Icon[type];
  return <IcomComp {...iconProps} />;
}
