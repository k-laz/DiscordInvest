# Discord Invest -- GryphHacks 2022 Submission<br/>

<p align="center">
  <img src="https://user-images.githubusercontent.com/56948805/169717054-e55d7292-a81d-409a-a5a8-0558beac739e.png" alt="logo" width="120" height="120">
  <a>
    <img src="link here" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">GRYPH HACKS 2022</h3>

  <p align="center">
    <br/>
    <a href="https://discord.gg/sXJdbFxc">Join the server!</a>
    <br/>
  </p>
</p>

## Inspiration

The recent market crash made us very conscious of our investments. This inspired the creation of Discord Invest, a mock trading platform in a convenient form of a Discord bot. By gamifying the exchange, users can learn more about trading strategies, compete with friends, and ultimately have fun!

## Functionality

**Purchasing Shares**
The command for buying is ':buy'. The user can then proceed by specifiying the stock ticker and how many shares to purchase.

**Selling Shares**
When the user wants to sell their shares, they can run the command ':sell' to specifiy the ticker and how much they want to sell.

**Viewing Stock Information**
User can run the command ':info' and enter the ticker of a a stock they are looking for, to get more information on that type of the stock, the asset price, what market is it on and any associated fees of the transaction.

**Viewing Portfolio**
By running the command ':porfolio', the user can look at their porfolio where information about their stocks and current total evaluation resides.

**Viewing The Leaderboard**
To further gamify the system, we added a leaderboard functionality which tracks every user invested on the server and their returns. The command ranks top 5 investors and displays them in a neat format for evrybody to see.

## How we built it

Discord Invest was built collaboratively using python with discord.py library as our main tool. The functionality is split into several classes responsible for their own domain such as User, Stock, and DataBase. The user data is saved with the use of [CockroachDB](https://www.cockroachlabs.com/), a commercial distributed SQL database management system. Our primary tool for obtaining live financial data is [Finnhub Stock API](https://finnhub.io/).

## What did we learn

We learnt that collaborating on a technical projects with teammates in multiple timezones is a challenge of a bigger magnitude than one initially expects. Both GIT and Discord were invaluable in the efficient cooperation that culminated in this project. On the technical side, we learnt how to use financial API's, store data in the cloud using a relational database, and use a very convenient python library to build the bot.

## Built With

**Python, SQL, Finnhub Stock API, CockroachDB, Discord**

## Getting Started

To get started <a href="   server address  ">Click Me</a> to add the bot to your server.

## Usage

- **:buy** - Buy shares for your portfolio<br/>
- **:sell** - Sell shares from your portfolio <br/>
- **:info** - To get some more information about a particular stock <br/>
- **:portfolio** - To view your portfolio <br/>
- **:leaderboard** - To view the leaderboard of the server <br/>

## License

Distributed under the MIT License. See [LICENSE](https://github.com///blob/main/LICENSE.md) for more information.
