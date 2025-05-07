import React from 'react';
import Icon from '@/components/Icons';
import { DefaultFooter } from '@ant-design/pro-components';

const Footer: React.FC = () => {
  return (
    <DefaultFooter
      className="site-footer"
      copyright={false}
      links={[
        {
          key: 'LPS',
          title: 'LPS',
          href: '',
          blankTarget: false
        }
      ]}
    />
  );
};

export default Footer;
