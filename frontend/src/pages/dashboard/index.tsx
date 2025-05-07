import SalesCard from './components/SalesCard';
import Ranking from './components/Ranking';
import { Row, Col } from 'antd';

export default function Analysis() {
  // const { loading, data = {} } = useRequest(fetchAnalysisChart);
  const [salesData, setSalesData] = useState<{ x: string; y: number }[]>([]);
  const [loading, setLoading] = useState(true);
  setTimeout(() => {
    setSalesData([
      {
        x: '1月',
        y: 931
      },
      {
        x: '2月',
        y: 310
      },
      {
        x: '3月',
        y: 777
      },
      {
        x: '4月',
        y: 461
      },
      {
        x: '5月',
        y: 345
      },
      {
        x: '6月',
        y: 777
      },
      {
        x: '7月',
        y: 915
      },
      {
        x: '8月',
        y: 843
      },
      {
        x: '9月',
        y: 814
      },
      {
        x: '10月',
        y: 685
      },
      {
        x: '11月',
        y: 602
      },
      {
        x: '12月',
        y: 620
      }
    ]);
    setLoading(false);
  }, 800);

  return (
    <>
      <Row gutter={16}>
        <Col span={16}>
          <SalesCard loading={loading} data={salesData} />
        </Col>
        <Col span={8}>
          <Ranking loading={loading} data={Array.from({ length: 18 })} />
        </Col>
      </Row>
    </>
  );
}
