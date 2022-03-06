import {
  action,
  configure,
  makeObservable,
  observable,
  onBecomeObserved,
  onBecomeUnobserved,
} from 'mobx';
import { createContext } from 'react';

// without configuring enforceActions it would be possible to modify any observable from anywhere
configure({ enforceActions: "observed" });

// base class
class AppState {
  socket: WebSocket | null = null;
  socketURL: string = 'ws://localhost:8080/ws';
  constructor(socketURL: string) {
    makeObservable(this, {
      coins: observable,
    });
    this.socketURL = socketURL;
    // setup lazy observables
    onBecomeObserved(this, "coins", this.startSocket);
    // close the socket if no more observers (multiple routes etc)
    onBecomeUnobserved(this, "coins", this.socket?.close ?? (() => {}));
  }

  coins: { [id: string]: string } = {};

  startSocket = () => {
    this.socket = new WebSocket(this.socketURL);
    this.socket.onclose = () => setTimeout(() => this.startSocket(), 5000);
    this.socket.onmessage = this.updateCoins;
  };

  updateCoins = action(({ data }: MessageEvent) => {
    const newCoins = JSON.parse(data);
    this.coins = { ...this.coins, ...newCoins };
  });
}

export const CoinStoreInstance = new CoinStore(
  "wss://ws.coincap.io/prices?assets=ALL"
);

export const CoinStoreContext = createContext(CoinStoreInstance);
