# MLB Predictor

## Tech Stack

Built using React, PostgreSQL, Flask, Beautiful Soup, and Scikit-learn.

## Challenges

The main challenge that I faced while building this project was learning the Flask framework instead of Node. Since I had primarily worked with the MERN stack before, I was more familiar with Node.js and Express for building APIs. Switching to Flask meant adapting to a different framework structure, understanding Python-specific features, and learning how to manage routes, models, and templates differently.

After figuring that out, I had to learn how to implement Scikit-learn's Random Forest Classifier into my app without any prior experience with machine learning models. Through research, I determined that the Random Forest Classifier would be ideal for predicting MLB game outcomes, as it combines the predictions of several decision trees and works well with the data I believed to be most important for predictions: team name, opponent name, rank, home or away status, and win-loss records.
