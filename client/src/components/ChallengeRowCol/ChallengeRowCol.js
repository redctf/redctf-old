import React, { useEffect, useState, createContext, useContext } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import axiosInstance from '../../axiosApi';
import JeopardyButton from '../ui/JeopardyButton/JeopardyButton';
import { AppState } from '../../stores/AppState';
const AppContext = createContext(new AppState());


async function getAllTeamSolves() {
  const query = `query me {
    me {
      id,
      team {
        id
        correctFlags
      }
    }
  }`;

  try {
    const response = await axiosInstance.post('/graphql/', {
      query: query
    });
    return response.data.data.me.team.correctFlags;
  } catch (error) {
    throw `Error in Login.js: ${error}`;
  } 
}


export default function ChallengeRowCol() {
    const store = useContext(AppContext);
    // const [teamSolves, setTeamSolves] = useState([]);

    const challenges = async() => {await Promise.resolve(store.getChallenges())};


    console.log('test', challenges);

    // const { challenges, categories, category, categoryId, vertical } = this.props;

    // const teamSolves = await getAllTeamSolves();



    const allTeamSolves = getAllTeamSolves().then(res => {
      return res;
    });
    
  
    const test = this.store;
    console.log('test', test)



    // Default to horizontal challenge orientation unless 'vertical' is passed in as a prop
    const direction = this.props.vertical ? 'vertical' : 'horizontal';  
    const challengeData = challenges.filter((challenge) => {
      if (challenge.category == categoryId) {
        return challenge;
      }
    });

    console.log('challengeData', challenges);

    challengeData.sort(function(a,b){return (a.points > b.points) ? 1 : ((b.points > a.points) ? -1 : 0); } );

    // Get array of solved challenges
    // const solved = this.store.appState.filterSingleTeam(team.id)[0].solved;

    // Map over JSON challenge data
    const challengeRowCol = challengeData.map((challenge) => {
      let challengeSolved = false;

      console.log('challenge', challenge);
      // solved.forEach((solve) => {
      //   if (solve.id == challenge.sid) {
      //     challengeSolved = true;
      //   }
      // });

      // Need to just send challenge, lol

      return (
        <JeopardyButton key={challenge.sid}
          sid={challenge.sid}
          value={challenge.points}
          name={challenge.title}
          category={category}
          description={challenge.description}
          solves={challenge.solved_count}
          solved={challengeSolved}
          path={challenge.pathPrefix}
          fileUpload={challenge.fileUpload}
          hosted={challenge.hosted}
          downloadPath={challenge.downloadPath}
        />
      )
    });

    console.log('challengeRowCol', challengeRowCol);

    const cat = (
      <span className='challengeCategory'>{category}</span>
    )

    return (
      <div className='challengeRowCol'>
        <div className={direction}>
          {cat} {challengeRowCol}
        </div>
      </div>
    );
  
  }


ChallengeRowCol.propTypes = {
  categories: PropTypes.array.isRequired,
  challenges: PropTypes.array.isRequired,
  category: PropTypes.string.isRequired,
  categoryId: PropTypes.string.isRequired
};