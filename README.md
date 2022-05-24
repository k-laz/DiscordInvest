# Discord Invest <img src="https://user-images.githubusercontent.com/56948805/169717054-e55d7292-a81d-409a-a5a8-0558beac739e.png" align="right" alt="logo" width="180" height="180">
<br/>

## Usage

- **$invest** - Initializes the trading platform, all commands follow it<br/>
- **sell** - Sell shares<br/>
- **buy** - Buy shares<br/>
- **portfolio** - To view your portfolio <br/>
- **help** - To view a list of commands <br/>

## Inspiration

The recent market crash made us very conscious of our investments. This inspired the creation of Discord Invest, a mock trading platform in a convenient form of a Discord bot. By gamifying the exchange, users can learn more about trading strategies, compete with friends, and ultimately have fun!

## How we built it

Discord Invest was built collaboratively using python with discord.py library as our main tool. The functionality is split into several classes responsible for their own domain such as User, Stock, and DataBase. The user data is saved with the use of [CockroachDB](https://www.cockroachlabs.com/), a commercial distributed SQL database management system. Our primary tool for obtaining live financial data is [Finnhub Stock API](https://finnhub.io/).

## What did we learn

We learnt that collaborating on a technical projects with teammates in multiple timezones is a challenge of a bigger magnitude than one initially expects. Both GIT and Discord were invaluable in the efficient cooperation that culminated in this project. On the technical side, we learnt how to use financial API's, store data in the cloud using a relational database, and use a very convenient python library to build the bot.

## Built With
* [Python](https://www.python.org/)
* [CockroachDB](https://www.cockroachlabs.com/)
* [Finnhub Stock API](https://finnhub.io/)
* [discord.py](https://discordpy.readthedocs.io/en/stable/)

## Getting Started

To get started <a href="https://discord.gg/sXJdbFxc">Join the server!</a>

## License

Distributed under the MIT License. See [LICENSE](https://github.com///blob/main/LICENSE.md) for more information.
