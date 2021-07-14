# Does the number of NBA trades/transactions in a season affect a teams's efficiency? 

Evaluting whether the number of NBA trades/transactions, which includes trades, free agent signings, draft picks, etc., has any impact on the performance of the team throughout the season. I will be measuring the correlation between a teams win percentage, playoff wins and finals appearances with the number of transactions during each season from the 2018-2019 season to the current one, 2020-2021. This analysis sets to provide quantitative evidence that team chemistry is a significat factor in a team's ability to be successful during the regular season and post-season.

**Audience**: NBA fanatics who obsess over every trade their favorite team may or may not make.

Data is gathered and scraped from the NBA API and from www.prosportstransactions.com/basketball, respectively.

Null Hypothesis, using Pearson Correlation Coefficient: 

\begin{equation}
\rho_{xy} = \frac{[E[X-E[X])(Y-E[Y])}{\sigma_x \sigma_y} = 0
\end{equation}


Alternative Hypothesis:
\begin{equation}
\rho_{xy} = \frac{[E[X-E[X])(Y-E[Y])}{\sigma_x \sigma_y} \neq 0
\end{equation}

**x** = [ wins, playoff wins, finals appearance]

**y** = [ # of transactions, +/- players added, money spent during season, market cap, pick quality]
