# covid-prediction-challenge
Codebase that powers: <a href="covidpredictions.com"> covidpredictions.com </a>

Right now, (3/20/2020), it is extremely difficult to know the difference between outlandish, modest, politically motivated, financially motivated, plain lazy, or useless predictions on the effects of COVID-19 on the planet. There are predictions saying that it will infect 40% of the world, 70% of the world, and some play it really safe and say <a href="https://thehill.com/changing-america/well-being/prevention-cures/482794-officials-say-the-cdc-is-preparing-for"> 40-70% of the world </a>. The first 2 are wildly different but specific enough to be useful, the last is so broad it is not useful, this imputes a variance of 2.3 billion people?! We can not be more precise than that? Lets see..

They and many others are reporting forecasts, some are wrong, some, as <a href="https://www.cnn.com/2020/03/22/world/doomsday-prophets-coronavirus-blake/index.html"> CNN reports </a>, are dangerous, some are fantastic (<a href="https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf"> here </a> is the article that convinced Trump to begin suppression, <a href="https://covidactnow.org/"> here is my personal favorite right now</a>, and <a href='https://github.com/daveselinger/covid-19-hackathon'>here</a>, <a href='https://github.com/coronafighter/coronaSEIR'>here</a>, <a href='https://midasnetwork.us/covid-19/'>here</a> , and <a href='https://github.com/HopkinsIDD/ncov_incubation'>here</a> are many others), but who is right? They all made many, many assumptions as all predictions must, they modeled it one way or another, some will be more right than others. So who to listen to? 
<br/><br/>
The world needs accurate COVID-19 infection/death models so that people can make informed decisions about how to react to the new realities around them. If you knew with 80% probability your grandmother was going to die in June, 2020, would you change something about your life? Would you tell her with confidence to do something different? Or if you knew that with 0.3% probability that she would die in June 2020, would that change your answer? If there is a difference, then that proves this initiative's worth. 
<br/><br/>
As AI workers, there is only so much that we can do to help this crisis. I am not a pathologist, I am not an epidemiologist, I am not a nurse, and I’m not a doctor. I know how to take large amounts of data, train models that will be robust enough to predict the future with some confidence interval based on a lot of best practices in Machine Learning. A useful thing I may be able to do is to provide a prediction that approaches the Shannon Bound for what is going to happen, how many people will die, when, where, and who. While this is horrible to consider, this is very useful for a number of reasons in my point of view. 
<br/><br/>
<ul>
<li>First, we will be able to react and change our lives conditioned upon this information. </li>
<li>Second, we will be able to trust a prediction and avoid overstatements/overreactions and understatements/underreactions of what will happen. </li>
<li>Third, perhaps government officials, health workers, etc will be able to use the community's models to triage and rank sort key areas and people that need resources, attention, and to be quarantined first. </li>
<li>Last, and probably least, there is no downside / risk to this. Even if the above benefits do not happen, doing nothing feels worse than doing something that may or may not serve some use to the world, so via pascal's wager, lets contribute and lets use AI / datascience to help bring clarity to the complexity like we know how! </li>
</ul>

Predicting deaths and number of sick people is an unfortunate reality, but it must be done. These are real people with real life and real families not data points on a plot. But for the world to know how to react they must TRUST the predictions of the future, and right now in the post fact era people are too skeptical of sensationalism to sell ads, politicians spinning things to overstate how great a job they are doing, fake news published by foreign entities, etc. We need predictions from experts controlled for any potential bias, pitted against each other on a nowcasting challenge, where each person's models have been forcibly submitted weeks/months in advance, so you can clearly see which projections are worth their salt. This project seeks to fill this gap, by offering a framework for us to decipher how much better one prediction is from the other.

For those of you like me who want to help this cause with their skill set please contribute a prediction. 

<h1>How this works</h1>
In science, it is control and careful analysis that allow us to know anything with any amount of certainty. That is what this project offers. 

The way we will do this is the following:
1. Every night the world health organization and many other health organizations publish their data online. John Hopkins University scraped this data and made it available by their APIs. 
2. We will pull that data every night and measure the accuracy of all the submissions against that day and the previous days. 
3. In order to prevent an unfair advantage of the natural autoregressive properties of the dependent variables, we do not score the first week of any submission and certainly not days before the submission date. Thus, we will not calculate and you will not see your scores until a week after the submission date. Thereafter, you will see your scores update at 2am every night.
4. We will rank and publish the full report of the top 10 submissions that will change daily.


 <h1>Getting started</h1>
Getting started is very easy. We will provide a starter ipython notebook that will download all the most recent data and create a naïve predictions.csv that you can drag and drop into the submit form. This is only a helper script and not required to be used at all. 
A predictions.csv must initially include the following columns: date (YYYY/MM/DD) starting a week after submission date (all previous dates/rows will be ignored anyway), # of people infected globally, and death rate globally. Then later if people are using this, we can add country level predictions, and age level predictions. We will report scores for all submissions above a certain accuracy. 

In the submit prediction form, you can submit the csv, name of submitter, and optionally add a github link / ipython nb. 

<h1>Submissions</h1>
COMING SOON.

<h1>Results</h1>
COMING SOON.

<h1>Contributing to the Core Project</h1>
If you would like to help on this project or you have any questions, please send a note to fchaubard [[at]] gmail.com. 
