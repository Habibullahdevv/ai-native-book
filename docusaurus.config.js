import { themes as prismThemes } from 'prism-react-renderer';



/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI Native Book',
  tagline: 'A comprehensive guide to Physical AI and more.',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://Habibullahdevv.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages deployment, it is often '/<projectName>/'
  baseUrl: '/ai-native-book/', // Replace with your repository name

  // GitHub pages deployment config.
  // If you aren't using GitHub Pages, you don't need these.
  organizationName: 'Habibullahdevv', // Usually your GitHub org/user name.
  projectName: 'ai-native-book', // Usually your repo name.
  trailingSlash: false,

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Custom fields for runtime configuration
  customFields: {
    // Chat API URL - override via environment variable for production
    chatApiUrl: process.env.CHAT_API_URL || 'http://localhost:8000',
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Client modules - inject ChatWidget on all pages
  clientModules: [
    require.resolve('./src/clientModules/chatWidget.js'),
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo. For example: alois/docusaurus-ai-native-book
          editUrl: 'https://github.com/Habibullahdevv/ai-native-book/tree/main/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo. For example: alois/docusaurus-ai-native-book
          editUrl: 'https://github.com/Habibullahdevv/ai-native-book/tree/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      // image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'AI Native Book',
        // logo: {
        //   alt: 'My Site Logo',
        //   src: 'img/logo.svg',
        // },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book Modules',
          },
          // {
          //   to: '/blog',
          //   label: 'Blog',
          //   position: 'left'
          // },
          // {
          //   href: 'https://github.com/facebook/docusaurus',
          //   label: 'GitHub',
          //   position: 'right',
          // },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Module 1',
                to: '/docs/module1',
              },
              {
                label: 'Module 2',
                to: '/docs/module2',
              },
              {
                label: 'Module 3',
                to: '/docs/module3',
              },
              {
                label: 'Module 4',
                to: '/docs/module4',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Habibullahdevv/ai-native-book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} My Book, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      // Algolia DocSearch - commented out until API credentials are configured
      // algolia: {
      //   appId: 'YOUR_APP_ID',
      //   apiKey: 'YOUR_API_KEY',
      //   indexName: 'ai-native-book',
      // },
    }),
};

module.exports = config;