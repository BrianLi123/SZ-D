// 导入 Mock
import Mock from 'mockjs';

// 生成模拟数据
export const direct_data = Mock.mock({
  code: 200,
  // 生成5条数据，具体设置可查看官方文档
  'data|7': [
    {
      id: '@increment()',
      object: '@name', // name
      title: '@ctitle',
      'list|5-20': [{ attribute: '@upper(@word(5, 15)' }] // attribute
      // string: '@string()', // "jPXEu"
    }
  ]
});
export const related_data = Mock.mock({
  code: 200,
  // 生成5条数据，具体设置可查看官方文档
  'data|22': [
    {
      id: '@increment()',
      object: '@name', // name
      title: '@ctitle',
      'list|5-20': [{ attribute: '@upper(@word(5, 15)' }] // attribute
      // string: '@string()', // "jPXEu"
    }
  ]
});

// Mock.mock('/list', 'get', {
// 	code: 200,
// 	// 生成5条数据，具体设置可查看官方文档
// 	'data|7': [
// 		{
// 			id: '@increment()',
// 			object: '@name', // name
// 			word2: '@upper(@word(5, 15)', // attribute
// 			title: '@ctitle',
// 			'total|1000': 8,
// 		},
// 	],
// })
