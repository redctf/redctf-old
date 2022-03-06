import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ChallengeRowCol from '../../components/ChallengeRowCol/ChallengeRowCol';
import './Challenges.scss';
import myAxios from '../../utils/api';


// onbecomeobserver(async () => {
//   const { data } = await axios.get('/api/challenges');
//   console.log('data', data);
//   setChallenges(data);
// });

// react.context.api - share globals and objects between components

// socket.io channel, group subscriptions (teams)

async function retrieveFromGraphQL(mut){
  // myAxios.post('/graphql/', { query: mut }).then(res => {')
  axios.defaults.baseURL = `${window.location.protocol}//${window.location.hostname}`;
  axios.defaults.withCredentials = true;
  const res = await axios.post('/graphql/', {
    query: mut,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  });

  console.log(`retrieved from graphql (${Object.keys(res.data.data)[0]} ): `, res.data.data[`${Object.keys(res.data.data)[0]}`]);
  return await res.data.data[`${Object.keys(res.data.data)[0]}`];
}

export default function Challenges() {
  const [categories, setCategories] = useState([]);
  const [challenges, setChallenges] = useState([]);
  const categoryOrientationClass = 'horizontal';
  const mutCategories = `query {
    categories {
      id
      name
    }
  }`;

  const mutChallenges = `query challenges {
    challenges {
      id
      title
      description
      category {
        id
      }
      points
      hosted
      fileUpload
      imageName
      ports
      pathPrefix
      upload
      created
    }
}`;

  useEffect(async () => {
    const getCategories = async () => {
      const categories = await retrieveFromGraphQL(mutCategories);
      setCategories(categories);
    };
    getCategories();

    const getChallenges = async () => {
      const challenges = await retrieveFromGraphQL(mutChallenges);
      setChallenges(challenges);
    };
    getChallenges();
  }, []);

  const categoryMap = categories.map(category => {
    return (
      <div key={category.id}
        className={`category-${categoryOrientationClass}`}>
        <ChallengeRowCol categories={categories}
          challenges={challenges}
          category={category.name}
          categoryId={category.id}
        />
      </div>
    );
  });

  return (
    <div>
      <div className='challenges-wrapper'>
        <div className={`redctf-page redctf-page-${categoryOrientationClass}`}>
          {categoryMap}
        </div>
        <div className='legend'>
          <span className='solved-key-color'/><span className='solved-key'>Solved</span>
          <span className='unsolved-key-color'/><span className='unsolved-key'>Unsolved</span>
        </div>
      </div>
    </div>
  );
}