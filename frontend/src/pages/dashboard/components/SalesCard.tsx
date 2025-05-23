import { Card, Tabs, Space, DatePicker, type TabsProps } from 'antd';
import { Column } from '@ant-design/plots';
import '../style.css';
const { RangePicker } = DatePicker;

interface SalesCardProps {
  loading: boolean;
  data: any[];
}

const tabBarStyle = { marginBottom: 24, padding: '0 16px' };

function SalesCard({ loading, data }: SalesCardProps) {
  const items: TabsProps['items'] = [
    {
      key: 'sales',
      label: '销售额',
      children: (
        <Column
          height={300}
          autoFit
          data={data}
          xField="x"
          yField="y"
          xAxis={{
            title: {
              text: '2022年'
            }
          }}
          yAxis={{
            title: {
              text: '销售量'
            }
          }}
          meta={{
            y: {
              alias: '销售量'
            }
          }}
        />
      )
    },
    {
      key: 'views',
      label: '访问量',
      children: (
        <Column
          height={300}
          autoFit
          data={data}
          xField="x"
          yField="y"
          xAxis={{
            title: {
              text: '2022年'
            }
          }}
          yAxis={{
            title: {
              text: '访问量'
            }
          }}
          meta={{
            y: {
              alias: '访问量'
            }
          }}
        />
      )
    }
  ];
  return (
    <Card
      loading={loading}
      bordered={false}
      styles={{ body:{ padding: 0 }}}
      className="analysis_salesCard"
      style={{ height: '100%' }}
    >
      <Tabs
        size="large"
        items={items}
        tabBarStyle={tabBarStyle}
        tabBarExtraContent={<TabBarExtraContent />}
      />
    </Card>
  );
}

function TabBarExtraContent() {
  return (
    <Space size="large">
      <a>今日</a>
      <a>本周</a>
      <a>本月</a>
      <a>本年</a>
      <RangePicker
        style={{ width: 256 }}
        onChange={(date, string) => {
          console.log(date, string);
        }}
      />
    </Space>
  );
}

export default SalesCard;
