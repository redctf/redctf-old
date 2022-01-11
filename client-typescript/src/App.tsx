import logo from "./logo.svg";
import style from "./App.module.scss";
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Home from './pages/Home';
import Login from './pages/Login';

function App() {
  return (
    <div className={style.App}>
      <h1>Test</h1>

      {/* <header className={style["App-header"]}>
        <img src={logo} className={style["App-logo"]} alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className={style["App-link"]}
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
    </div>
  );
}

export default App;
