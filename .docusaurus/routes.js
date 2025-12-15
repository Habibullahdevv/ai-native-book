import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/ai-native-book/search',
    component: ComponentCreator('/ai-native-book/search', 'fd7'),
    exact: true
  },
  {
    path: '/ai-native-book/docs',
    component: ComponentCreator('/ai-native-book/docs', '590'),
    routes: [
      {
        path: '/ai-native-book/docs',
        component: ComponentCreator('/ai-native-book/docs', '3a3'),
        routes: [
          {
            path: '/ai-native-book/docs',
            component: ComponentCreator('/ai-native-book/docs', '8da'),
            routes: [
              {
                path: '/ai-native-book/docs/intro',
                component: ComponentCreator('/ai-native-book/docs/intro', 'f9f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module-1',
                component: ComponentCreator('/ai-native-book/docs/module-1', '99c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module-1/chapter-1',
                component: ComponentCreator('/ai-native-book/docs/module-1/chapter-1', 'b14'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module-1/chapter-2',
                component: ComponentCreator('/ai-native-book/docs/module-1/chapter-2', 'e3d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module-1/chapter-3',
                component: ComponentCreator('/ai-native-book/docs/module-1/chapter-3', '0d0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module-1/chapter-4',
                component: ComponentCreator('/ai-native-book/docs/module-1/chapter-4', 'a34'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module-1/chapter-5',
                component: ComponentCreator('/ai-native-book/docs/module-1/chapter-5', '1ba'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module2',
                component: ComponentCreator('/ai-native-book/docs/module2', '79a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module2/chapter1',
                component: ComponentCreator('/ai-native-book/docs/module2/chapter1', 'e17'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module2/chapter2',
                component: ComponentCreator('/ai-native-book/docs/module2/chapter2', '2e8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module2/chapter3',
                component: ComponentCreator('/ai-native-book/docs/module2/chapter3', 'c14'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module2/chapter4',
                component: ComponentCreator('/ai-native-book/docs/module2/chapter4', '912'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module2/chapter5',
                component: ComponentCreator('/ai-native-book/docs/module2/chapter5', '00d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module3',
                component: ComponentCreator('/ai-native-book/docs/module3', '9fe'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module3/chapter1',
                component: ComponentCreator('/ai-native-book/docs/module3/chapter1', 'd9b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module3/chapter2',
                component: ComponentCreator('/ai-native-book/docs/module3/chapter2', '80f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module3/chapter3',
                component: ComponentCreator('/ai-native-book/docs/module3/chapter3', 'd18'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module3/chapter4',
                component: ComponentCreator('/ai-native-book/docs/module3/chapter4', 'aa7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module3/chapter5',
                component: ComponentCreator('/ai-native-book/docs/module3/chapter5', '5b9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module4',
                component: ComponentCreator('/ai-native-book/docs/module4', '669'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module4/chapter1',
                component: ComponentCreator('/ai-native-book/docs/module4/chapter1', 'a32'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module4/chapter2',
                component: ComponentCreator('/ai-native-book/docs/module4/chapter2', '0e4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module4/chapter3',
                component: ComponentCreator('/ai-native-book/docs/module4/chapter3', 'd2a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module4/chapter4',
                component: ComponentCreator('/ai-native-book/docs/module4/chapter4', '84b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module4/chapter5',
                component: ComponentCreator('/ai-native-book/docs/module4/chapter5', 'e5a'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
