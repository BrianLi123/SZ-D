import Icon from '@/components/Icons';
import { Dropdown, Row, Col } from 'antd';
import { setLanguage, selectLanguage } from '@/store/reducer/langSlice';

const LanguageSetting = () => {
  const dispatch = useAppDispatch();

  const lang = useAppSelector(selectLanguage);
  return (
    <Dropdown
      trigger={['hover']}
      menu={{
        selectable: true,
        defaultSelectedKeys: [lang],
        style: { width: 110 },
        onClick: (e) => {
          const { key } = e;
          dispatch(setLanguage(key));
        }
      }}
    >
      <Row
        gutter={10}
        style={{
          cursor: 'pointer',
          marginTop: -2,
          userSelect: 'none',
          padding: '0 10px'
        }}
      >
        <Col>
          <Icon type="TranslationOutlined" />
        </Col>
      </Row>
    </Dropdown>
  );
};
export default memo(LanguageSetting);
