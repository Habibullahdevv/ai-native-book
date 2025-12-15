import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Welcome to the AI Native Book
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeatureItem({title, description, link}) {
  return (
    <div className={clsx('col col--3')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
        <Link className="button button--secondary" to={link}>
          Learn More
        </Link>
      </div>
    </div>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive guide to Physical AI, Humanoid Robotics, and more.">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <FeatureItem
                title="Module 1: Foundations of Physical AI"
                description="Learn the fundamentals of Physical AI and humanoid robotics."
                link="/docs/module1"
              />
              <FeatureItem
                title="Module 2: Locomotion & Control"
                description="Explore human locomotion, balance, and control in humanoid robotics."
                link="/docs/module2"
              />
              <FeatureItem
                title="Module 3: Perception & Intelligence"
                description="Discover perception and intelligence in Physical AI systems."
                link="/docs/module3"
              />
              <FeatureItem
                title="Module 4: HRI, Safety & Ethics"
                description="Understand human-robot interaction, safety, and ethical considerations."
                link="/docs/module4"
              />
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
