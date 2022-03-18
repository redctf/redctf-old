import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ChallengeRowCol from '../../components/ChallengeRowCol/ChallengeRowCol';
import axiosInstance from '../../axiosApi';
import './Challenges.scss';
import myAxios from '../../utils/api';

async function getAllCategories() {
  const mut = `query {
    categories {
      id
      name
    }
  }`;

  try {
    const response = await axiosInstance.post('/graphql/', {
      query: mut
    });
    return response.data.data.categories;
  } catch (error) {
    throw `Error in Login.js: ${error}`;
  }
}

async function getAllChallenges() {
  const mut = `query challenges {
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


  try {
    const response = await axiosInstance.post('/graphql/', {
      query: mut
    });
    return response.data.data.challenges;
  } catch (error) {
    throw `Error in Login.js: ${error}`;
  } 
}


export default function Challenges() {
  const [categories, setCategories] = useState([]);
  const [challenges, setChallenges] = useState([]);
  const categoryOrientationClass = 'horizontal';

  useEffect(() => {
    const getCategories = async () => {
      const categories = await getAllCategories();
      setCategories(categories);
    };
    getCategories();

    const getChallenges = async () => {
      const challenges = await getAllChallenges();
      setChallenges(challenges);
    };
    getChallenges();
  }, []);

  const categoryMap = categories ? categories.map(category => {
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
  }) : '';

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