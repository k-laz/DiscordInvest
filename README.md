# Discord Invest <br/>

<p align="center">
  <a>
    <img src="https://user-images.githubusercontent.com/56948805/169717054-e55d7292-a81d-409a-a5a8-0558beac739e.png" alt="logo" width="180" height="180">
  </a>
  <h5 align="center">GryphHacks 2022 submission</h5>
</p>

## Usage

- **:buy** - Buy shares<br/>
- **:sell** - Sell shares<br/>
- **:info** - To get some more information about a particular stock <br/>
- **:portfolio** - To view your portfolio <br/>
- **:leaderboard** - To view the leaderboard of the server <br/>

## Inspiration

The recent market crash made us very conscious of our investments. This inspired the creation of Discord Invest, a mock trading platform in a convenient form of a Discord bot. By gamifying the exchange, users can learn more about trading strategies, compete with friends, and ultimately have fun!

## How we built it

Discord Invest was built collaboratively using python with discord.py library as our main tool. The functionality is split into several classes responsible for their own domain such as User, Stock, and DataBase. The user data is saved with the use of [CockroachDB](https://www.cockroachlabs.com/), a commercial distributed SQL database management system. Our primary tool for obtaining live financial data is [Finnhub Stock API](https://finnhub.io/).

## What did we learn

We learnt that collaborating on a technical projects with teammates in multiple timezones is a challenge of a bigger magnitude than one initially expects. Both GIT and Discord were invaluable in the efficient cooperation that culminated in this project. On the technical side, we learnt how to use financial API's, store data in the cloud using a relational database, and use a very convenient python library to build the bot.

## Built With

**Python, SQL, Finnhub Stock API, CockroachDB, Discord**

## Getting Started

To get started <a href="https://discord.gg/sXJdbFxc">Join the server!</a>

## License

Distributed under the MIT License. See [LICENSE](https://github.com///blob/main/LICENSE.md) for more information.
