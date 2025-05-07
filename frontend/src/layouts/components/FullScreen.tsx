import React, { memo } from 'react';
import { Tooltip, Button } from 'antd';
import Icon from '@/components/Icons';
import { useFullscreen } from 'ahooks';

function FullScreenHeaderButton() {
  const [isFullscreen, { toggleFullscreen }] = useFullscreen(() =>
    document.querySelector('html')
  );
  const [tooltipTitle, setTooltipTitle] = useState('');
  const lang = useAppSelector(selectLanguage);

  useEffect(() => {
    setTooltipTitle(isFullscreen ? '退出全屏' : '进入全屏');
  }, [isFullscreen, lang]);

  return (
    <Tooltip placement="bottom" title={tooltipTitle} arrow>
      <Button
        type="text"
        icon={React.createElement(
          !isFullscreen ? Icon.FullscreenOutlined : Icon.FullscreenExitOutlined
        )}
        onClick={toggleFullscreen}
      />
    </Tooltip>
  );
}

export default memo(FullScreenHeaderButton);
