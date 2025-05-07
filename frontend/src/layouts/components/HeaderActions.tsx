import { Space } from 'antd';
import FullScreenHeaderButton from './FullScreen';
import PersonalCenter from './PersonalCenter';
// import LanguageSetting from './LanguageSetting';
import LocalSettingsHeaderButton from './LocalSettings';

export default function HeaderActions() {
  return (
    <Space>
      <FullScreenHeaderButton />
      <PersonalCenter />
      {/* <LanguageSetting /> */}
      <LocalSettingsHeaderButton />
    </Space>
  );
}
