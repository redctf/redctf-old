import React, { useEffect, Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
// import JeopardyButton from '../ui/JeopardyButton';

import useUser from '../../hooks/useUser';

async function retrieveFromGraphQL(mut){
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

export default class ChallengeRowCol extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  render() {
    const { challenges, categories, category, categoryId, vertical } = this.props;

    const teamSolves = async () => {return await retrieveFromGraphQL(`query {
      myTeam {
        solved {
          challenge {
            id
          }
        }
      }
    }`)};

    console.log('teamSolves', teamSolves)



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
      // solved.forEach((solve) => {
      //   if (solve.id == challenge.sid) {
      //     challengeSolved = true;
      //   }
      // });

      // Need to just send challenge, lol

      return (
        <div>{challenge.title}</div>
        // <JeopardyButton key={challenge.sid}
        //   sid={challenge.sid}
        //   value={challenge.points}
        //   name={challenge.title}
        //   category={category}
        //   description={challenge.description}
        //   solves={challenge.solved_count}
        //   solved={challengeSolved}
        //   path={challenge.pathPrefix}
        //   fileUpload={challenge.fileUpload}
        //   hosted={challenge.hosted}
        //   downloadPath={challenge.downloadPath}
        // />
      )
    });

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
}


ChallengeRowCol.propTypes = {
  categories: PropTypes.array.isRequired,
  challenges: PropTypes.array.isRequired,
  category: PropTypes.string.isRequired,
  categoryId: PropTypes.string.isRequired
};