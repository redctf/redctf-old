import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import { action, configure, makeObservable, onBecomeObserved } from "mobx";
import { createContext } from "react";

// without configuring enforceActions it would be possible to modify any observable from anywhere
configure({ enforceActions: "observed" });

// base class
class APIStore {
  api: AxiosInstance;
  constructor(
    axiosConf: AxiosRequestConfig = {
      baseURL: "https://jsonplaceholder.typicode.com",
      auth: undefined,
    }
  ) {
    makeObservable(this, {
      users: true,
    });
    // setup api that should be in it's own class
    this.api = axios.create(axiosConf);

    // setup lazy observables
    onBecomeObserved(this, "users", this.getUsers);
  }

  users: User[] = [];
  // async / await
  getUsers = action(async () => {
    const { data } = await this.api.get<User[]>("/users");
    this.users = data;
    // return data;
  });

  // not using async/await is a little weirder
  // getUsers = () => this.api.get<User[]>('/users').then(
  //   action(({ data }) => {
  //     this.users = data;
  //     // return data;
  //   })
  // )
}

// all references should point to this singleton.
// If store is accessed outside of useContext (e.g. outside of React) you need to use this instance (unless you want multiple stores)!
export const APIStoreInstance = new APIStore();

export const APIStoreContext = createContext(APIStoreInstance);
